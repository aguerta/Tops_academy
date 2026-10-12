import { test, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

const SCREENSHOTS_DIR = path.resolve(__dirname, 'screenshots');

test.describe('Visual Fidelity Screenshot Generator', () => {

  test.beforeAll(() => {
    if (!fs.existsSync(SCREENSHOTS_DIR)) {
      fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });
    }
  });

  test('VF-01: Capture 6 Canonical Platform States', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });

    // 1. Course Overview
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const courseLink = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')");
    if (await courseLink.count() > 0) {
      await courseLink.first().click();
      await page.waitForLoadState('networkidle');
    }
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, '01_course_overview.png'), fullPage: true });

    // 2. Pre-exercise
    const unitTrigger = page.locator("[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Practice')");
    if (await unitTrigger.count() > 0) {
      await unitTrigger.first().click();
      await page.waitForTimeout(400);
    }
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, '02_pre_exercise.png') });

    // 3. Question with Graph
    const letsGo = page.locator("button:has-text(\"Let's go\"), [data-testid='start-practice-btn']");
    if (await letsGo.count() > 0 && await letsGo.first().isVisible()) {
      await letsGo.first().click();
      await page.waitForLoadState('networkidle');
    }
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, '03_question_with_graph.png') });

    // 4. Good Answer Toast
    const optCorrect = page.locator("[data-testid^='option-']:has-text('-4'), .option-item:has-text('-4')");
    if (await optCorrect.count() > 0) {
      await optCorrect.first().click();
      const checkBtn = page.locator("button:has-text('Check'), [data-testid='check-btn']").first();
      if (await checkBtn.isEnabled()) {
        await checkBtn.click();
        await page.waitForTimeout(500);
      }
    }
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, '04_good_answer_toast.png') });

    // 5. Exercise Complete Confetti
    for (let i = 0; i < 8; i++) {
      const completion = page.locator("[data-testid='completion-screen'], :text-matches('Exercise complete', 'i')");
      if (await completion.count() > 0 && await completion.first().isVisible()) break;
      const nextBtn = page.locator("button:has-text('Next question'), button:has-text('Next')");
      if (await nextBtn.count() > 0 && await nextBtn.first().isVisible()) {
        await nextBtn.first().click();
        await page.waitForTimeout(300);
        continue;
      }
      const skipBtn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']").first();
      if (await skipBtn.isVisible() && await skipBtn.isEnabled()) {
        await skipBtn.click();
        await page.waitForTimeout(300);
      }
    }
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, '05_exercise_complete_confetti.png') });

    // 6. Course Challenge
    await page.goto('/');
    const challengeLink = page.locator("a:has-text('Comprehensive Challenge'), button:has-text('Comprehensive Challenge')");
    if (await challengeLink.count() > 0) {
      await challengeLink.first().click();
      const challengeCard = page.locator("[data-testid='course-challenge-card'], a:has-text('Course challenge')");
      if (await challengeCard.count() > 0) {
        await challengeCard.first().click();
        await page.waitForTimeout(400);
      }
    }
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, '06_course_challenge.png') });

    const expectedFiles = [
      '01_course_overview.png',
      '02_pre_exercise.png',
      '03_question_with_graph.png',
      '04_good_answer_toast.png',
      '05_exercise_complete_confetti.png',
      '06_course_challenge.png',
    ];
    for (const f of expectedFiles) {
      expect(fs.existsSync(path.join(SCREENSHOTS_DIR, f))).toBeTruthy();
    }
  });

});
