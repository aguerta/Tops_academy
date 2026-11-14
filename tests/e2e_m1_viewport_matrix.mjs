/**
 * E2E Viewport Matrix Verification Suite — Milestone 1 & 1-T: Split-View 50%, Laptop Zoom-Fix & Blank-First AC-CORE
 *
 * Hardened Dual-Mode Edition (Stream 2A):
 * 1. Non-trivial assertions:
 *    - Verifies MC7 questions have EXACTLY 7 options (no trivial pass on missing/corrupt options).
 *    - Verifies 4+3 column-first distribution by coordinates:
 *      * In 2-col mode: Col 1 has items 0..3 (4 items) vertically stacked, Col 2 has items 4..6 (3 items) vertically stacked.
 *      * In 1-col mode (mobile 390x844): all 7 items vertically stacked in a single column.
 * 2. Milestone 1-T Expanded Viewport Matrix (12 Viewports):
 *    - Standard & Split: 683x768, 720x900, 800x900, 960x1080, 1366x768, 1440x900, 390x844.
 *    - High-DPI Zoom & Tablets: 1280x590 (14" 150%), 610x590 (Split 14" 150%), 1536x740 (ASUS TUF 125%), 768x1024 (Tablet Portrait), 1024x768 (Tablet Landscape).
 * 3. Dual-Mode AC-CORE Verification:
 *    - Mode Blank-First: ON (Default):
 *      * Evocation curtain & lift button rendered; options hidden.
 *      * AC-CORE under curtain: no horizontal overflow, KaTeX within bounds, footer check-btn visible.
 *      * Enter key (or lift button) drops curtain and reveals exactly 7 options with 4+3 distribution.
 *      * Toast feedback non-occlusion and answered no-scroll.
 *    - Mode Blank-First: OFF (Standard):
 *      * Toggled via [data-testid="toggle-blank-first-btn"].
 *      * Curtain absent; 7 options rendered immediately.
 *      * AC-CORE validated: no horizontal scroll, KaTeX within bounds, footer check-btn visible, 4+3 distribution.
 * 4. Process lifecycle & port resilience:
 *    - Automatic free port detection with retries, Windows taskkill tree cleanup, global interruption handlers.
 */

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import net from 'node:net';
import { spawn, execSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');
const screensDir = path.resolve(projectRoot, '.agents/teamwork/m1_zoomfix_split50/screens');

// Timeouts
const SERVER_START_TIMEOUT = 15000;
const PAGE_NAV_TIMEOUT = 15000;
const SELECTOR_TIMEOUT = 12000;

// Ensure output screenshot directory exists
if (!fs.existsSync(screensDir)) {
  fs.mkdirSync(screensDir, { recursive: true });
}

/**
 * Dynamically resolves Playwright from standard modules or npx global cache across Windows paths.
 */
function resolvePlaywright() {
  try {
    const req = createRequire(import.meta.url);
    return req('playwright');
  } catch {}

  const localAppData = process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local');
  const userProfile = process.env.USERPROFILE || os.homedir();

  const npxCandidates = [
    path.join(localAppData, 'npm-cache', '_npx'),
    path.join(userProfile, 'AppData', 'Local', 'npm-cache', '_npx'),
    path.join(os.homedir(), 'AppData', 'Local', 'npm-cache', '_npx'),
  ];

  for (const npxDir of npxCandidates) {
    if (fs.existsSync(npxDir)) {
      const dirs = fs.readdirSync(npxDir);
      for (const d of dirs) {
        const candidate = path.join(npxDir, d, 'node_modules', 'playwright');
        if (fs.existsSync(candidate)) {
          const req = createRequire(path.join(candidate, 'package.json'));
          return req('playwright');
        }
      }
    }
  }

  throw new Error('Playwright not found in local node_modules or npx global cache.');
}

/**
 * Finds pre-installed Chromium executable in ms-playwright.
 */
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
      const dirs = fs.readdirSync(msDir);
      for (const d of dirs) {
        if (d.startsWith('chromium-')) {
          const exePath = path.join(msDir, d, 'chrome-win64', 'chrome.exe');
          if (fs.existsSync(exePath)) {
            return exePath;
          }
        }
      }
    }
  }
  return undefined;
}

/**
 * Kills process tree safely on Windows and POSIX.
 */
function killProcessTree(pid) {
  if (!pid) return;
  try {
    if (process.platform === 'win32') {
      execSync(`taskkill /pid ${pid} /T /F`, { stdio: 'ignore' });
    } else {
      process.kill(-pid, 'SIGKILL');
    }
  } catch (e) {
    try {
      process.kill(pid, 'SIGKILL');
    } catch {}
  }
}

/**
 * Finds a free TCP port.
 */
async function getFreePort() {
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.unref();
    srv.on('error', reject);
    srv.listen(0, '127.0.0.1', () => {
      const port = srv.address().port;
      srv.close((err) => {
        if (err) reject(err);
        else resolve(port);
      });
    });
  });
}

/**
 * Starts the courseServer in background with retry logic on port collision.
 */
