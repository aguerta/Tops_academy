const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const COURSES_DIR = path.resolve(__dirname, '../../courses');
const CACHE_FILE = path.resolve(__dirname, '../.cache/course_index.json');

// Telemetry and profiling stats
const stats = {
  parseCount: 0,
  cachedHits: 0,
  lastBuildDurationMs: 0,
};

let cachedIndex = null;

/**
 * Validates course JSON structure and checks for corrupted control characters.
 * Matches existing platform validation semantics.
 */
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

/**
 * Generates an ETag string based on file size and modification time.
 */
function computeEtag(size, mtimeMs) {
  return `"${size.toString(16)}-${Math.floor(mtimeMs).toString(16)}"`;
}

/**
 * Loads cached index from disk if available.
 */
function loadDiskCache(cacheFilePath = CACHE_FILE) {
  try {
    if (fs.existsSync(cacheFilePath)) {
      const raw = fs.readFileSync(cacheFilePath, 'utf-8');
      const parsed = JSON.parse(raw);
      if (parsed && parsed.version === 1 && typeof parsed.entries === 'object') {
        return parsed;
      }
    }
  } catch (err) {
    // Disk cache corrupted or unreadable; fallback to empty cache
  }
  return null;
}

/**
 * Persists index to disk cache.
 */
function saveDiskCache(indexData, cacheFilePath = CACHE_FILE) {
  try {
    const cacheDir = path.dirname(cacheFilePath);
    if (!fs.existsSync(cacheDir)) {
      fs.mkdirSync(cacheDir, { recursive: true });
    }
    const tempFile = `${cacheFilePath}.${Date.now()}.tmp`;
    fs.writeFileSync(tempFile, JSON.stringify(indexData, null, 2), 'utf-8');
    fs.renameSync(tempFile, cacheFilePath);
  } catch (err) {
    try {
      fs.writeFileSync(cacheFilePath, JSON.stringify(indexData, null, 2), 'utf-8');
    } catch (writeErr) {
      // Non-fatal: disk cache failed to save, index remains in memory
    }
  }
}

/**
 * Builds or refreshes the course index.
 * Revalidates only files whose size or mtimeMs changed.
 */
function buildIndex(options = {}) {
  const startTime = Date.now();
  const force = options.force === true;
  const coursesDir = options.coursesDir || COURSES_DIR;
  const cacheFile = options.cacheFile || CACHE_FILE;

  let diskCache = force ? null : loadDiskCache(cacheFile);
  const entries = diskCache ? { ...diskCache.entries } : {};

  if (!fs.existsSync(coursesDir)) {
    cachedIndex = {
      version: 1,
      generated_at: new Date().toISOString(),
      entries: {},
    };
    stats.lastBuildDurationMs = Date.now() - startTime;
    return cachedIndex;
  }

  const files = fs.readdirSync(coursesDir).filter((f) => f.endsWith('.json'));
  const currentFilenames = new Set(files);

  for (const file of files) {
    const fullPath = path.join(coursesDir, file);
    try {
      const fileStat = fs.statSync(fullPath);
      const cached = entries[file];

      if (
        !force &&
        cached &&
        cached.mtimeMs === fileStat.mtimeMs &&
        cached.size === fileStat.size
      ) {
        // Cache hit: reuse cached validation and metadata
        stats.cachedHits++;
        continue;
      }

      // Cache miss: read, validate, and parse
      stats.parseCount++;
      const raw = fs.readFileSync(fullPath, 'utf-8');
      const check = validateCourseJson(fullPath, raw);
      const etag = computeEtag(fileStat.size, fileStat.mtimeMs);

      if (check.valid && check.data) {
        entries[file] = {
          id: check.data.course_id,
          filename: file,
          title: check.data.title,
          description: check.data.description || '',
          status: 'valid',
          total_competencies: check.data.competencies.length,
          total_questions: check.data.questions.length,
          bytes: fileStat.size,
          etag,
          error_message: null,
          mtimeMs: fileStat.mtimeMs,
          size: fileStat.size,
        };
      } else {
        let fallbackTitle = file.replace('.json', '');
        try {
          const partial = JSON.parse(raw);
          if (partial.title) fallbackTitle = partial.title;
        } catch {}

        entries[file] = {
          id: file.replace('.json', ''),
          filename: file,
          title: fallbackTitle,
          description: 'Corrupted or malformed course file',
          status: 'error',
          total_competencies: 0,
          total_questions: 0,
          bytes: fileStat.size,
          etag,
          error_message: check.error || 'Validation failed',
          mtimeMs: fileStat.mtimeMs,
          size: fileStat.size,
        };
      }
    } catch (err) {
      stats.parseCount++;
      const etag = `"${Date.now().toString(16)}"`;
      entries[file] = {
        id: file.replace('.json', ''),
        filename: file,
        title: file,
        description: 'Error reading course file',
        status: 'error',
        total_competencies: 0,
        total_questions: 0,
        bytes: 0,
        etag,
        error_message: err.message,
        mtimeMs: 0,
        size: 0,
      };
    }
  }

  // Remove entries for deleted course files
  for (const filename of Object.keys(entries)) {
    if (!currentFilenames.has(filename)) {
      delete entries[filename];
    }
  }

  const newIndex = {
    version: 1,
    generated_at: new Date().toISOString(),
    entries,
  };

  saveDiskCache(newIndex, cacheFile);
  cachedIndex = newIndex;
  stats.lastBuildDurationMs = Date.now() - startTime;

  return cachedIndex;
}

