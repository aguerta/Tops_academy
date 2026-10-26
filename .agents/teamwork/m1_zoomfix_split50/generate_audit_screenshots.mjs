import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import http from 'node:http';
import { createRequire } from 'node:module';

const req = createRequire(path.resolve('platform/package.json'));
const katex = req('katex');
const ts = req('typescript');

function resolvePlaywright() {
  const localAppData = process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local');
  const userProfile = process.env.USERPROFILE || os.homedir();
  const npxCandidates = [
    path.join(localAppData, 'npm-cache', '_npx'),
    path.join(userProfile, 'AppData', 'Local', 'npm-cache', '_npx'),
    path.join(os.homedir(), 'AppData', 'Local', 'npm-cache', '_npx'),
  ];
  for (const npxDir of npxCandidates) {
    if (fs.existsSync(npxDir)) {
      for (const d of fs.readdirSync(npxDir)) {
        const candidate = path.join(npxDir, d, 'node_modules', 'playwright');
        if (fs.existsSync(candidate)) {
          const r = createRequire(path.join(candidate, 'package.json'));
          return r('playwright');
        }
      }
    }
  }
}

function resolveChromiumExecutable() {
  const localAppData = process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local');
  const userProfile = process.env.USERPROFILE || os.homedir();
  const candidates = [
    path.join(localAppData, 'ms-playwright'),
    path.join(userProfile, 'AppData', 'Local', 'ms-playwright'),
    path.join(os.homedir(), 'AppData', 'Local', 'ms-playwright'),
  ];
  for (const msDir of candidates) {
    if (fs.existsSync(msDir)) {
      for (const d of fs.readdirSync(msDir)) {
        if (d.startsWith('chromium-')) {
          const exePath = path.join(msDir, d, 'chrome-win64', 'chrome.exe');
          if (fs.existsSync(exePath)) return exePath;
        }
      }
    }
  }
}

// Compile MathText helper
const mathTextSrc = fs.readFileSync('platform/src/components/MathText.tsx', 'utf8');
const transpiled = ts.transpileModule(mathTextSrc, {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, jsx: ts.JsxEmit.React }
});
const m = { exports: {} };
const fn = new Function('module', 'exports', 'require', transpiled.outputText);
fn(m, m.exports, req);
const { splitMathAndProse } = m.exports;

function renderMathText(text) {
  if (!text) return '';
  const parts = [];
  let remaining = text;
  while (remaining.length > 0) {
    const blockStart = remaining.indexOf('$$');
    const inlineStart = remaining.indexOf('$');

    if (blockStart !== -1 && (inlineStart === -1 || blockStart <= inlineStart)) {
      if (blockStart > 0) parts.push({ type: 'text', content: remaining.slice(0, blockStart) });
      const blockEnd = remaining.indexOf('$$', blockStart + 2);
      if (blockEnd !== -1) {
        parts.push({ type: 'block-math', content: remaining.slice(blockStart + 2, blockEnd) });
        remaining = remaining.slice(blockEnd + 2);
      } else {
        parts.push({ type: 'text', content: remaining.slice(blockStart) });
        break;
      }
    } else if (inlineStart !== -1) {
      if (inlineStart > 0) parts.push({ type: 'text', content: remaining.slice(0, inlineStart) });
      const inlineEnd = remaining.indexOf('$', inlineStart + 1);
      if (inlineEnd !== -1) {
        const rawMath = remaining.slice(inlineStart + 1, inlineEnd);
        const subParts = splitMathAndProse(rawMath);
        for (const sp of subParts) parts.push(sp);
        remaining = remaining.slice(inlineEnd + 1);
      } else {
        parts.push({ type: 'text', content: remaining.slice(inlineStart) });
        break;
      }
    } else {
      parts.push({ type: 'text', content: remaining });
      break;
    }
  }

  return parts.map(p => {
    if (p.type === 'text') {
      return `<span class="inline break-words">${p.content}</span>`;
    }
    const displayMode = p.type === 'block-math';
    try {
      let html = katex.renderToString(p.content, { throwOnError: false, displayMode });
      if (!displayMode) html = html.replace(/\u00a0/g, ' ');
      return `<span class="${displayMode ? 'block my-2 overflow-x-auto text-center' : 'inline mx-0.5'}">${html}</span>`;
    } catch {
      return `<span class="text-red-500 font-mono">${p.content}</span>`;
    }
  }).join('');
}

