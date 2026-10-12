"""Cognitive Task Analysis (CTA) Data Models and Parser.

Provides structured models for the Knowledge Triad (Facts, Concepts, Skills) and
fused distractors (misconceptions + expert blindness), without any hardcoded domain logic
or external LLM API calls.
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger("cta_analyzer")


@dataclass
class DistractorModel:
    """A fused misconception or expert blindness error model."""
    id: str
    name: str
    wrong_belief: Optional[str] = None
    correct_belief: Optional[str] = None
    omitted_step: Optional[str] = None
    trigger: str = ""
    manifestation: str = ""
    error_type: str = "other"
    severity: str = "medium"
    origin: str = "source"
    evidence: Optional[Dict[str, Any]] = None
    remediation_hint: str = ""


@dataclass
class CompetencyItem:
    """A granular assessed competency within the course curriculum."""
    id: str  # e.g. "Hab-01", "C-01", "H-01"
    code: str  # e.g. "HAB-01", "CON-01", "HEC-01"
    name: str
    category: str  # "Skill", "Concept", "Fact"
    description: str
    mastery_target: int = 100
    bloom: str = "Apply"
    prerequisites: List[str] = field(default_factory=list)
    source_examples: List[str] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    distractors: List[DistractorModel] = field(default_factory=list)

    def to_course_dict(self) -> Dict[str, Any]:
        """Converts to standard course manifest competency dictionary."""
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "mastery_target": self.mastery_target,
        }


@dataclass
class CTAResult:
    """Complete result of Cognitive Task Analysis."""
    course_id: str
    title: str = ""
    macro_competency: str = ""
    competencies: List[CompetencyItem] = field(default_factory=list)
    raw_markdown: str = ""

    def get_competency(self, comp_id: str) -> Optional[CompetencyItem]:
        """Finds competency by ID."""
        for c in self.competencies:
            if c.id == comp_id or c.code == comp_id:
                return c
        return None

    def get_by_category(self, category: str) -> List[CompetencyItem]:
        """Returns competencies belonging to specified category."""
        return [c for c in self.competencies if c.category.lower() == category.lower()]


class CTAAnalyzer:
    """Agnostic loader and parser for Cognitive Task Analysis artifacts."""

    def __init__(self, prompt_template_path: Optional[Union[str, Path]] = None) -> None:
        self.prompt_path = Path(prompt_template_path) if prompt_template_path else None

    def load_from_json(self, json_path: Union[str, Path]) -> CTAResult:
        """Parses a cta.json file into a CTAResult object."""
        path = Path(json_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        return self.from_dict(data)

    def from_dict(self, data: Dict[str, Any]) -> CTAResult:
        """Constructs a CTAResult from a dictionary matching cta.schema.json."""
        cid = data.get("course_id", "course_generic")
        title = data.get("title", cid)
        macro = data.get("macro_competency", "")

        competencies: List[CompetencyItem] = []
        for raw_c in data.get("competencies", []):
            distractors = []
            for raw_d in raw_c.get("distractors", []):
                distractors.append(
                    DistractorModel(
                        id=raw_d.get("id", ""),
                        name=raw_d.get("name", ""),
                        wrong_belief=raw_d.get("wrong_belief"),
                        correct_belief=raw_d.get("correct_belief"),
                        omitted_step=raw_d.get("omitted_step"),
                        trigger=raw_d.get("trigger", ""),
                        manifestation=raw_d.get("manifestation", ""),
                        error_type=raw_d.get("error_type", "other"),
                        severity=raw_d.get("severity", "medium"),
                        origin=raw_d.get("origin", "source"),
                        evidence=raw_d.get("evidence"),
                        remediation_hint=raw_d.get("remediation_hint", ""),
                    )
                )

            raw_cat = raw_c.get("type") or raw_c.get("category", "Concept")
            cat_map = {"skill": "Skill", "concept": "Concept", "fact": "Fact"}
            category = cat_map.get(raw_cat.lower(), raw_cat.title())

            comp_id = raw_c.get("id", "")
            code = raw_c.get("code") or comp_id.upper().replace("-", "")

            competencies.append(
                CompetencyItem(
                    id=comp_id,
                    code=code,
                    name=raw_c.get("name", comp_id),
                    category=category,
                    description=raw_c.get("description_latex") or raw_c.get("description", ""),
                    mastery_target=raw_c.get("mastery_target", 100),
                    bloom=raw_c.get("bloom", "Apply"),
                    prerequisites=raw_c.get("prerequisites", []),
                    source_examples=raw_c.get("source_examples", []),
                    evidence=raw_c.get("evidence", []),
                    distractors=distractors,
                )
            )

        return CTAResult(
            course_id=cid,
            title=title,
            macro_competency=macro,
            competencies=competencies,
        )

    def analyze(self, content_text: str, course_id: str = "course_generic") -> CTAResult:
        """Parses JSON content if provided as JSON string, or returns a basic CTAResult."""
        try:
            parsed = json.loads(content_text)
            if isinstance(parsed, dict) and "competencies" in parsed:
                return self.from_dict(parsed)
        except Exception:
            pass

        return CTAResult(
            course_id=course_id,
            macro_competency="Curriculum Analysis",
            competencies=[],
            raw_markdown=content_text,
        )
