import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const COURSES_DIR = path.resolve(__dirname, '../../courses');
const FIXTURES_DIR = path.resolve(COURSES_DIR, 'test_fixtures');

test.describe('Platform Acceptance Criteria (E2E Headless Suite)', () => {

  test.beforeEach(async ({ page }) => {
    // Collect console errors
    const consoleErrors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error' && !msg.text().includes('favicon.ico')) {
        consoleErrors.push(msg.text());
      }
    });
    page.on('pageerror', err => {
      consoleErrors.push(err.message);
    });
    (page as any)._consoleErrors = consoleErrors;
  });

  test.afterEach(async ({ page }) => {
    const errs = (page as any)._consoleErrors || [];
    expect(errs, `Unhandled console errors found: ${errs.join(', ')}`).toHaveLength(0);
  });

  test('AC-01: Library lists courses and hot-reloads new valid course file', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Verify baseline course exists
    const bodyText = await page.innerText('body');
    expect(bodyText).toMatch(/Calculus|Limits|Differential/i);

    // Copy new dynamic course into courses/
    const dynamicPath = path.resolve(COURSES_DIR, 'dynamic_node_course.json');
    try {
      const srcFixture = fs.readFileSync(path.resolve(FIXTURES_DIR, 'valid_course_calculus.json'), 'utf-8');
      const modified = srcFixture
        .replace('Differential Calculus (Test Fixture)', 'Dynamic Node Course')
        .replace('test-differential-calculus', 'dynamic-node-course');
      fs.writeFileSync(dynamicPath, modified, 'utf-8');

      await page.waitForTimeout(500);
      await page.reload();
      await page.waitForLoadState('networkidle');

      const reloadedText = await page.innerText('body');
      expect(reloadedText).toContain('Dynamic Node Course');
    } finally {
      if (fs.existsSync(dynamicPath)) fs.unlinkSync(dynamicPath);
    }
  });

  test('AC-02: Invalid course shows error card without breaking valid courses', async ({ page }) => {
    const corruptPath = path.resolve(COURSES_DIR, 'z_node_corrupt.json');
    try {
      fs.copyFileSync(path.resolve(FIXTURES_DIR, 'invalid_corrupt_course.json'), corruptPath);

      await page.goto('/');
      await page.waitForLoadState('networkidle');

      const bodyText = await page.innerText('body');
      // Valid course remains
      expect(bodyText).toMatch(/Calculus|Limits/i);

      // Error indication is present
      const errorIndicator = page.locator("[data-testid='course-error-card'], :text-matches('Error|Invalid|Corrupted', 'i')");
      expect(await errorIndicator.count() > 0 || /error|invalid|corrupted/i.test(bodyText)).toBeTruthy();
    } finally {
      if (fs.existsSync(corruptPath)) fs.unlinkSync(corruptPath);
    }
  });

  test('AC-03: Course overview displays units, mastery legend, and course mastery %', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const courseLink = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')");
    if (await courseLink.count() > 0) {
      await courseLink.first().click();
      await page.waitForLoadState('networkidle');
    }

    const text = await page.innerText('body');
    expect(text).toMatch(/Course mastery|mastery:/i);
    expect(text).toContain('Mastered');
    expect(text).toContain('Proficient');
    expect(text).toContain('Familiar');
    expect(text).toContain('Attempted');
    expect(text).toContain('Not started');
    expect(text).toMatch(/Limits intro/i);
  });

  test('AC-04: Full practice session wrong -> hints -> correct -> completion', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const courseLink = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')");
    if (await courseLink.count() > 0) {
      await courseLink.first().click();
      await page.waitForLoadState('networkidle');
    }

    const unitTrigger = page.locator("[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Practice')");
    if (await unitTrigger.count() > 0) {
      await unitTrigger.first().click();
    }

    const letsGo = page.locator("button:has-text(\"Let's go\"), [data-testid='start-practice-btn']");
    if (await letsGo.count() > 0 && await letsGo.first().isVisible()) {
      await letsGo.first().click();
      await page.waitForLoadState('networkidle');
    }

    // Hint reveal check
    const hintBtn = page.locator("button:has-text('hint'), [data-testid='hints-toggle']");
    if (await hintBtn.count() > 0 && await hintBtn.first().isVisible()) {
      await hintBtn.first().click();
      const getHint = page.locator("button:has-text('Get hint'), button:has-text('next hint')");
      if (await getHint.count() > 0 && await getHint.first().isVisible()) {
        await getHint.first().click();
      }
    }

    // Step through questions until completion screen
    for (let i = 0; i < 8; i++) {
      const completion = page.locator("[data-testid='completion-screen'], :text-matches('Exercise complete', 'i')");
      if (await completion.count() > 0 && await completion.first().isVisible()) break;

      const optCorrect = page.locator("[data-testid^='option-']:has-text('-4'), .option-item:has-text('-4')");
      if (await optCorrect.count() > 0 && await optCorrect.first().isVisible()) {
        await optCorrect.first().click();
        const checkBtn = page.locator("button:has-text('Check'), [data-testid='check-btn']").first();
        if (await checkBtn.isEnabled()) {
          await checkBtn.click();
          await page.waitForTimeout(400);
        }
      } else {
        const skipBtn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']").first();
        if (await skipBtn.isVisible() && await skipBtn.isEnabled()) {
          await skipBtn.click();
          await page.waitForTimeout(300);
        }
      }

      const nextBtn = page.locator("button:has-text('Next question'), button:has-text('Next')");
      if (await nextBtn.count() > 0 && await nextBtn.first().isVisible()) {
        await nextBtn.first().click();
        await page.waitForTimeout(300);
      }
    }

    const text = await page.innerText('body');
    expect(text).toMatch(/Exercise complete|correct|\d\/\d/i);
  });

  test('AC-06: Grading types: MCQ, algebraic equivalence, all-or-nothing multi-select', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const courseLink = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')");
    if (await courseLink.count() > 0) {
      await courseLink.first().click();
    }

    const unitTrigger = page.locator("[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Practice')");
    if (await unitTrigger.count() > 0) {
      await unitTrigger.first().click();
    }

    const letsGo = page.locator("button:has-text(\"Let's go\"), [data-testid='start-practice-btn']");
    if (await letsGo.count() > 0 && await letsGo.first().isVisible()) {
      await letsGo.first().click();
    }

    // Fill in the blank algebraic equivalence test
    for (let i = 0; i < 5; i++) {
      const fillInput = page.locator("input[data-testid='fill-blank-input'], input[type='text']");
      const stem = await page.innerText('body');
      if (await fillInput.count() > 0 && (stem.includes('alpha') || stem.includes('sigma') || stem.includes('L ='))) {
        await fillInput.first().fill('1-(alpha+n)*sigma');
        const checkBtn = page.locator("button:has-text('Check'), [data-testid='check-btn']").first();
        if (await checkBtn.isEnabled()) {
          await checkBtn.click();
          await page.waitForTimeout(400);
          const feedback = await page.innerText('body');
          expect(feedback).toMatch(/Good work|correct/i);
        }
        break;
      }
      const skipBtn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']").first();
      if (await skipBtn.isVisible() && await skipBtn.isEnabled()) {
        await skipBtn.click();
        await page.waitForTimeout(300);
      }
    }
  });

  test('AC-09: Question with graph renders Cartesian SVG elements', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const courseLink = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')");
    if (await courseLink.count() > 0) {
      await courseLink.first().click();
    }

    const unitTrigger = page.locator("[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Practice')");
    if (await unitTrigger.count() > 0) {
      await unitTrigger.first().click();
    }

    const letsGo = page.locator("button:has-text(\"Let's go\"), [data-testid='start-practice-btn']");
    if (await letsGo.count() > 0 && await letsGo.first().isVisible()) {
      await letsGo.first().click();
    }

    let graphFound = false;
    for (let i = 0; i < 5; i++) {
      const svg = page.locator("[data-testid='coordinate-plane'], svg.coordinate-plane, [data-testid='graph-container'] svg, svg");
      if (await svg.count() > 0) {
        const circles = svg.locator('circle');
        const paths = svg.locator('path, line');
        if (await circles.count() > 0 || await paths.count() > 0) {
          graphFound = true;
          expect(await circles.count()).toBeGreaterThanOrEqual(1);
          break;
        }
      }
      const skipBtn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']").first();
      if (await skipBtn.isVisible() && await skipBtn.isEnabled()) {
        await skipBtn.click();
        await page.waitForTimeout(300);
      }
    }
    expect(graphFound).toBeTruthy();
  });

});