const coursesConfig = [
  {
    id: 'saul_control_optimo',
    title: 'Saúl Control Óptimo',
    file: 'courses/saul_control_optimo.json',
    dir: 'audit_screenshots/saul_control_optimo'
  },
  {
    id: 'asyntotic_estatistics',
    title: 'Asyntotic Estatistics',
    file: 'courses/asyntotic_estatistics_v7.json',
    dir: 'audit_screenshots/asyntotic_estatistics'
  },
  {
    id: 'estadistica_v2_cano',
    title: 'Estadística Versión 2 (Cano)',
    file: 'courses/estadistica_3_pre_parcial_v2.json',
    dir: 'audit_screenshots/estadistica_v2_cano'
  },
  {
    id: 'gavilano',
    title: 'Gavilano Pre-Parcial',
    file: 'courses/gavilano_pre_parcial.json',
    dir: 'audit_screenshots/gavilano'
  }
];

// Seeded PRNG for reproducible random selection
function createPrng(seed = 123456789) {
  let s = seed;
  return function() {
    s = (s * 1664525 + 1013904223) % 4294967296;
    return s / 4294967296;
  };
}

// Select 50 random questions per course
function selectQuestions(courseData, count = 50, seed = 42) {
  const prng = createPrng(seed);
  const questions = courseData.questions || [];
  // Shuffle copy
  const shuffled = [...questions];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(prng() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled.slice(0, count);
}

function buildQuestionCardHtml(courseTitle, question, qNum, totalCount) {
  const options = question.options || [];
  const mcqRowCount = Math.ceil(options.length / 2);
  const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'];

  return `
    <div class="h-dvh flex flex-col justify-between bg-[#f8fafc] text-gray-900 font-sans p-3 sm:p-4 box-border">
      <!-- Header bar -->
      <header class="h-11 bg-white border border-gray-200 rounded-xl px-4 flex items-center justify-between shrink-0 shadow-xs mb-3">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold text-gray-700">${courseTitle}</span>
          <span class="text-xs text-gray-400">|</span>
          <span class="text-xs text-ka-blue font-medium">Pregunta ${qNum} de ${totalCount} (ID: ${question.id || 'N/A'})</span>
        </div>
        <div class="text-[11px] font-mono text-gray-400">${question.type}</div>
      </header>

      <!-- Main Question Shell -->
      <main class="flex-1 min-h-0 flex flex-col">
        <div class="qc-root bg-white rounded-xl border border-gray-200 p-4 sm:p-5 flex flex-col flex-1 shadow-xs overflow-hidden">
          <!-- Question Stem -->
          <div class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Enunciado</div>
          <h2 class="qc-stem text-gray-900 font-normal leading-relaxed mb-4" style="font-size: var(--qc-font, 0.9375rem);">
            ${renderMathText(question.stem)}
          </h2>

          <!-- Choose prompt -->
          <div class="text-xs font-semibold text-gray-500 mb-2">Choose 1 answer:</div>

          <!-- Options Grid -->
          <div class="qc-options-scroll flex-1 min-h-0">
            <div class="qc-options" style="--qc-rows: ${mcqRowCount}; --rows: ${mcqRowCount};">
              ${options.map((opt, idx) => `
                <div class="option-item qc-option-item w-full min-w-0 text-left rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center transition-all">
                  <div class="qc-badge rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 border border-gray-300 text-gray-600 bg-gray-50">
                    ${letters[idx] || String.fromCharCode(65 + idx)}
                  </div>
                  <div class="flex-1 min-w-0 text-gray-900" style="font-size: var(--qc-font, 0.9375rem);">
                    ${renderMathText(opt.content)}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- Stuck hint line -->
          <div class="mt-3 pt-2 border-t border-gray-100 flex items-center gap-1.5 text-xs text-ka-blue font-medium shrink-0">
            <span>💡</span>
            <span>Stuck? Review related articles/videos or use a hint.</span>
          </div>
        </div>
      </main>

      <!-- Footer Bar -->
      <footer class="h-12 bg-white border border-gray-200 rounded-xl px-4 flex items-center justify-between shrink-0 shadow-xs mt-3">
        <div class="flex items-center gap-2">
          <div class="w-3.5 h-3.5 rounded-full border-2 border-gray-300"></div>
          <span class="text-xs text-gray-500 font-medium">Do 50 problems</span>
        </div>
        <div class="flex items-center gap-2">
          <button class="px-3.5 py-1 text-xs font-medium text-gray-600 rounded-md border border-gray-200 hover:bg-gray-50">Skip</button>
          <button class="px-4 py-1 text-xs font-semibold bg-ka-blue text-white rounded-md hover:bg-blue-700 shadow-xs">Check</button>
        </div>
      </footer>
    </div>
  `;
}

async function main() {
  console.log('Starting screenshot generation for 50 random questions across 4 courses (200 total)...');
  const startTime = Date.now();

  // Create output directories
  for (const c of coursesConfig) {
    if (!fs.existsSync(c.dir)) {
      fs.mkdirSync(c.dir, { recursive: true });
    }
  }

  // Find css bundle in platform/dist/assets
  const distAssetsDir = path.resolve('platform/dist/assets');
  const cssFiles = fs.readdirSync(distAssetsDir).filter(f => f.endsWith('.css'));
  if (cssFiles.length === 0) throw new Error('No CSS bundle found in platform/dist/assets. Run npm run build first.');
  const cssBundleName = cssFiles[0];

  // Start tiny HTTP server to serve dist assets (fonts, css) and dynamic question pages
  let currentHtml = '';
  const server = http.createServer((req, res) => {
    if (req.url === '/' || req.url === '/index.html') {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(currentHtml);
    } else if (req.url.startsWith('/assets/')) {
      const assetPath = path.join(distAssetsDir, req.url.replace('/assets/', ''));
      if (fs.existsSync(assetPath)) {
        const ext = path.extname(assetPath);
        const mimeTypes = {
          '.css': 'text/css',
          '.woff2': 'font/woff2',
          '.woff': 'font/woff',
          '.ttf': 'font/ttf',
          '.js': 'text/javascript'
        };
        res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
        fs.createReadStream(assetPath).pipe(res);
      } else {
        res.writeHead(404);
        res.end();
      }
    } else {
      res.writeHead(404);
      res.end();
    }
  });

  const port = 49152 + Math.floor(Math.random() * 1000);
  await new Promise(resolve => server.listen(port, '127.0.0.1', resolve));
  console.log(`Asset server running on http://127.0.0.1:${port}`);

  const { chromium } = resolvePlaywright();
  const exePath = resolveChromiumExecutable();

  const browser = await chromium.launch({
    headless: true,
    executablePath: exePath,
    ignoreDefaultArgs: ['--hide-scrollbars']
  });

  // 14" laptop 50% split view viewport (standard laptop testing: 683x768)
  const context = await browser.newContext({
    viewport: { width: 683, height: 768 }
  });
  const page = await context.newPage();

  const galleryItems = [];

  for (let cIdx = 0; cIdx < coursesConfig.length; cIdx++) {
    const config = coursesConfig[cIdx];
    console.log(`\nProcessing [${cIdx + 1}/4]: ${config.title}...`);
    const rawData = JSON.parse(fs.readFileSync(config.file, 'utf8'));
    const selected = selectQuestions(rawData, 50, 1000 + cIdx * 777);

    for (let qIdx = 0; qIdx < selected.length; qIdx++) {
      const q = selected[qIdx];
      const qNum = String(qIdx + 1).padStart(2, '0');
      const safeId = (q.id || `q${qIdx + 1}`).replace(/[^a-zA-Z0-9_-]/g, '_');
      const filename = `q${qNum}_${safeId}.png`;
      const screenshotPath = path.join(config.dir, filename);

      const bodyContent = buildQuestionCardHtml(config.title, q, qIdx + 1, selected.length);

      currentHtml = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="/assets/${cssBundleName}">
  <style>
    /* Ensure container query root is active */
    .qc-root {
      container-type: inline-size;
      container-name: qc;
    }
  </style>
</head>
<body class="m-0 p-0 overflow-hidden bg-slate-100">
  ${bodyContent}
</body>
</html>`;

      await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: 'domcontentloaded' });
      // Small tick for layout & KaTeX font calculation
      await page.waitForTimeout(40);

      await page.screenshot({ path: screenshotPath });

      galleryItems.push({
        courseId: config.id,
        courseTitle: config.title,
        qNum: qIdx + 1,
        id: q.id,
        type: q.type,
        stemSnippet: (q.stem || '').slice(0, 100),
        relPath: `${config.id}/${filename}`
      });

      if ((qIdx + 1) % 10 === 0) {
        process.stdout.write(`  Captured ${qIdx + 1}/50 screenshots...\n`);
      }
    }
  }

  await browser.close();
  server.close();

  // Generate interactive HTML gallery index.html
  const galleryHtml = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Auditoría Visual - 200 Screenshots (50 por Curso)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
    h1 { font-size: 24px; font-weight: 700; margin-bottom: 8px; color: #38bdf8; }
    .subtitle { font-size: 14px; color: #94a3b8; margin-bottom: 24px; }
    .filters { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; position: sticky; top: 0; background: #0f172a; padding: 10px 0; z-index: 10; border-bottom: 1px solid #1e293b; }
    .filter-btn { background: #1e293b; color: #cbd5e1; border: 1px solid #334155; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 500; transition: all 0.15s; }
    .filter-btn:hover { background: #334155; color: #fff; }
    .filter-btn.active { background: #0284c7; color: #fff; border-color: #38bdf8; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }
    .card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; overflow: hidden; display: flex; flex-col; transition: transform 0.2s; }
    .card:hover { transform: translateY(-2px); border-color: #38bdf8; }
    .thumb { width: 100%; aspect-ratio: 683 / 768; object-fit: cover; background: #fff; cursor: pointer; border-bottom: 1px solid #334155; }
    .card-body { padding: 12px; font-size: 12px; }
    .badge { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 600; text-transform: uppercase; background: #334155; color: #38bdf8; margin-bottom: 6px; }
    .card-title { font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    .card-stem { color: #94a3b8; font-size: 11px; max-height: 2.8em; overflow: hidden; text-overflow: ellipsis; }

    /* Modal */
    .modal { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 100; align-items: center; justify-content: center; padding: 20px; }
    .modal.open { display: flex; }
    .modal-img { max-width: 90vw; max-height: 90vh; border-radius: 8px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); }
    .modal-close { position: absolute; top: 20px; right: 24px; color: #fff; font-size: 32px; font-weight: bold; cursor: pointer; }
  </style>
</head>
<body>
  <h1>🔍 Auditoría Visual de Preguntas (200 Screenshots)</h1>
  <div class="subtitle">50 preguntas aleatorias de Saúl Control Óptimo, Asyntotic Estatistics, Estadística v2 (Cano) y Gavilano. Viewport: 683×768 (Laptop 14" Split 50%).</div>

  <div class="filters">
    <button class="filter-btn active" onclick="filterCourse('all')">Todos (200)</button>
    <button class="filter-btn" onclick="filterCourse('saul_control_optimo')">Saúl Control Óptimo (50)</button>
    <button class="filter-btn" onclick="filterCourse('asyntotic_estatistics')">Asyntotic Estatistics (50)</button>
    <button class="filter-btn" onclick="filterCourse('estadistica_v2_cano')">Estadística v2 Cano (50)</button>
    <button class="filter-btn" onclick="filterCourse('gavilano')">Gavilano (50)</button>
  </div>

  <div class="grid" id="grid">
    ${galleryItems.map(item => `
      <div class="card" data-course="${item.courseId}">
        <img class="thumb" src="${item.relPath}" alt="${item.courseTitle}" onclick="openModal('${item.relPath}')" loading="lazy">
        <div class="card-body">
          <span class="badge">${item.courseTitle} #${item.qNum}</span>
          <div class="card-title">ID: ${item.id}</div>
          <div class="card-stem">${item.stemSnippet}...</div>
        </div>
      </div>
    `).join('')}
  </div>

  <div class="modal" id="modal" onclick="closeModal()">
    <span class="modal-close">&times;</span>
    <img class="modal-img" id="modal-img" src="" alt="Full view">
  </div>

  <script>
    function filterCourse(id) {
      document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');
      document.querySelectorAll('.card').forEach(card => {
        if (id === 'all' || card.getAttribute('data-course') === id) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }
    function openModal(src) {
      const modal = document.getElementById('modal');
      const img = document.getElementById('modal-img');
      img.src = src;
      modal.classList.add('open');
    }
    function closeModal() {
      document.getElementById('modal').classList.remove('open');
    }
  </script>
</body>
</html>`;

  fs.writeFileSync('audit_screenshots/index.html', galleryHtml);

  const durationSec = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`\n✅ Generated 200 screenshots in ${durationSec}s!`);
  console.log(`Directory: ${path.resolve('audit_screenshots')}`);
  console.log(`Gallery index: ${path.resolve('audit_screenshots/index.html')}`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
