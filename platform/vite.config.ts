import { defineConfig, Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);

function courseApiPlugin(): Plugin {
  const getCoursesDir = () => path.resolve(__dirname, '../courses');

  // Fallback indexing logic in case ./server/courseIndex.cjs is unavailable
  function createFallbackCourseIndex() {
    const coursesDir = getCoursesDir();

    function validateCourseJson(filePath: string, content: string) {
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

      const title = parsed.title || parsed.course_title;
      if (!title || typeof title !== 'string') {
        return { valid: false, error: 'Missing or invalid course title' };
      }
      parsed.title = title;

      if (!Array.isArray(parsed.competencies) || parsed.competencies.length === 0) {
        return { valid: false, error: 'Course must specify non-empty competencies array' };
      }

      if (!Array.isArray(parsed.questions) || parsed.questions.length === 0) {
        return { valid: false, error: 'Course must specify non-empty questions array' };
      }

      const validTypes = ['multiple_choice_7_options', 'multiple_select', 'fill_in_the_blank'];
      for (const q of parsed.questions) {
        const qType = q.type || q.interaction_type;
        if (!validTypes.includes(qType)) {
          return { valid: false, error: `Invalid question type: ${qType}` };
        }
      }

      return { valid: true, data: parsed };
    }

    function readAllCourses() {
      if (!fs.existsSync(coursesDir)) {
        return [];
      }

      const files = fs.readdirSync(coursesDir).filter((f) => f.endsWith('.json'));
      const results: any[] = [];

      for (const file of files) {
        const fullPath = path.join(coursesDir, file);
        try {
          const stat = fs.statSync(fullPath);
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
              bytes: stat.size,
              etag: `"${stat.mtimeMs.toString(36)}-${stat.size.toString(36)}"`,
              data: check.data,
            });
          } else {
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
              bytes: stat.size,
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

    return {
      getCoursesDir: () => coursesDir,
      buildIndex: () => {
        const all = readAllCourses();
        return {
          generated_at: new Date().toISOString(),
          courses: all.map(({ data, ...slim }) => slim),
        };
      },
      getManifest: () => {
        const all = readAllCourses();
        return {
          generated_at: new Date().toISOString(),
          courses: all.map(({ data, ...slim }) => slim),
        };
      },
      getSafeManifestHtmlScript: (manifest?: any) => {
        const m = manifest || {
          generated_at: new Date().toISOString(),
          courses: readAllCourses().map(({ data, ...slim }) => slim),
        };
        const safeJson = JSON.stringify(m).replace(/</g, '\\u003c');
        return `<script id="course-manifest" type="application/json">${safeJson}</script>`;
      },
      getCoursesWithData: () => readAllCourses(),
      getCourse: (requestedId: string) => {
        const all = readAllCourses();
        const found = all.find(
          (c) => c.id === requestedId || c.filename === requestedId || c.filename === `${requestedId}.json`
        );
        if (!found) return null;
        if (found.status === 'valid') return { valid: true, data: found.data };
        return { valid: false, error: found.error_message };
      },
      getCoursePath: (requestedId: string) => {
        const candidate = requestedId.endsWith('.json') ? requestedId : `${requestedId}.json`;
        const filePath = path.join(coursesDir, candidate);
        if (fs.existsSync(filePath)) return filePath;
        return null;
      },
    };
  }

  const fallback = createFallbackCourseIndex();

  function getCourseIndexModule() {
    const courseIndexPath = path.resolve(__dirname, 'server/courseIndex.cjs');
    if (fs.existsSync(courseIndexPath)) {
      try {
        delete require.cache[require.resolve(courseIndexPath)];
        return require(courseIndexPath);
      } catch (err) {
        console.warn('[vite.config] Warning: could not require ./server/courseIndex.cjs:', err);
      }
    }
    return null;
  }

  function stripData(manifestOrList: any) {
    if (!manifestOrList) return { generated_at: new Date().toISOString(), courses: [] };
    const courses = Array.isArray(manifestOrList.courses)
      ? manifestOrList.courses
      : Array.isArray(manifestOrList)
      ? manifestOrList
      : [];
    const slimCourses = courses.map((c: any) => {
      const { data, ...slim } = c;
      return slim;
    });
    return {
      generated_at: manifestOrList.generated_at || new Date().toISOString(),
      courses: slimCourses,
    };
  }

  function getIndexHelper() {
    const mod = getCourseIndexModule();
    if (mod) {
      return {
        getManifest: () => {
          if (typeof mod.getManifest === 'function') {
            return stripData(mod.getManifest());
          }
          if (typeof mod.buildIndex === 'function') {
            return stripData(mod.buildIndex());
          }
          if (typeof mod.getCourseList === 'function') {
            return stripData(mod.getCourseList());
          }
          return stripData(mod);
        },
        getSafeManifestHtmlScript: (manifest?: any) => {
          if (typeof mod.getSafeManifestHtmlScript === 'function') {
            return mod.getSafeManifestHtmlScript(manifest);
          }
          const m = manifest || stripData(mod.getManifest ? mod.getManifest() : mod);
          const safeJson = JSON.stringify(m).replace(/</g, '\\u003c');
          return `<script id="course-manifest" type="application/json">${safeJson}</script>`;
        },
        getCoursesWithData: () => {
          if (typeof mod.getManifest === 'function' && typeof mod.getCourseData === 'function') {
            const manifest = mod.getManifest();
            return manifest.courses.map((entry: any) => {
              if (entry.status !== 'valid') return { ...entry, data: null };
              const detail = mod.getCourseData(entry.id);
              return {
                ...entry,
                data: detail?.data || null,
              };
            });
          }
          if (typeof mod.getCoursesWithData === 'function') {
            return mod.getCoursesWithData();
          }
          if (typeof mod.getCourseList === 'function') {
            const list = mod.getCourseList();
            if (list.length > 0 && !list[0].data && typeof mod.getCourse === 'function') {
              return list.map((c: any) => {
                const res = mod.getCourse(c.id);
                return { ...c, data: res?.data || res };
              });
            }
            return list;
          }
          return fallback.getCoursesWithData();
        },
        getCourse: (id: string) => {
          if (typeof mod.getCourseData === 'function') {
            const res = mod.getCourseData(id);
            if (res) {
              if (res.status === 'valid' && res.data) return { valid: true, data: res.data };
              if (res.status === 'error') return { valid: false, error: res.error_message };
            }
          }
          if (typeof mod.getCourse === 'function') {
            const res = mod.getCourse(id);
            if (res) {
              if (res.data) return { valid: true, data: res.data };
              if (res.status === 'valid' && res.data) return res;
              if (res.status === 'error') return { valid: false, error: res.error || res.error_message };
              if (res.course_id) return { valid: true, data: res };
            }
          }
          if (typeof mod.getCoursePath === 'function') {
            const p = mod.getCoursePath(id);
            if (p && fs.existsSync(p)) {
              try {
                const raw = fs.readFileSync(p, 'utf-8');
                return { valid: true, data: JSON.parse(raw) };
              } catch (e: any) {
                return { valid: false, error: e.message };
              }
            }
          }
          return fallback.getCourse(id);
        },
        getCoursePath: (id: string) => {
          if (typeof mod.getCoursePath === 'function') {
            return mod.getCoursePath(id);
          }
          return fallback.getCoursePath(id);
        },
      };
    }
    return fallback;
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
      const helper = getIndexHelper();
      const manifest = helper.getManifest();
      res.setHeader('Content-Type', 'application/json');
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.end(JSON.stringify(manifest));
      return;
    }

    const detailMatch = pathname.match(/\/api\/courses\/([^/]+)$/);
    if (detailMatch && req.method === 'GET') {
      let requestedId = decodeURIComponent(detailMatch[1]);
      if (requestedId.endsWith('.json')) {
        requestedId = requestedId.slice(0, -5);
      }
      const helper = getIndexHelper();
      const result = helper.getCourse(requestedId);

      if (result && result.valid && result.data) {
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.end(JSON.stringify(result.data));
        return;
      } else if (result && result.error) {
        res.statusCode = 400;
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.end(JSON.stringify({ error: result.error }));
        return;
      } else {
        res.statusCode = 404;
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.end(JSON.stringify({ error: 'Course not found' }));
        return;
      }
    }

    const courseFileMatch = pathname.match(/^\/courses\/([^/]+)$/);
    if (courseFileMatch && req.method === 'GET') {
      let requestedFile = decodeURIComponent(courseFileMatch[1]);
      const helper = getIndexHelper();
      const result = helper.getCourse(requestedFile);
      if (result && result.valid && result.data) {
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.end(JSON.stringify(result.data));
        return;
      }
    }

    next();
  }

  return {
    name: 'course-api-plugin',
    transformIndexHtml(html: string) {
      const helper = getIndexHelper();
      const manifest = helper.getManifest();
      const manifestScript =
        typeof helper.getSafeManifestHtmlScript === 'function'
          ? helper.getSafeManifestHtmlScript(manifest)
          : `<script id="course-manifest" type="application/json">${JSON.stringify(manifest).replace(/</g, '\\u003c')}</script>`;

      if (html.includes('<!--COURSE_MANIFEST-->')) {
        return html.replace('<!--COURSE_MANIFEST-->', manifestScript);
      }
      return html.replace('</head>', `    ${manifestScript}\n  </head>`);
    },
    generateBundle() {
      const helper = getIndexHelper();
      const manifest = helper.getManifest();

      // Emit SLIM manifest (< 10 KB, NO data field)
      this.emitFile({
        type: 'asset',
        fileName: 'api/courses.json',
        source: JSON.stringify(manifest),
      });

      // Emit individual courses MINIFIED (no null, 2)
      const coursesWithData = helper.getCoursesWithData();
      for (const c of coursesWithData) {
        if (c.status === 'valid' && c.data) {
          const minifiedData = JSON.stringify(c.data);
          this.emitFile({
            type: 'asset',
            fileName: `api/courses/${c.id}.json`,
            source: minifiedData,
          });
          this.emitFile({
            type: 'asset',
            fileName: `courses/${c.filename}`,
            source: minifiedData,
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