async function startServerWithRetry(maxRetries = 3) {
  const platformDir = path.join(projectRoot, 'platform');
  const serverScript = path.join(platformDir, 'server', 'courseServer.cjs');

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const port = await getFreePort();
    console.log(`[E2E-Server] Attempt ${attempt}/${maxRetries}: Launching courseServer on http://127.0.0.1:${port}...`);

    let earlyExit = false;
    let exitError = null;

    const srv = spawn('node', [serverScript], {
      cwd: platformDir,
      env: { ...process.env, PORT: String(port) },
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    srv.stdout.on('data', (d) => {
      const msg = d.toString().trim();
      if (msg) console.log(`[Server] ${msg}`);
    });

    srv.stderr.on('data', (d) => {
      const msg = d.toString().trim();
      if (msg) console.error(`[Server-ERR] ${msg}`);
    });

    srv.on('error', (err) => {
      earlyExit = true;
      exitError = err;
    });

    srv.on('exit', (code) => {
      if (code !== 0) {
        earlyExit = true;
        exitError = new Error(`Server exited prematurely with code ${code}`);
      }
    });

    const baseUrl = `http://127.0.0.1:${port}`;
    let ready = false;
    const startTime = Date.now();

    while (Date.now() - startTime < SERVER_START_TIMEOUT) {
      if (earlyExit) break;
      try {
        const res = await fetch(`${baseUrl}/api/courses`);
        if (res.ok) {
          ready = true;
          break;
        }
      } catch {
        await new Promise((r) => setTimeout(r, 200));
      }
    }

    if (ready) {
      console.log(`[E2E-Server] courseServer is up and answering at ${baseUrl} (PID: ${srv.pid})`);
      return {
        baseUrl,
        pid: srv.pid,
        kill: () => killProcessTree(srv.pid),
      };
    }

    // Kill failed attempt
    killProcessTree(srv.pid);
    console.warn(`[E2E-Server] Attempt ${attempt} failed: ${exitError ? exitError.message : 'Timeout waiting for response'}.`);
    if (attempt === maxRetries) {
      throw new Error(`Failed to start courseServer after ${maxRetries} attempts.`);
    }
    await new Promise((r) => setTimeout(r, 500));
  }
}

// Global references for crash/interrupt cleanup
let globalServer = null;
let globalBrowser = null;

async function globalCleanup() {
  if (globalBrowser) {
    try {
      await globalBrowser.close();
    } catch {}
    globalBrowser = null;
  }
  if (globalServer) {
    try {
      globalServer.kill();
    } catch {}
    globalServer = null;
  }
}

process.on('SIGINT', async () => {
  console.log('\n[E2E-Suite] Received SIGINT. Running cleanup...');
  await globalCleanup();
  process.exit(130);
});

process.on('SIGTERM', async () => {
  console.log('\n[E2E-Suite] Received SIGTERM. Running cleanup...');
  await globalCleanup();
  process.exit(143);
});

process.on('uncaughtException', async (err) => {
  console.error('\n[E2E-Suite] Uncaught exception:', err);
  await globalCleanup();
  process.exit(1);
});

process.on('unhandledRejection', async (err) => {
  console.error('\n[E2E-Suite] Unhandled rejection:', err);
  await globalCleanup();
  process.exit(1);
});

/**
 * Non-trivial position validator for MC7 options.
 * Confirms exact 7 options in DOM and checks column-first (4+3) distribution.
 */
async function verifyMc7OptionPositions(page, expectColumns) {
  const options = await page.locator('[data-testid^="option-"]').all();
  if (options.length !== 7) {
    return {
      ok: false,
      count: options.length,
      actualColumns: 0,
      distribution: 'invalid-count',
      reason: `Expected exactly 7 options for MC7, found ${options.length}`,
    };
  }

  const boxes = [];
  for (let i = 0; i < 7; i++) {
    const box = await options[i].boundingBox();
    if (!box) {
      return {
        ok: false,
        count: 7,
        actualColumns: 0,
        distribution: 'null-box',
        reason: `Option ${i} bounding box is null`,
      };
    }
    boxes.push(box);
  }

  if (expectColumns === 2) {
    // Column 1: items 0, 1, 2, 3 (4 items)
    const col1X = boxes[0].x;
    for (let i = 0; i < 4; i++) {
      if (Math.abs(boxes[i].x - col1X) > 15) {
        return {
          ok: false,
          count: 7,
          actualColumns: 1,
          distribution: 'col1-x-deviated',
          reason: `Item ${i} in Col 1 has X=${boxes[i].x.toFixed(1)}, expected ~${col1X.toFixed(1)}`,
        };
      }
    }
    for (let i = 0; i < 3; i++) {
      if (boxes[i].y >= boxes[i + 1].y) {
        return {
          ok: false,
          count: 7,
          actualColumns: 2,
          distribution: 'col1-y-order-error',
          reason: `Item ${i} Y=${boxes[i].y} not strictly above Item ${i + 1} Y=${boxes[i + 1].y}`,
        };
      }
    }

    // Column 2: items 4, 5, 6 (3 items)
    const col2X = boxes[4].x;
    if (col2X <= col1X + 40) {
      return {
        ok: false,
        count: 7,
        actualColumns: 1,
        distribution: 'overlap-columns',
        reason: `Col 2 X=${col2X.toFixed(1)} not far enough right of Col 1 X=${col1X.toFixed(1)}`,
      };
    }
    for (let i = 4; i < 7; i++) {
      if (Math.abs(boxes[i].x - col2X) > 15) {
        return {
          ok: false,
          count: 7,
          actualColumns: 2,
          distribution: 'col2-x-deviated',
          reason: `Item ${i} in Col 2 has X=${boxes[i].x.toFixed(1)}, expected ~${col2X.toFixed(1)}`,
        };
      }
    }
    for (let i = 4; i < 6; i++) {
      if (boxes[i].y >= boxes[i + 1].y) {
        return {
          ok: false,
          count: 7,
          actualColumns: 2,
          distribution: 'col2-y-order-error',
          reason: `Item ${i} Y=${boxes[i].y} not strictly above Item ${i + 1} Y=${boxes[i + 1].y}`,
        };
      }
    }

    // Row 1 top alignment
    const row1Diff = Math.abs(boxes[0].y - boxes[4].y);
    if (row1Diff > 35) {
      return {
        ok: false,
        count: 7,
        actualColumns: 2,
        distribution: 'misaligned-row-1',
        reason: `Item 0 Y=${boxes[0].y} and Item 4 Y=${boxes[4].y} top alignment diff is ${row1Diff}px (> 35px)`,
      };
    }

    return {
      ok: true,
      count: 7,
      actualColumns: 2,
      distribution: '4 left + 3 right (column-first)',
      col1Count: 4,
      col2Count: 3,
      col1X,
      col2X,
    };
  } else {
    // expectColumns === 1 (Mobile view)
    const col1X = boxes[0].x;
    for (let i = 1; i < 7; i++) {
      if (Math.abs(boxes[i].x - col1X) > 15) {
        return {
          ok: false,
          count: 7,
          actualColumns: 2,
          distribution: 'not-single-column',
          reason: `Item ${i} X=${boxes[i].x.toFixed(1)} deviates from Col 1 X=${col1X.toFixed(1)}`,
        };
      }
    }
    for (let i = 0; i < 6; i++) {
      if (boxes[i].y >= boxes[i + 1].y) {
        return {
          ok: false,
          count: 7,
          actualColumns: 1,
          distribution: 'order-error',
          reason: `Item ${i} Y=${boxes[i].y} not strictly above Item ${i + 1} Y=${boxes[i + 1].y}`,
        };
      }
    }

    return {
      ok: true,
      count: 7,
      actualColumns: 1,
      distribution: '7 vertical single-column',
      col1Count: 7,
      col2Count: 0,
      col1X,
    };
  }
}

/**
 * Milestone 1 & Milestone 1-T Complete Viewport Matrix (12 Viewports)
 */
const VIEWPORT_MATRIX = [
  // Original Milestone 1
  { width: 683, height: 768, label: '683x768 (Split 50% 1366)', expectColumns: 2 },
  { width: 720, height: 900, label: '720x900 (Split 50% 1440)', expectColumns: 2 },
  { width: 800, height: 900, label: '800x900 (Split 50% 1600)', expectColumns: 2 },
  { width: 960, height: 1080, label: '960x1080 (Split 50% 1080p)', expectColumns: 2 },
  { width: 1366, height: 768, label: '1366x768 (Laptop HD Full)', expectColumns: 2 },
  { width: 1440, height: 900, label: '1440x900 (Desktop Full)', expectColumns: 2 },
  { width: 390, height: 844, label: '390x844 (Mobile Phone)', expectColumns: 1 },
  // Milestone 1-T: High-DPI Zoom 150%/125% & Tablets
  { width: 1280, height: 590, label: '1280x590 (Laptop 14" 150%)', expectColumns: 2 },
  { width: 610, height: 590, label: '610x590 (Split 50% 14" 150%)', expectColumns: 2 },
  { width: 1536, height: 740, label: '1536x740 (ASUS TUF 15.6" 125%)', expectColumns: 2 },
  { width: 768, height: 1024, label: '768x1024 (Tablet Portrait)', expectColumns: 2 },
  { width: 1024, height: 768, label: '1024x768 (Tablet Landscape)', expectColumns: 2 },
];

async function runMatrix() {
  console.log('================================================================');
  console.log(' STARTING MILESTONE 1-T VIEWPORT MATRIX E2E SUITE (DUAL-MODE)');
  console.log('================================================================\n');

  const pw = resolvePlaywright();
  const execPath = resolveChromiumExecutable();
  console.log(`[Playwright] Using Chromium executable: ${execPath || 'Default'}`);

  globalServer = await startServerWithRetry(3);
  const server = globalServer;

  const results = [];
  let allPassed = true;

  try {
    globalBrowser = await pw.chromium.launch({
      executablePath: execPath,
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });
    const browser = globalBrowser;

    for (const vp of VIEWPORT_MATRIX) {
      console.log(`\n----------------------------------------------------------------`);
      console.log(`Testing Viewport: ${vp.label} [${vp.width}x${vp.height}]`);
      console.log(`----------------------------------------------------------------`);

      const context = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
        deviceScaleFactor: 1,
      });

      const page = await context.newPage();
      page.setDefaultTimeout(SELECTOR_TIMEOUT);

      page.on('console', (msg) => {
        if (msg.type() === 'error') console.log(`[Browser Console Error] ${msg.text()}`);
      });
      page.on('pageerror', (err) => console.error(`[Browser Page Error] ${err.message}`));

      const testRecord = {
        viewport: `${vp.width}x${vp.height}`,
        label: vp.label,
        overviewScrollOk: false,
        sidebarBehaviorOk: false,
        // Mode 1: Blank-First: ON (Default state)
        bfOn: {
          curtainVisible: false,
          liftBtnVisible: false,
          optionsHiddenInitially: false,
          curtainScrollOk: false,
          curtainCheckBtnOk: false,
          curtainKatexOk: false,
          curtainLiftOk: false,
          optionsRevealedCount: 0,
          optionsDistributionOk: false,
          actualColumns: 0,
          distribution: '',
          toastFeedbackOk: false,
          actionButtonVisibleAfterToast: false,
          answeredScrollOk: false,
          passed: false,
        },
        // Mode 2: Blank-First: OFF (Standard mode)
        bfOff: {
          curtainHidden: false,
          optionsImmediateCount: 0,
          optionsImmediateOk: false,
          practiceScrollOk: false,
          checkButtonVisibleOk: false,
          katexOverflowOk: false,
          optionsDistributionOk: false,
          actualColumns: 0,
          distribution: '',
          passed: false,
        },
        passed: false,
        notes: [],
      };

      try {
        // 1. Load library and select course
        await page.goto(server.baseUrl, { waitUntil: 'domcontentloaded', timeout: PAGE_NAV_TIMEOUT });
        await page.waitForSelector('[data-testid="course-card"]', { timeout: SELECTOR_TIMEOUT });

        // Select Saul course or first available valid course
        const courseCards = page.locator('[data-testid="course-card"]');
        const saulCard = courseCards.filter({ hasText: 'Saul' }).first();
        if ((await saulCard.count()) > 0) {
          await saulCard.click();
        } else {
          await courseCards.first().click();
        }

        // Wait for CourseOverview
        await page.waitForSelector('[data-testid="completion-tracker-summary"]', { timeout: SELECTOR_TIMEOUT });
        await page.waitForTimeout(300); // Allow layout transition

        // 2. Overview checks: scrollWidth and Sidebar responsiveness
        const overviewMetrics = await page.evaluate(() => ({
          scrollWidth: document.documentElement.scrollWidth,
          innerWidth: window.innerWidth,
          bodyScrollWidth: document.body.scrollWidth,
        }));

        testRecord.overviewScrollOk =
          overviewMetrics.scrollWidth <= overviewMetrics.innerWidth &&
          overviewMetrics.bodyScrollWidth <= overviewMetrics.innerWidth;

        if (!testRecord.overviewScrollOk) {
          testRecord.notes.push(
            `Overview overflow: scrollWidth=${overviewMetrics.scrollWidth} > innerWidth=${overviewMetrics.innerWidth}`
          );
        }

        const isDesktop = vp.width >= 1024;
        const toggleButton = page.locator('[data-testid="sidebar-toggle"]');
        const sidebar = page.locator('[data-testid="sidebar"]');

        const toggleCount = await toggleButton.count();
        const toggleVisible = toggleCount > 0 ? await toggleButton.isVisible() : false;
        const sidebarBox = (await sidebar.count()) > 0 ? await sidebar.boundingBox() : null;

        if (isDesktop) {
          // Desktop: toggle must be hidden, sidebar must be static and taking layout flow
          testRecord.sidebarBehaviorOk = !toggleVisible && sidebarBox !== null && sidebarBox.width > 0;
          if (!testRecord.sidebarBehaviorOk) {
            testRecord.notes.push(`Desktop sidebar error: toggleVisible=${toggleVisible}`);
          }
        } else {
          // Mobile / Split < 1024px: toggle must be visible, sidebar must be off-canvas (not taking layout flow)
          const sidebarTakesFlow = sidebarBox !== null && sidebarBox.x >= 0 && sidebarBox.width > 100;
          testRecord.sidebarBehaviorOk = toggleVisible && !sidebarTakesFlow;
          if (!testRecord.sidebarBehaviorOk) {
            testRecord.notes.push(
              `Split/Mobile sidebar error: toggleVisible=${toggleVisible}, sidebarTakesFlow=${sidebarTakesFlow}`
            );
          }
        }

        // Screenshot: Overview
        const overviewShot = path.join(screensDir, `overview_${vp.width}x${vp.height}.png`);
        await page.screenshot({ path: overviewShot });

        // 3. Enter Practice Session (Blank-First: ON is active by default)
        const practiceBtn = page.locator('button[data-testid^="competency-"]').first();
        await practiceBtn.click();

        const startPracticeBtn = page.locator('[data-testid="start-practice-btn"]');
        try {
          await startPracticeBtn.waitFor({ state: 'visible', timeout: 5000 });
          await startPracticeBtn.click();
        } catch {
          // Direct to practice
        }

        // Wait for question card
        await page.waitForSelector('[data-testid="question-card"]', { timeout: SELECTOR_TIMEOUT });
        await page.waitForTimeout(300);

        // =================================================================
        // MODE 1: BLANK-FIRST: ON (AC-CORE + Evocation Curtain Flow)
        // =================================================================

        // 3.1 Verify Curtain & Lift Button visibility, options hidden initially
        const curtain = page.locator('[data-testid="blank-first-curtain"]');
        const liftBtn = page.locator('[data-testid="lift-curtain-btn"]');
        await curtain.waitFor({ state: 'visible', timeout: 5000 });
        await liftBtn.waitFor({ state: 'visible', timeout: 5000 });

        testRecord.bfOn.curtainVisible = await curtain.isVisible();
        testRecord.bfOn.liftBtnVisible = await liftBtn.isVisible();
        const initialOptionsCount = await page.locator('[data-testid^="option-"]').count();
        testRecord.bfOn.optionsHiddenInitially = initialOptionsCount === 0;

        if (!testRecord.bfOn.curtainVisible || !testRecord.bfOn.liftBtnVisible || !testRecord.bfOn.optionsHiddenInitially) {
          testRecord.notes.push(
            `BF-ON initial state error: curtain=${testRecord.bfOn.curtainVisible}, liftBtn=${testRecord.bfOn.liftBtnVisible}, optsCount=${initialOptionsCount}`
          );
        }

        // 3.2 AC-CORE with Curtain Active: scrollWidth
        const curtainScrollMetrics = await page.evaluate(() => ({
          scrollWidth: document.documentElement.scrollWidth,
          innerWidth: window.innerWidth,
          bodyScrollWidth: document.body.scrollWidth,
        }));

        testRecord.bfOn.curtainScrollOk =
          curtainScrollMetrics.scrollWidth <= curtainScrollMetrics.innerWidth &&
          curtainScrollMetrics.bodyScrollWidth <= curtainScrollMetrics.innerWidth;

        if (!testRecord.bfOn.curtainScrollOk) {
          testRecord.notes.push(
            `BF-ON Curtain overflow: scrollWidth=${curtainScrollMetrics.scrollWidth} > innerWidth=${curtainScrollMetrics.innerWidth}`
          );
        }

        // 3.3 Check button visible within viewport bounds during curtain
        const checkBtn = page.locator('[data-testid="check-btn"]');
        const checkBtnBox = await checkBtn.boundingBox();
        if (checkBtnBox) {
          const withinVp =
            checkBtnBox.y >= 0 &&
            checkBtnBox.y + checkBtnBox.height <= vp.height + 2 &&
            checkBtnBox.x >= 0 &&
            checkBtnBox.x + checkBtnBox.width <= vp.width + 2;
          testRecord.bfOn.curtainCheckBtnOk = withinVp;
          if (!withinVp) {
            testRecord.notes.push(
              `BF-ON check-btn outside viewport: top=${checkBtnBox.y}, height=${checkBtnBox.height}, vpHeight=${vp.height}`
            );
          }
        } else {
          testRecord.bfOn.curtainCheckBtnOk = false;
          testRecord.notes.push('BF-ON check-btn boundingBox is null');
        }

        // 3.4 Mathematical KaTeX overflow guard during curtain
        const katexMetrics = await page.evaluate(() => {
          const els = document.querySelectorAll('.katex, .katex-display');
          let overflowing = 0;
          for (const el of els) {
            const r = el.getBoundingClientRect();
            if (r.right > window.innerWidth + 2 || r.left < -2) {
              overflowing++;
            }
          }
          return { total: els.length, overflowing };
        });

        testRecord.bfOn.curtainKatexOk = katexMetrics.total > 0 && katexMetrics.overflowing === 0;
        if (!testRecord.bfOn.curtainKatexOk) {
          testRecord.notes.push(
            `BF-ON KaTeX overflow: total=${katexMetrics.total}, overflowing=${katexMetrics.overflowing}`
          );
        }

        if (vp.width === 683 && vp.height === 768) {
          const katexShot = path.join(screensDir, `katex_dense_683x768.png`);
          await page.screenshot({ path: katexShot });
        }

        // 3.5 Lift Curtain via Enter key (with fallback to lift-curtain-btn click)
        await page.keyboard.press('Enter');
        try {
          await curtain.waitFor({ state: 'detached', timeout: 2500 });
        } catch {
          if (await liftBtn.isVisible()) {
            await liftBtn.click();
            await curtain.waitFor({ state: 'detached', timeout: 3000 });
          }
        }

        await page.waitForSelector('[data-testid^="option-"]', { timeout: 5000 });
        await page.waitForTimeout(200);

        const revealedOptions = await page.locator('[data-testid^="option-"]').all();
        testRecord.bfOn.optionsRevealedCount = revealedOptions.length;
        testRecord.bfOn.curtainLiftOk = revealedOptions.length === 7;
        if (!testRecord.bfOn.curtainLiftOk) {
          testRecord.notes.push(`BF-ON curtain lift error: expected 7 options, found ${revealedOptions.length}`);
        }

        // 3.6 Non-trivial MC7 4+3 Options Distribution Check
        const distCheckOn = await verifyMc7OptionPositions(page, vp.expectColumns);
        testRecord.bfOn.optionsDistributionOk = distCheckOn.ok;
        testRecord.bfOn.actualColumns = distCheckOn.actualColumns;
        testRecord.bfOn.distribution = distCheckOn.distribution;

        if (!distCheckOn.ok) {
          testRecord.notes.push(`BF-ON options distribution error: ${distCheckOn.reason}`);
        }

        // Screenshot: Practice Initial State (Curtain Lifted)
        const practiceShot = path.join(screensDir, `practice_${vp.width}x${vp.height}.png`);
        await page.screenshot({ path: practiceShot });

        // 3.7 Interaction: Select option 0, trigger Check Answer, verify Toast + Action Button non-occlusion
        if (revealedOptions.length === 7) {
          await revealedOptions[0].click();
          await page.waitForTimeout(100);

          await checkBtn.click();
          await page.waitForTimeout(400); // Allow toast fade-in and feedback state

          const toastLocator = page.locator('[data-testid="feedback-toast"], [data-testid="good-work-toast"]');
          const isToastVisible = (await toastLocator.count()) > 0 && (await toastLocator.first().isVisible());
          testRecord.bfOn.toastFeedbackOk = isToastVisible;

          if (!isToastVisible) {
            testRecord.notes.push('BF-ON feedback toast was not visible after checking answer');
          }

          const nextBtn = page.locator('[data-testid="next-question-btn"]');
          const tryAgainBtn = page.locator('[data-testid="check-btn"]');
          const activeActionBtn = (await nextBtn.count()) > 0 && (await nextBtn.isVisible()) ? nextBtn : tryAgainBtn;

          const actionBtnBox = await activeActionBtn.boundingBox();
          const toastBox = isToastVisible ? await toastLocator.first().boundingBox() : null;

          if (actionBtnBox) {
            const btnWithinVp =
              actionBtnBox.y >= 0 &&
              actionBtnBox.y + actionBtnBox.height <= vp.height + 2 &&
              actionBtnBox.x >= 0 &&
              actionBtnBox.x + actionBtnBox.width <= vp.width + 2;

            let noOverlap = true;
            if (toastBox) {
              noOverlap = toastBox.y + toastBox.height <= actionBtnBox.y + 2;
            }

            testRecord.bfOn.actionButtonVisibleAfterToast = btnWithinVp && noOverlap;
            if (!btnWithinVp) {
              testRecord.notes.push(
                `BF-ON Action button outside viewport after toast: top=${actionBtnBox.y}, height=${actionBtnBox.height}, vpHeight=${vp.height}`
              );
            }
            if (!noOverlap) {
              testRecord.notes.push(
                `BF-ON Toast overlaps action button: toastBottom=${toastBox.y + toastBox.height}, actionTop=${actionBtnBox.y}`
              );
            }
          } else {
            testRecord.bfOn.actionButtonVisibleAfterToast = false;
            testRecord.notes.push('BF-ON action button boundingBox is null after toast');
          }

          if (vp.width === 683 && vp.height === 768) {
            const toastShot = path.join(screensDir, 'toast_feedback_683x768.png');
            await page.screenshot({ path: toastShot });
          }

          // Verify Answered state metrics (AC-1, AC-7)
          const answeredMetrics = await page.evaluate(() => ({
            scrollWidth: document.documentElement.scrollWidth,
            innerWidth: window.innerWidth,
          }));

          testRecord.bfOn.answeredScrollOk = answeredMetrics.scrollWidth <= answeredMetrics.innerWidth;
          if (!testRecord.bfOn.answeredScrollOk) {
            testRecord.notes.push(
              `BF-ON Answered state overflow: scrollWidth=${answeredMetrics.scrollWidth} > innerWidth=${answeredMetrics.innerWidth}`
            );
          }

          const answeredShot = path.join(screensDir, `answered_${vp.width}x${vp.height}.png`);
          await page.screenshot({ path: answeredShot });
        }

        testRecord.bfOn.passed =
          testRecord.bfOn.curtainVisible &&
          testRecord.bfOn.liftBtnVisible &&
          testRecord.bfOn.optionsHiddenInitially &&
          testRecord.bfOn.curtainScrollOk &&
          testRecord.bfOn.curtainCheckBtnOk &&
          testRecord.bfOn.curtainKatexOk &&
          testRecord.bfOn.curtainLiftOk &&
          testRecord.bfOn.optionsDistributionOk &&
          testRecord.bfOn.toastFeedbackOk &&
          testRecord.bfOn.actionButtonVisibleAfterToast &&
          testRecord.bfOn.answeredScrollOk;

        // =================================================================
        // MODE 2: BLANK-FIRST: OFF (AC-CORE Standard Flow)
        // =================================================================

        // 3.8 Toggle Blank-First to OFF using the header toggle button
        const toggleBtn = page.locator('[data-testid="toggle-blank-first-btn"]');
        await toggleBtn.click();
        await page.waitForTimeout(150);

        // 3.9 Return to overview and re-enter practice (sessionStorage persists tops_blank_first_enabled = 'false')
        const quitBtn = page.locator('button[aria-label="Quit practice"]');
        await quitBtn.click();

        const quitConfirmExit = page.locator('[data-testid="quit-confirm-exit"]');
        try {
          await quitConfirmExit.waitFor({ state: 'visible', timeout: 3000 });
          await quitConfirmExit.click();
        } catch {
          // If modal did not appear or was dismissed
        }

        await page.waitForSelector('[data-testid="completion-tracker-summary"]', { timeout: SELECTOR_TIMEOUT });
        await page.waitForTimeout(200);

        const practiceBtnOff = page.locator('button[data-testid^="competency-"]').first();
        await practiceBtnOff.click();

        const startPracticeBtnOff = page.locator('[data-testid="start-practice-btn"]');
        try {
          await startPracticeBtnOff.waitFor({ state: 'visible', timeout: 3000 });
          await startPracticeBtnOff.click();
        } catch {}

        await page.waitForSelector('[data-testid="question-card"]', { timeout: SELECTOR_TIMEOUT });
        await page.waitForTimeout(300);

        // 3.10 In Blank-First: OFF, curtain must NOT be rendered / visible
        const curtainOffCount = await page.locator('[data-testid="blank-first-curtain"]').count();
        testRecord.bfOff.curtainHidden = curtainOffCount === 0 || !(await page.locator('[data-testid="blank-first-curtain"]').isVisible());
        if (!testRecord.bfOff.curtainHidden) {
          testRecord.notes.push('BF-OFF error: curtain is still visible in OFF mode');
        }

        // 3.11 Exactly 7 options must be immediately rendered without curtain interaction
        const optionsOff = await page.locator('[data-testid^="option-"]').all();
        testRecord.bfOff.optionsImmediateCount = optionsOff.length;
        testRecord.bfOff.optionsImmediateOk = optionsOff.length === 7;
        if (!testRecord.bfOff.optionsImmediateOk) {
          testRecord.notes.push(`BF-OFF error: expected 7 immediate options, found ${optionsOff.length}`);
        }

        // 3.12 AC-CORE validation in Blank-First: OFF
        const practiceMetricsOff = await page.evaluate(() => ({
          scrollWidth: document.documentElement.scrollWidth,
          innerWidth: window.innerWidth,
          bodyScrollWidth: document.body.scrollWidth,
        }));

        testRecord.bfOff.practiceScrollOk =
          practiceMetricsOff.scrollWidth <= practiceMetricsOff.innerWidth &&
          practiceMetricsOff.bodyScrollWidth <= practiceMetricsOff.innerWidth;

        if (!testRecord.bfOff.practiceScrollOk) {
          testRecord.notes.push(
            `BF-OFF practice overflow: scrollWidth=${practiceMetricsOff.scrollWidth} > innerWidth=${practiceMetricsOff.innerWidth}`
          );
        }

        const checkBtnOff = page.locator('[data-testid="check-btn"]');
        const checkBtnBoxOff = await checkBtnOff.boundingBox();
        if (checkBtnBoxOff) {
          const withinVp =
            checkBtnBoxOff.y >= 0 &&
            checkBtnBoxOff.y + checkBtnBoxOff.height <= vp.height + 2 &&
            checkBtnBoxOff.x >= 0 &&
            checkBtnBoxOff.x + checkBtnBoxOff.width <= vp.width + 2;
          testRecord.bfOff.checkButtonVisibleOk = withinVp;
          if (!withinVp) {
            testRecord.notes.push(
              `BF-OFF check-btn outside viewport: top=${checkBtnBoxOff.y}, height=${checkBtnBoxOff.height}, vpHeight=${vp.height}`
            );
          }
        } else {
          testRecord.bfOff.checkButtonVisibleOk = false;
          testRecord.notes.push('BF-OFF check-btn boundingBox is null');
        }

        const katexMetricsOff = await page.evaluate(() => {
          const els = document.querySelectorAll('.katex, .katex-display');
          let overflowing = 0;
          for (const el of els) {
            const r = el.getBoundingClientRect();
            if (r.right > window.innerWidth + 2 || r.left < -2) {
              overflowing++;
            }
          }
          return { total: els.length, overflowing };
        });

        testRecord.bfOff.katexOverflowOk = katexMetricsOff.total > 0 && katexMetricsOff.overflowing === 0;
        if (!testRecord.bfOff.katexOverflowOk) {
          testRecord.notes.push(
            `BF-OFF KaTeX overflow: total=${katexMetricsOff.total}, overflowing=${katexMetricsOff.overflowing}`
          );
        }

        const distCheckOff = await verifyMc7OptionPositions(page, vp.expectColumns);
        testRecord.bfOff.optionsDistributionOk = distCheckOff.ok;
        testRecord.bfOff.actualColumns = distCheckOff.actualColumns;
        testRecord.bfOff.distribution = distCheckOff.distribution;

        if (!distCheckOff.ok) {
          testRecord.notes.push(`BF-OFF options distribution error: ${distCheckOff.reason}`);
        }

        testRecord.bfOff.passed =
          testRecord.bfOff.curtainHidden &&
          testRecord.bfOff.optionsImmediateOk &&
          testRecord.bfOff.practiceScrollOk &&
          testRecord.bfOff.checkButtonVisibleOk &&
          testRecord.bfOff.katexOverflowOk &&
          testRecord.bfOff.optionsDistributionOk;

        // Overall pass decision for this viewport across both modes
        testRecord.passed =
          testRecord.overviewScrollOk &&
          testRecord.sidebarBehaviorOk &&
          testRecord.bfOn.passed &&
          testRecord.bfOff.passed;

        if (!testRecord.passed) allPassed = false;
      } catch (err) {
        testRecord.passed = false;
        testRecord.notes.push(`Exception: ${err.message}`);
        allPassed = false;
      } finally {
        await context.close();
      }

      results.push(testRecord);
      const statusIcon = testRecord.passed ? '✅ PASS' : '❌ FAIL';
      console.log(`Result: ${statusIcon}`);
      console.log(`- Overview No-Scroll: ${testRecord.overviewScrollOk ? 'OK' : 'FAIL'}`);
      console.log(`- Sidebar Responsive: ${testRecord.sidebarBehaviorOk ? 'OK' : 'FAIL'}`);
      console.log(`[Blank-First: ON]`);
      console.log(`  - Curtain & Lift Button Visible: ${testRecord.bfOn.curtainVisible && testRecord.bfOn.liftBtnVisible ? 'OK' : 'FAIL'}`);
      console.log(`  - Options Hidden Initially: ${testRecord.bfOn.optionsHiddenInitially ? 'OK' : 'FAIL'}`);
      console.log(`  - Curtain No-Scroll: ${testRecord.bfOn.curtainScrollOk ? 'OK' : 'FAIL'}`);
      console.log(`  - KaTeX Overflow Guard: ${testRecord.bfOn.curtainKatexOk ? 'OK' : 'FAIL'}`);
      console.log(`  - Check Button Visible: ${testRecord.bfOn.curtainCheckBtnOk ? 'OK' : 'FAIL'}`);
      console.log(`  - Enter Lifts Curtain (7 Options): ${testRecord.bfOn.curtainLiftOk ? 'OK' : 'FAIL'}`);
      console.log(`  - Options Distribution: ${testRecord.bfOn.optionsDistributionOk ? 'OK' : 'FAIL'} (${testRecord.bfOn.distribution})`);
      console.log(`  - Toast Feedback Rendered: ${testRecord.bfOn.toastFeedbackOk ? 'OK' : 'FAIL'}`);
      console.log(`  - Action Button Visible After Toast: ${testRecord.bfOn.actionButtonVisibleAfterToast ? 'OK' : 'FAIL'}`);
      console.log(`  - Answered No-Scroll: ${testRecord.bfOn.answeredScrollOk ? 'OK' : 'FAIL'}`);
      console.log(`  - Blank-First ON Status: ${testRecord.bfOn.passed ? 'PASS' : 'FAIL'}`);
      console.log(`[Blank-First: OFF]`);
      console.log(`  - Curtain Hidden: ${testRecord.bfOff.curtainHidden ? 'OK' : 'FAIL'}`);
      console.log(`  - 7 Options Immediate: ${testRecord.bfOff.optionsImmediateOk ? 'OK' : 'FAIL'}`);
      console.log(`  - Practice No-Scroll: ${testRecord.bfOff.practiceScrollOk ? 'OK' : 'FAIL'}`);
      console.log(`  - KaTeX Overflow Guard: ${testRecord.bfOff.katexOverflowOk ? 'OK' : 'FAIL'}`);
      console.log(`  - Check Button Visible: ${testRecord.bfOff.checkButtonVisibleOk ? 'OK' : 'FAIL'}`);
      console.log(`  - Options Distribution: ${testRecord.bfOff.optionsDistributionOk ? 'OK' : 'FAIL'} (${testRecord.bfOff.distribution})`);
      console.log(`  - Blank-First OFF Status: ${testRecord.bfOff.passed ? 'PASS' : 'FAIL'}`);
      if (testRecord.notes.length > 0) {
        console.log(`  Notes: ${testRecord.notes.join(' | ')}`);
      }
    }
  } finally {
    await globalCleanup();
  }

  console.log('\n================================================================');
  console.log(' MILESTONE 1-T: VIEWPORT MATRIX DUAL MODE SUMMARY');
  console.log('================================================================');

  console.log('\n--- MODE 1: BLANK-FIRST: ON (AC-CORE + Evocation Curtain Flow) ---');
  console.table(
    results.map((r) => ({
      Viewport: r.viewport,
      Overview: r.overviewScrollOk ? 'PASS' : 'FAIL',
      Sidebar: r.sidebarBehaviorOk ? 'PASS' : 'FAIL',
      Curtain: r.bfOn.curtainVisible ? 'PASS' : 'FAIL',
      Lift: r.bfOn.curtainLiftOk ? 'PASS' : 'FAIL',
      Distribution: `${r.bfOn.distribution} (${r.bfOn.optionsDistributionOk ? 'PASS' : 'FAIL'})`,
      'Check-Btn': r.bfOn.curtainCheckBtnOk ? 'PASS' : 'FAIL',
      Toast: r.bfOn.toastFeedbackOk ? 'PASS' : 'FAIL',
      'Btn-After-Toast': r.bfOn.actionButtonVisibleAfterToast ? 'PASS' : 'FAIL',
      Answered: r.bfOn.answeredScrollOk ? 'PASS' : 'FAIL',
      Status: r.bfOn.passed ? 'PASS' : 'FAIL',
    }))
  );

  console.log('\n--- MODE 2: BLANK-FIRST: OFF (AC-CORE Standard Flow) ---');
  console.table(
    results.map((r) => ({
      Viewport: r.viewport,
      'Curtain-Hidden': r.bfOff.curtainHidden ? 'PASS' : 'FAIL',
      'Immediate-Opts': r.bfOff.optionsImmediateOk ? 'PASS' : 'FAIL',
      PracticeScroll: r.bfOff.practiceScrollOk ? 'PASS' : 'FAIL',
      KaTeX: r.bfOff.katexOverflowOk ? 'PASS' : 'FAIL',
      Distribution: `${r.bfOff.distribution} (${r.bfOff.optionsDistributionOk ? 'PASS' : 'FAIL'})`,
      'Check-Btn': r.bfOff.checkButtonVisibleOk ? 'PASS' : 'FAIL',
      Status: r.bfOff.passed ? 'PASS' : 'FAIL',
    }))
  );

  console.log('\n--- OVERALL VIEWPORT MATRIX PASS/FAIL DECISION (12 VIEWPORTS) ---');
  console.table(
    results.map((r) => ({
      Viewport: r.viewport,
      Label: r.label,
      'Blank-First: ON': r.bfOn.passed ? 'PASS' : 'FAIL',
      'Blank-First: OFF': r.bfOff.passed ? 'PASS' : 'FAIL',
      Status: r.passed ? 'PASS' : 'FAIL',
    }))
  );

  if (!allPassed) {
    console.error('\nMatrix suite finished with failures.');
    process.exit(1);
  } else {
    console.log('\nMatrix suite PASSED 100% across all 12 viewports in both Blank-First: ON and Blank-First: OFF modes with non-trivial hardened assertions!');
    process.exit(0);
  }
}

runMatrix().catch((e) => {
  console.error('Fatal execution error:', e);
  process.exit(1);
});
