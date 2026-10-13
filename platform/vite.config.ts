import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import fs from 'fs';
import path from 'path';

function courseApiPlugin() {
  const getCoursesDir = () => path.resolve(__dirname, '../courses');

  function validateCourseJson(filePath: string, content: string) {
    // Check for silent unescaped control characters in raw text
    const controlCharRegex = /[\x00-\x08\x0b\x0c\x0e-\x1f]/;
    if (controlCharRegex.test(content)) {
      return {
        valid: false,
        error: 'Contains unescaped control characters or corrupted LaTeX escapes',
      };
    }

    let parsed: any;
    try {
      parsed = JSON.parse(content);
    } catch (e: any) {
      return {
        valid: false,
        error: `Invalid JSON syntax: ${e.message}`,
      };
    }

    if (!parsed || typeof parsed !== 'object') {
      return { valid: false, error: 'Course root must be a JSON object' };
    }

    if (!parsed.course_id || typeof parsed.course_id !== 'string') {
      return { valid: false, error: 'Missing or invalid course_id' };
    }

    if (!parsed.title || typeof parsed.title !== 'string') {
      return { valid: false, error: 'Missing or invalid course title' };
    }

    if (!Array.isArray(parsed.competencies) || parsed.competencies.length === 0) {
      return { valid: false, error: 'Course must specify non-empty competencies array' };
    }

    if (!Array.isArray(parsed.questions) || parsed.questions.length === 0) {
      return { valid: false, error: 'Course must specify non-empty questions array' };
    }

    // Check for invalid question types
    const validTypes = ['multiple_choice_7_options', 'multiple_select', 'fill_in_the_blank'];
    for (const q of parsed.questions) {
      if (!validTypes.includes(q.type)) {
        return { valid: false, error: `Invalid question type: ${q.type}` };
      }
    }

    return { valid: true, data: parsed };
  }

  function getCourseList() {
    const coursesDir = getCoursesDir();
    if (!fs.existsSync(coursesDir)) {
      return [];
    }

    const files = fs.readdirSync(coursesDir).filter((f) => f.endsWith('.json'));
    const results: any[] = [];

    for (const file of files) {
      const fullPath = path.join(coursesDir, file);
      try {
        const raw = fs.readFileSync(fullPath, 'utf-8');
        const check = validateCourseJson(fullPath, raw);

        if (check.valid && check.data) {
          results.push({
            id: check.data.course_id,
            filename: file,
            title: check.data.title,
            description: check.data.description || '',
            status: 'valid',
            total_competencies: check.data.competencies.length,
            total_questions: check.data.questions.length,
            data: check.data,
          });
        } else {
          // Attempt to extract title or id for error card
          let fallbackTitle = file.replace('.json', '');
          try {
            const partial = JSON.parse(raw);
            if (partial.title) fallbackTitle = partial.title;
          } catch {}

          results.push({
            id: file.replace('.json', ''),
            filename: file,
            title: fallbackTitle,
            description: 'Corrupted or malformed course file',
            status: 'error',
            error_message: check.error || 'Validation failed',
          });
        }
      } catch (err: any) {
        results.push({
          id: file.replace('.json', ''),
          filename: file,
          title: file,
          description: 'Error reading course file',
          status: 'error',
          error_message: err.message,
        });
      }
    }

    return results;
  }

  function handleApiMiddleware(req: any, res: any, next: any) {
    const url = new URL(req.url, 'http://localhost');
    const pathname = url.pathname;

    const isCoursesList =
      pathname === '/api/courses' ||
      pathname === '/api/courses.json' ||
      pathname.endsWith('/api/courses') ||
      pathname.endsWith('/api/courses.json');

    if (isCoursesList && req.method === 'GET') {
      const courses = getCourseList();
      res.setHeader('Content-Type', 'application/json');
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.end(JSON.stringify({ courses }));
      return;
    }

    const detailMatch = pathname.match(/\/api\/courses\/([^/]+)$/);
    if (detailMatch && req.method === 'GET') {
      let requestedId = decodeURIComponent(detailMatch[1]);
      if (requestedId.endsWith('.json')) {
        requestedId = requestedId.slice(0, -5);
      }
      const courses = getCourseList();
      const found = courses.find((c) => c.id === requestedId || c.filename === requestedId || c.filename === `${requestedId}.json`);

      if (found && found.status === 'valid') {
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.end(JSON.stringify(found.data));
        return;
      } else if (found && found.status === 'error') {
        res.statusCode = 400;
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ error: found.error_message }));
        return;
      } else {
        res.statusCode = 404;
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ error: 'Course not found' }));
        return;
      }
    }

    next();
  }

  return {
    name: 'course-api-plugin',
    generateBundle() {
      const courses = getCourseList();
      this.emitFile({
        type: 'asset',
        fileName: 'api/courses.json',
        source: JSON.stringify({ courses }, null, 2),
      });

      for (const c of courses) {
        if (c.status === 'valid' && c.data) {
          this.emitFile({
            type: 'asset',
            fileName: `api/courses/${c.id}.json`,
            source: JSON.stringify(c.data, null, 2),
          });
          this.emitFile({
            type: 'asset',
            fileName: `courses/${c.filename}`,
            source: JSON.stringify(c.data, null, 2),
          });
        }
      }
    },
    closeBundle() {
      const distDir = path.resolve(__dirname, 'dist');
      const indexPath = path.join(distDir, 'index.html');
      const notFoundPath = path.join(distDir, '404.html');
      if (fs.existsSync(indexPath) && !fs.existsSync(notFoundPath)) {
        try {
          fs.copyFileSync(indexPath, notFoundPath);
        } catch {}
      }
    },
    configureServer(server: any) {
      server.middlewares.use(handleApiMiddleware);
    },
    configurePreviewServer(server: any) {
      server.middlewares.use(handleApiMiddleware);
    },
  };
}

export default defineConfig({
  base: process.env.VITE_BASE_PATH || './',
  plugins: [react(), courseApiPlugin()],
  server: {
    port: 5173,
    host: '127.0.0.1',
    strictPort: false,
  },
  preview: {
    port: 5173,
    host: '127.0.0.1',
  },
});
