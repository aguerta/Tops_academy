const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');
const courseIndex = require('./courseIndex.cjs');

const PORT = process.env.PORT !== undefined ? parseInt(process.env.PORT, 10) : 5173;
const COURSES_DIR = courseIndex.COURSES_DIR;
const DIST_DIR = path.resolve(__dirname, '../dist');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.ttf': 'font/ttf',
  '.ico': 'image/x-icon',
  '.webmanifest': 'application/manifest+json',
};

/**
 * Checks if the client accepts gzip compression.
 */
function canGzip(req) {
  const accept = req.headers['accept-encoding'] || '';
  return /\bgzip\b/i.test(accept);
}

/**
 * Checks if the client's If-None-Match header matches the resource ETag.
 */
function isFresh(req, etag) {
  if (!etag) return false;
  const ifNoneMatch = req.headers['if-none-match'];
  if (!ifNoneMatch) return false;
  if (ifNoneMatch === '*') return true;

  const clientEtags = ifNoneMatch
    .split(',')
    .map((s) => s.trim().replace(/^W\//, ''));
  const currentClean = etag.replace(/^W\//, '').trim();
  return clientEtags.includes(currentClean);
}

/**
 * Serves the HTML document with inline manifest injection and caching headers.
 */
function serveIndexHtml(req, res) {
  const indexPath = path.join(DIST_DIR, 'index.html');
  if (!fs.existsSync(indexPath)) {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<h1>Platform API Running. Build frontend with npm run build.</h1>');
    return;
  }

  let html;
  try {
    html = fs.readFileSync(indexPath, 'utf-8');
  } catch (err) {
    res.writeHead(500, { 'Content-Type': 'text/plain' });
    res.end('Error reading index.html');
    return;
  }

  // Inject manifest script inline into index.html
  const scriptTag = courseIndex.getSafeManifestHtmlScript();
  if (html.includes('<!--COURSE_MANIFEST-->')) {
    html = html.replace('<!--COURSE_MANIFEST-->', scriptTag);
  } else if (html.includes('</head>')) {
    html = html.replace('</head>', `  ${scriptTag}\n</head>`);
  } else if (html.includes('<div id="root">')) {
    html = html.replace('<div id="root">', `${scriptTag}\n    <div id="root">`);
  } else {
    html = html + scriptTag;
  }

  const etag = '"' + crypto.createHash('md5').update(html).digest('hex').slice(0, 16) + '"';

  if (isFresh(req, etag)) {
    res.writeHead(304, {
      'ETag': etag,
      'Cache-Control': 'no-cache',
      'Vary': 'Accept-Encoding',
    });
    res.end();
    return;
  }

  const headers = {
    'Content-Type': 'text/html; charset=utf-8',
    'ETag': etag,
    'Cache-Control': 'no-cache',
    'Vary': 'Accept-Encoding',
  };

  if (canGzip(req)) {
    headers['Content-Encoding'] = 'gzip';
    res.writeHead(200, headers);
    const gzip = zlib.createGzip();
    gzip.pipe(res);
    gzip.end(Buffer.from(html, 'utf-8'));
  } else {
    headers['Content-Length'] = Buffer.byteLength(html, 'utf-8');
    res.writeHead(200, headers);
    res.end(html);
  }
}

/**
 * Serves static dist files with appropriate MIME types, caching, and gzip compression.
 */
function serveStaticFile(req, res, filePath) {
  let stat;
  try {
    stat = fs.statSync(filePath);
    if (!stat.isFile()) {
      serveIndexHtml(req, res);
      return;
    }
  } catch (err) {
    serveIndexHtml(req, res);
    return;
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';
  const etag = courseIndex.computeEtag(stat.size, stat.mtimeMs);

  const isHashedAsset = filePath.includes(path.sep + 'assets' + path.sep) || filePath.includes('/assets/');
  const cacheControl = isHashedAsset
    ? 'public, max-age=31536000, immutable'
    : 'public, max-age=3600';

  if (isFresh(req, etag)) {
    res.writeHead(304, {
      'ETag': etag,
      'Cache-Control': cacheControl,
      'Vary': 'Accept-Encoding',
    });
    res.end();
    return;
  }

  const isCompressible = ['.js', '.mjs', '.css', '.json', '.svg', '.html'].includes(ext);
  const headers = {
    'Content-Type': contentType,
    'ETag': etag,
    'Cache-Control': cacheControl,
    'Vary': 'Accept-Encoding',
  };

  if (isCompressible && canGzip(req)) {
    headers['Content-Encoding'] = 'gzip';
    res.writeHead(200, headers);
    const gzip = zlib.createGzip();
    fs.createReadStream(filePath).pipe(gzip).pipe(res);
  } else {
    headers['Content-Length'] = stat.size;
    res.writeHead(200, headers);
    fs.createReadStream(filePath).pipe(res);
  }
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);

  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, If-None-Match, Accept-Encoding',
    });
    res.end();
    return;
  }

  // Health check endpoint for uptime and index status
  if (url.pathname === '/healthz' && req.method === 'GET') {
    res.writeHead(200, {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'no-cache',
    });
    res.end(
      JSON.stringify({
        status: 'ok',
        pid: process.pid,
        uptime_seconds: Math.floor(process.uptime()),
        index_version: 1,
        courses_count: courseIndex.getManifest().courses.length,
        stats: courseIndex.getStats(),
      })
    );
    return;
  }

  // Manifest endpoint: returns SLIM manifest (< 50 KB) without 'data' field
  if (
    (url.pathname === '/api/courses' || url.pathname === '/api/courses.json') &&
    req.method === 'GET'
  ) {
    const manifest = courseIndex.getManifest();
    const etag = courseIndex.getManifestEtag();

    if (isFresh(req, etag)) {
      res.writeHead(304, {
        'ETag': etag,
        'Access-Control-Allow-Origin': '*',
        'Vary': 'Accept-Encoding',
      });
      res.end();
      return;
    }

    const payload = JSON.stringify(manifest);
    const headers = {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'ETag': etag,
      'Cache-Control': 'no-cache',
      'Vary': 'Accept-Encoding',
    };

    if (canGzip(req)) {
      headers['Content-Encoding'] = 'gzip';
      res.writeHead(200, headers);
      const gzip = zlib.createGzip();
      gzip.pipe(res);
      gzip.end(Buffer.from(payload, 'utf-8'));
    } else {
      headers['Content-Length'] = Buffer.byteLength(payload, 'utf-8');
      res.writeHead(200, headers);
      res.end(payload);
    }
    return;
  }

  // Detail endpoint: returns single course with ETag, 304, and gzip streaming
  if (url.pathname.startsWith('/api/courses/') && req.method === 'GET') {
    let requestedId = decodeURIComponent(url.pathname.replace('/api/courses/', ''));
    if (requestedId.endsWith('.json')) {
      requestedId = requestedId.slice(0, -5);
    }

    const rawCourse = courseIndex.getCourseRaw(requestedId);
    if (!rawCourse) {
      res.writeHead(404, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      });
      res.end(JSON.stringify({ error: 'Course not found' }));
      return;
    }

    if (rawCourse.status === 'error') {
      res.writeHead(400, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      });
      res.end(JSON.stringify({ error: rawCourse.error_message || 'Validation failed' }));
      return;
    }

    // Check ETag freshness (304 Not Modified)
    if (isFresh(req, rawCourse.etag)) {
      res.writeHead(304, {
        'ETag': rawCourse.etag,
        'Access-Control-Allow-Origin': '*',
        'Vary': 'Accept-Encoding',
      });
      res.end();
      return;
    }

    const headers = {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'ETag': rawCourse.etag,
      'Cache-Control': 'public, max-age=3600, must-revalidate',
      'Vary': 'Accept-Encoding',
    };

    if (canGzip(req)) {
      headers['Content-Encoding'] = 'gzip';
      res.writeHead(200, headers);
      const gzip = zlib.createGzip({ level: zlib.constants.Z_BEST_SPEED });
      fs.createReadStream(rawCourse.filePath).pipe(gzip).pipe(res);
    } else {
      const stat = fs.statSync(rawCourse.filePath);
      headers['Content-Length'] = stat.size;
      res.writeHead(200, headers);
      fs.createReadStream(rawCourse.filePath).pipe(res);
    }
    return;
  }

  // Serve direct courses files if requested via /courses/...
  if (url.pathname.startsWith('/courses/') && req.method === 'GET') {
    const filename = path.basename(url.pathname);
    const directPath = path.join(COURSES_DIR, filename);
    if (fs.existsSync(directPath) && fs.statSync(directPath).isFile()) {
      serveStaticFile(req, res, directPath);
      return;
    }
  }

  // Serve static dist files if available
  if (url.pathname === '/' || url.pathname === '/index.html') {
    serveIndexHtml(req, res);
    return;
  }

  const staticFilePath = path.join(DIST_DIR, url.pathname);
  if (fs.existsSync(staticFilePath) && fs.statSync(staticFilePath).isFile()) {
    serveStaticFile(req, res, staticFilePath);
  } else {
    // SPA fallback: non-file routes fall back to index.html with inline manifest
    serveIndexHtml(req, res);
  }
});

// Server hardening
server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(
      `[CourseServer] Port ${PORT} is already in use (EADDRINUSE). Another instance may be running.`
    );
  } else {
    console.error('[CourseServer] Server error:', err);
  }
});

process.on('uncaughtException', (err) => {
  console.error('[CourseServer] Uncaught exception:', err);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('[CourseServer] Unhandled rejection:', reason);
});

server.keepAliveTimeout = 65000;
server.headersTimeout = 66000;

// Warm up index on startup
courseIndex.buildIndex();

server.listen(PORT, '127.0.0.1', () => {
  console.log(
    `[${new Date().toISOString()}] [PID ${process.pid}] Course server running at http://127.0.0.1:${PORT}`
  );
});

module.exports = {
  server,
  PORT,
  courseIndex,
};
