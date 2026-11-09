"""
Contract tests for Milestone 6: Antigravity Study Harness 2.0.

Validates structural invariants and prompt generation across platform/src:
- Blank-First curtain in QuestionCard.tsx and PracticeSession.tsx
- Socratic Transfer ($0 API) button and anti-giveaway contract in socraticPrompt.ts
- Enter key handling to lift the curtain
- SessionStorage persistence for tops_blank_first_enabled
- Data testids preserved for automated test suites
"""

from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLATFORM_SRC = REPO_ROOT / "platform" / "src"

QUESTION_CARD_TSX = PLATFORM_SRC / "components" / "QuestionCard.tsx"
PRACTICE_SESSION_TSX = PLATFORM_SRC / "components" / "PracticeSession.tsx"
SOCRATIC_PROMPT_TS = PLATFORM_SRC / "utils" / "socraticPrompt.ts"


class TestMilestone6StaticContracts:
    """Verifies that all Milestone 6 components exist and contain the required contract invariants."""

    def test_socratic_prompt_utility_exists_and_contains_anti_giveaway(self):
        assert SOCRATIC_PROMPT_TS.exists(), "Missing socraticPrompt.ts utility"
        content = SOCRATIC_PROMPT_TS.read_text(encoding="utf-8")

        assert "buildSocraticPrompt" in content, "Missing buildSocraticPrompt export"
        assert "ANTI-GIVEAWAY" in content, "Missing anti-giveaway contract in prompt"
        assert "PROHIBIDO revelar la respuesta correcta" in content, "Missing rule 1 in socratic prompt"
        assert "UNA SOLA pregunta reflexiva" in content, "Missing single question rule in socratic prompt"

    def test_question_card_contains_curtain_and_socratic_button(self):
        assert QUESTION_CARD_TSX.exists(), "Missing QuestionCard.tsx"
        content = QUESTION_CARD_TSX.read_text(encoding="utf-8")

        assert 'data-testid="blank-first-curtain"' in content, "Missing blank-first-curtain testid"
        assert 'data-testid="lift-curtain-btn"' in content, "Missing lift-curtain-btn testid"
        assert 'data-testid="socratic-tutor-container"' in content, "Missing socratic-tutor-container testid"
        assert 'data-testid="copy-socratic-prompt-btn"' in content, "Missing copy-socratic-prompt-btn testid"
        assert "isCurtainLifted" in content, "Missing isCurtainLifted prop in QuestionCard"
        assert "blankFirstEnabled" in content, "Missing blankFirstEnabled prop in QuestionCard"
        assert "isSocraticUnlocked" in content, "Missing isSocraticUnlocked gate in QuestionCard"
        assert "minAttemptsNeeded = totalHints > 0 ? 3 : 2" in content, "Missing adaptive attempts threshold (3 with hints, 2 without)"
        assert "Haz click en el botón y Copia y pega el text en tu IA favorita para ayuda especializada para que te ayude." in content, "Missing updated Socratic transfer helper text"
        assert "fillInputRef.current?.focus" in content, "Missing autofocus on fill_in_the_blank"

    def test_practice_session_contains_toggle_and_curtain_management(self):
        assert PRACTICE_SESSION_TSX.exists(), "Missing PracticeSession.tsx"
        content = PRACTICE_SESSION_TSX.read_text(encoding="utf-8")

        assert 'data-testid="toggle-blank-first-btn"' in content, "Missing toggle-blank-first-btn testid"
        assert "tops_blank_first_enabled" in content, "Missing tops_blank_first_enabled sessionStorage persistence"
        assert "isCurtainLifted" in content, "Missing isCurtainLifted state in PracticeSession"
        assert "setIsCurtainLifted(true)" in content, "Missing curtain lift handler on Enter"
        assert "Blank-First: ON" in content, "Missing Blank-First: ON badge in header"
        assert "OPTION_KEYS" in content, "Missing mouseless OPTION_KEYS hotkey array"
        assert "handleSelectOption" in content, "Missing handleSelectOption hotkey trigger"
        assert "handleToggleMultiOption" in content, "Missing handleToggleMultiOption hotkey trigger"
        assert "prev === id ? null : id" in content, "Missing toggle-deselect for single-choice option"
        assert "nextWrongCount >= 4" in content, "Expected max attempts limit to be 4"
