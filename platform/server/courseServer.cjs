const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 5173;
const COURSES_DIR = path.resolve(__dirname, '../../courses');
const DIST_DIR = path.resolve(__dirname, '../dist');

function validateCourseJson(filePath, content) {
  const controlCharRegex = /[\x00-\x08\x0b\x0c\x0e-\x1f]/;
  if (controlCharRegex.test(content)) {
    return {
      valid: false,
      error: 'Contains unescaped control characters or corrupted LaTeX escapes',
    };
  }

  let parsed;
  try {
    parsed = JSON.parse(content);
  } catch (e) {
    return { valid: false, error: `Invalid JSON syntax: ${e.message}` };
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

function getCourseList() {
  if (!fs.existsSync(COURSES_DIR)) {
    return [];
  }

  const files = fs.readdirSync(COURSES_DIR).filter((f) => f.endsWith('.json'));
  const results = [];

  for (const file of files) {
    const fullPath = path.join(COURSES_DIR, file);
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
    } catch (err) {
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

const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.ttf': 'font/ttf',
};

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);

  if ((url.pathname === '/api/courses' || url.pathname === '/api/courses.json') && req.method === 'GET') {
    const courses = getCourseList();
    res.writeHead(200, {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    });
    res.end(JSON.stringify({ courses }));
    return;
  }

  if (url.pathname.startsWith('/api/courses/') && req.method === 'GET') {
    let requestedId = decodeURIComponent(url.pathname.replace('/api/courses/', ''));
    if (requestedId.endsWith('.json')) {
      requestedId = requestedId.slice(0, -5);
    }
    const courses = getCourseList();
    const found = courses.find((c) => c.id === requestedId || c.filename === requestedId || c.filename === `${requestedId}.json`);

    if (found && found.status === 'valid') {
      res.writeHead(200, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      });
      res.end(JSON.stringify(found.data));
      return;
    } else if (found && found.status === 'error') {
      res.writeHead(400, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      });
      res.end(JSON.stringify({ error: found.error_message }));
      return;
    } else {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Course not found' }));
      return;
    }
  }

  // Serve static dist files if available
  let filePath = path.join(DIST_DIR, url.pathname === '/' ? 'index.html' : url.pathname);
  if (!fs.existsSync(filePath)) {
    filePath = path.join(DIST_DIR, 'index.html');
  }

  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath);
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': contentType });
    fs.createReadStream(filePath).pipe(res);
  } else {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end('<h1>Platform API Running. Build frontend with npm run build.</h1>');
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`Course server running at http://127.0.0.1:${PORT}`);
});