/**
 * Ensures that the in-memory course index is initialized.
 */
function ensureIndex() {
  if (!cachedIndex) {
    buildIndex();
  }
  return cachedIndex;
}

/**
 * Finds a course entry in the index by course id or filename.
 */
function findEntry(id) {
  ensureIndex();
  if (!id) return null;
  const decoded = decodeURIComponent(id).trim();
  const baseName = decoded.endsWith('.json') ? decoded.slice(0, -5) : decoded;

  const entries = Object.values(cachedIndex.entries);

  // 1. Direct match on course id
  for (const entry of entries) {
    if (entry.id === decoded || entry.id === baseName) {
      return entry;
    }
  }

  // 2. Match on filename
  for (const entry of entries) {
    if (
      entry.filename === decoded ||
      entry.filename === `${baseName}.json` ||
      entry.filename === `${decoded}.json`
    ) {
      return entry;
    }
  }

  return null;
}

/**
 * Returns the slim manifest without the 'data' field.
 * Schema: { generated_at, courses: [ { id, filename, title, description, status, total_competencies, total_questions, bytes, etag, error_message } ] }
 */
function getManifest() {
  ensureIndex();

  const courses = Object.values(cachedIndex.entries).map((entry) => ({
    id: entry.id,
    filename: entry.filename,
    title: entry.title,
    description: entry.description,
    status: entry.status,
    total_competencies: entry.total_competencies,
    total_questions: entry.total_questions,
    bytes: entry.bytes,
    etag: entry.etag,
    error_message: entry.error_message,
  }));

  // Sort deterministically by filename
  courses.sort((a, b) => a.filename.localeCompare(b.filename));

  return {
    generated_at: cachedIndex.generated_at,
    courses,
  };
}

/**
 * Computes an ETag for the manifest payload.
 */
function getManifestEtag() {
  const manifest = getManifest();
  const hash = crypto
    .createHash('md5')
    .update(JSON.stringify(manifest.courses))
    .digest('hex')
    .slice(0, 16);
  return `"${hash}"`;
}

/**
 * Returns the absolute path to the course JSON file on disk, or null if not found.
 */
function getCoursePath(id) {
  ensureIndex();
  const entry = findEntry(id);
  if (!entry) return null;
  return path.join(COURSES_DIR, entry.filename);
}

/**
 * Retrieves a single course's parsed data, etag, status, and error_message.
 */
function getCourseData(id) {
  ensureIndex();
  const entry = findEntry(id);
  if (!entry) return null;

  if (entry.status !== 'valid') {
    return {
      data: null,
      etag: entry.etag,
      status: entry.status,
      error_message: entry.error_message,
    };
  }

  const filePath = path.join(COURSES_DIR, entry.filename);
  try {
    const raw = fs.readFileSync(filePath, 'utf-8');
    const data = JSON.parse(raw);
    return {
      data,
      etag: entry.etag,
      status: 'valid',
      error_message: null,
    };
  } catch (err) {
    return {
      data: null,
      etag: entry.etag,
      status: 'error',
      error_message: err.message,
    };
  }
}

/**
 * Retrieves a single course's raw string content, etag, status, and error_message.
 * Efficiently streams or serves raw file without reparsing.
 */
function getCourseRaw(id) {
  ensureIndex();
  const entry = findEntry(id);
  if (!entry) return null;

  const filePath = path.join(COURSES_DIR, entry.filename);
  try {
    const raw = fs.readFileSync(filePath, 'utf-8');
    return {
      raw,
      etag: entry.etag,
      status: entry.status,
      error_message: entry.error_message,
      filePath,
    };
  } catch (err) {
    return {
      raw: null,
      etag: entry.etag,
      status: 'error',
      error_message: err.message,
      filePath,
    };
  }
}

/**
 * Generates an inline <script> tag for index.html containing the manifest JSON.
 * Escapes '</script>' and '<!--' safely to prevent script breakout or HTML parser confusion.
 */
function getSafeManifestHtmlScript(manifest) {
  const data = manifest !== undefined ? manifest : getManifest();
  const raw = typeof data === 'string' ? data : JSON.stringify(data);

  // Escaping:
  // - '</script' is replaced with '<\/script' (\/ is valid in JSON standard)
  // - '<!--' is replaced with '\u003c!--' (\u003c is valid in JSON standard and decodes to <)
  // Also replace literal '<\\!--' if present to guarantee no '<!--' sequences exist in script
  const safe = raw
    .replace(/<\/script/gi, '<\\/script')
    .replace(/<!--/g, '\\u003c!--');

  return `<script id="course-manifest" type="application/json">${safe}</script>`;
}

/**
 * Returns profiling and test stats.
 */
function getStats() {
  return { ...stats };
}

/**
 * Resets profiling and test stats.
 */
function resetStats() {
  stats.parseCount = 0;
  stats.cachedHits = 0;
  stats.lastBuildDurationMs = 0;
}

/**
 * Invalidates in-memory and disk caches.
 */
function invalidateCache(cacheFilePath = CACHE_FILE) {
  cachedIndex = null;
  try {
    if (fs.existsSync(cacheFilePath)) {
      fs.unlinkSync(cacheFilePath);
    }
  } catch (err) {}
}

module.exports = {
  COURSES_DIR,
  CACHE_FILE,
  validateCourseJson,
  computeEtag,
  buildIndex,
  getManifest,
  getManifestEtag,
  getCoursePath,
  getCourseData,
  getCourseRaw,
  getSafeManifestHtmlScript,
  getStats,
  resetStats,
  invalidateCache,
};
