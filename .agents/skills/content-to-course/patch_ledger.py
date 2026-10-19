"""Patch Ledger: Unified Auditing and Telemetry for Automated Healers in C2C.

Tracks every automated repair (L1 to L5, shard normalizers, judge re-dispatch, append remap)
across runs to ensure transparency, observability, and anti-regression safeguards.

Severities:
- 'healed': Lossless, mechanical repair (e.g. raw-string conversion, control-char fix, bare macro wrap).
- 'snapped': Value changed to align with constraints (e.g. evidence page snapped to manifest).
- 'degraded': Content reduced to guarantee compilation/validity (e.g. unresolvable math wrapped in \\text{}).

Artifacts:
- Per-run machine-readable: work/telemetry/patch_ledger.json
- Per-run human review: work/cta_review.md
- Cross-run append-only: reports/c2c_patches/patch_ledger.jsonl
- Degradation threshold gate: alert if degraded fields exceed 3% of total competencies/fields.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

logger = logging.getLogger("patch_ledger")


@dataclass
class PatchRecord:
    stage: str
    layer: str
    rule_id: str
    scope: str
    before: Any
    after: Any
    severity: str  # "healed" | "snapped" | "degraded"
    reason: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PatchLedger:
    """Manages active run patch records, metrics, and persistence."""

    def __init__(self, course_id: str = "custom_course"):
        self.course_id = course_id
        self.records: List[PatchRecord] = []
        self._total_evaluated_fields: int = 0

    def record_patch(
        self,
        stage: str,
        layer: str,
        rule_id: str,
        scope: str,
        before: Any,
        after: Any,
        severity: str,
        reason: str,
    ) -> PatchRecord:
        """Records an automated patch."""
        norm_sev = severity.lower().strip()
        if norm_sev not in ("healed", "snapped", "degraded"):
            norm_sev = "healed"

        record = PatchRecord(
            stage=stage,
            layer=layer,
            rule_id=rule_id,
            scope=scope,
            before=before,
            after=after,
            severity=norm_sev,
            reason=reason,
        )
        self.records.append(record)
        return record

    record = record_patch

    def set_total_fields(self, count: int) -> None:
        """Sets denominator for degraded % calculation (e.g. total fields or competencies)."""
        self._total_evaluated_fields = max(0, count)

    @property
    def total_patches(self) -> int:
        return len(self.records)

    def count_by_severity(self) -> Dict[str, int]:
        counts = {"healed": 0, "snapped": 0, "degraded": 0}
        for r in self.records:
            counts[r.severity] = counts.get(r.severity, 0) + 1
        return counts

    def count_by_rule(self) -> Dict[str, int]:
        return dict(Counter(r.rule_id for r in self.records))

    def count_by_layer(self) -> Dict[str, int]:
        return dict(Counter(r.layer for r in self.records))

    def count_by_stage(self) -> Dict[str, int]:
        return dict(Counter(r.stage for r in self.records))

    def degraded_percentage(self, total_items: Optional[int] = None) -> float:
        """Calculates percentage of degraded items relative to total items/fields."""
        total = total_items or self._total_evaluated_fields or max(1, self.total_patches)
        degraded = sum(1 for r in self.records if r.severity == "degraded")
        return round((degraded / total) * 100.0, 2)

    def check_degraded_alert(
        self,
        total_items: Optional[int] = None,
        threshold_pct: float = 3.0,
    ) -> Tuple[bool, float, str]:
        """Returns (alert_triggered, pct, message)."""
        pct = self.degraded_percentage(total_items)
        degraded_count = sum(1 for r in self.records if r.severity == "degraded")
        if pct > threshold_pct:
            msg = (
                f"ALERT: Degraded fields ({degraded_count}, {pct}%) exceed the strict threshold of {threshold_pct}%. "
                "This indicates excessive prompt or source errors requiring prompt hardening."
            )
            return True, pct, msg
        return False, pct, f"OK: Degraded fields ({degraded_count}, {pct}%) within {threshold_pct}% budget."

    def to_summary_dict(self, total_items: Optional[int] = None) -> Dict[str, Any]:
        alert, pct, alert_msg = self.check_degraded_alert(total_items)
        return {
            "course_id": self.course_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_patches": self.total_patches,
            "summary": self.count_by_severity(),
            "by_rule": self.count_by_rule(),
            "by_layer": self.count_by_layer(),
            "by_stage": self.count_by_stage(),
            "degraded_pct": pct,
            "alert_degraded_exceeded": alert,
            "alert_message": alert_msg,
            "patches": [r.to_dict() for r in self.records],
        }

    def save_run_ledger(
        self,
        work_dir: Union[str, Path],
        course_id: Optional[str] = None,
        total_items: Optional[int] = None,
    ) -> Path:
        """Writes work/telemetry/patch_ledger.json."""
        if course_id:
            self.course_id = course_id
        p = Path(work_dir).resolve()
        if p.suffix == ".json":
            out_file = p
            out_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            telem_dir = p / "telemetry"
            telem_dir.mkdir(parents=True, exist_ok=True)
            out_file = telem_dir / "patch_ledger.json"

        data = self.to_summary_dict(total_items)
        out_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return out_file

    def generate_cta_review_md(
        self,
        course_id: Optional[str] = None,
        total_items: Optional[int] = None,
    ) -> str:
        """Generates human-readable work/cta_review.md."""
        cid = course_id or self.course_id
        summary = self.count_by_severity()
        alert, pct, alert_msg = self.check_degraded_alert(total_items)

        lines = [
            f"# CTA Automated Repair & Patch Review — {cid}",
            "",
            f"- **Date (UTC):** {datetime.now(timezone.utc).isoformat()}",
            f"- **Total Patches Applied:** {self.total_patches}",
            f"- **Healed (Lossless):** {summary.get('healed', 0)}",
            f"- **Snapped (Normalized):** {summary.get('snapped', 0)}",
            f"- **Degraded (Failsafe):** {summary.get('degraded', 0)} ({pct}%)",
            f"- **Quality Gate:** {'⚠️ FAILED' if alert else '✅ PASSED'} ({alert_msg})",
            "",
            "## 1. Patches Requiring Review (Snapped & Degraded)",
            "",
        ]

        review_items = [r for r in self.records if r.severity in ("snapped", "degraded")]
        if not review_items:
            lines.append("No snapped or degraded patches were applied. All repairs were purely mechanical/lossless.")
            lines.append("")
        else:
            lines.append("| Severity | Layer | Rule ID | Scope | Before | After | Reason / Root Cause |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
            for r in review_items:
                b_str = str(r.before).replace("\n", "\\n").replace("|", "\\|")
                a_str = str(r.after).replace("\n", "\\n").replace("|", "\\|")
                if len(b_str) > 40:
                    b_str = b_str[:37] + "..."
                if len(a_str) > 40:
                    a_str = a_str[:37] + "..."
                lines.append(
                    f"| **{r.severity.upper()}** | {r.layer} | `{r.rule_id}` | `{r.scope}` | `{b_str}` | `{a_str}` | {r.reason} |"
                )
            lines.append("")

        lines.extend([
            "## 2. Mechanical Heals (Summary by Rule)",
            "",
            "| Rule ID | Layer | Count | Description |",
            "| :--- | :--- | :--- | :--- |",
        ])

        rule_counts = self.count_by_rule()
        if not rule_counts:
            lines.append("| None | - | 0 | No mechanical fixes recorded |")
        else:
            for rule_id, count in sorted(rule_counts.items(), key=lambda x: -x[1]):
                # Sample a reason for this rule
                sample_r = next((r for r in self.records if r.rule_id == rule_id), None)
                r_layer = sample_r.layer if sample_r else "L1"
                r_reason = sample_r.reason if sample_r else ""
                lines.append(f"| `{rule_id}` | {r_layer} | {count} | {r_reason} |")
        lines.append("")

        return "\n".join(lines).strip() + "\n"

    def save_cta_review(
        self,
        work_dir: Union[str, Path],
        course_id: Optional[str] = None,
        total_items: Optional[int] = None,
    ) -> Path:
        """Writes work/cta_review.md (or custom md path)."""
        p = Path(work_dir).resolve()
        if p.suffix == ".md":
            out_file = p
            out_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            p.mkdir(parents=True, exist_ok=True)
            out_file = p / "cta_review.md"
        content = self.generate_cta_review_md(course_id, total_items)
        out_file.write_text(content, encoding="utf-8")
        return out_file

    def append_cross_run_record(
        self,
        repo_root: Optional[Union[str, Path]] = None,
        course_id: Optional[str] = None,
        total_items: Optional[int] = None,
    ) -> Path:
        """Appends run summary to reports/c2c_patches/patch_ledger.jsonl (or custom jsonl path)."""
        cid = course_id or self.course_id
        if repo_root and str(repo_root).endswith(".jsonl"):
            jsonl_file = Path(repo_root).resolve()
            jsonl_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            root = Path(repo_root).resolve() if repo_root else Path.cwd().resolve()
            patches_dir = root / "reports" / "c2c_patches"
            patches_dir.mkdir(parents=True, exist_ok=True)
            jsonl_file = patches_dir / "patch_ledger.jsonl"

        alert, pct, _ = self.check_degraded_alert(total_items)
        summary_line = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "course_id": cid,
            "total_patches": self.total_patches,
            "healed": sum(1 for r in self.records if r.severity == "healed"),
            "snapped": sum(1 for r in self.records if r.severity == "snapped"),
            "degraded": sum(1 for r in self.records if r.severity == "degraded"),
            "degraded_pct": pct,
            "alert": alert,
            "by_rule": self.count_by_rule(),
        }

        with open(jsonl_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(summary_line, ensure_ascii=False) + "\n")
        return jsonl_file

    append_cross_run = append_cross_run_record


# Global module singleton for easy access
_GLOBAL_LEDGER = PatchLedger()


def get_ledger() -> PatchLedger:
    return _GLOBAL_LEDGER


def reset_ledger(course_id: str = "custom_course") -> PatchLedger:
    global _GLOBAL_LEDGER
    _GLOBAL_LEDGER = PatchLedger(course_id=course_id)
    return _GLOBAL_LEDGER


def record_patch(
    stage: str,
    layer: str,
    rule_id: str,
    scope: str,
    before: Any,
    after: Any,
    severity: str,
    reason: str,
) -> PatchRecord:
    """Convenience functional interface for recording patches in the global ledger."""
    return _GLOBAL_LEDGER.record_patch(
        stage=stage,
        layer=layer,
        rule_id=rule_id,
        scope=scope,
        before=before,
        after=after,
        severity=severity,
        reason=reason,
    )


def save_run_ledger(
    work_dir: Union[str, Path],
    course_id: Optional[str] = None,
    total_items: Optional[int] = None,
) -> Path:
    return _GLOBAL_LEDGER.save_run_ledger(work_dir, course_id, total_items)


def save_cta_review(
    work_dir: Union[str, Path],
    course_id: Optional[str] = None,
    total_items: Optional[int] = None,
) -> Path:
    return _GLOBAL_LEDGER.save_cta_review(work_dir, course_id, total_items)


def append_cross_run_record(
    repo_root: Optional[Union[str, Path]] = None,
    course_id: Optional[str] = None,
    total_items: Optional[int] = None,
) -> Path:
    return _GLOBAL_LEDGER.append_cross_run_record(repo_root, course_id, total_items)
