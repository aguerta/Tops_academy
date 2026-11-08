"""Single Source of Truth for Inter-Stage Contracts and Schemas.

Provides unified Pydantic v2 schemas and normalization helpers for:
- ArtifactCertificate: Cryptographic proof of build and stage completion
- CompileAttemptRecord: Shard compilation attempt tracking
- RejectionSpec: Unified rejection spec with bidirectional key synchronization
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class ArtifactCertificate(BaseModel):
    """Cryptographic certificate attesting stage execution and integrity."""

    schema_version: int = Field(default=1)
    stage: str
    artifact_id: str
    source_sha256: str
    cta_sha256: str = Field(default="")
    compiler_sha256: str = Field(default="")
    contract_version: int = Field(default=2)
    template_shas: Dict[str, str] = Field(default_factory=dict)
    passed_50_seeds: bool = Field(default=True)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    cert_sha256: str = Field(default="")

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of certificate payload excluding cert_sha256."""
        payload = {
            "schema_version": self.schema_version,
            "stage": self.stage,
            "artifact_id": self.artifact_id,
            "source_sha256": self.source_sha256,
            "cta_sha256": self.cta_sha256,
            "compiler_sha256": self.compiler_sha256,
            "contract_version": self.contract_version,
            "template_shas": sorted(self.template_shas.items()),
            "passed_50_seeds": self.passed_50_seeds,
            "created_at": self.created_at,
        }
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def seal(self) -> ArtifactCertificate:
        """Seal certificate with its own cryptographic hash."""
        self.cert_sha256 = self.compute_hash()
        return self


def write_certificate(
    cert_path: Union[str, Path],
    cert: Union[ArtifactCertificate, Dict[str, Any]],
) -> Path:
    """Writes ArtifactCertificate to target path with cryptographic seal."""
    path = Path(cert_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(cert, dict):
        cert_obj = ArtifactCertificate(**cert)
    else:
        cert_obj = cert
    cert_obj.seal()
    dumped = cert_obj.model_dump()
    path.write_text(json.dumps(dumped, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def verify_certificate(
    cert_path: Union[str, Path],
    expected_source_bytes: Optional[bytes] = None,
    expected_source_path: Optional[Union[str, Path]] = None,
) -> bool:
    """Verifies certificate integrity, seal hash, and matching source SHA-256."""
    path = Path(cert_path)
    if not path.is_file():
        return False
    try:
        raw_data = json.loads(path.read_text(encoding="utf-8"))
        cert = ArtifactCertificate(**raw_data)
        if cert.cert_sha256 and cert.compute_hash() != cert.cert_sha256:
            return False

        if expected_source_bytes is not None:
            actual_sha = hashlib.sha256(expected_source_bytes).hexdigest()
            if actual_sha != cert.source_sha256:
                return False

        if expected_source_path is not None:
            sp = Path(expected_source_path)
            if not sp.is_file():
                return False
            actual_sha = hashlib.sha256(sp.read_bytes()).hexdigest()
            if actual_sha != cert.source_sha256:
                return False

        return True
    except Exception:
        return False


class CompileAttemptRecord(BaseModel):
    """Tracks a single compilation attempt for a shard or template set."""

    attempt: int
    passed: bool
    error_count: int = Field(default=0)
    affected_line_count: int = Field(default=0)
    has_syntax_error: bool = Field(default=False)
    error_sha256: str = Field(default="")
    errors: List[str] = Field(default_factory=list)

    @field_validator("error_sha256", mode="before")
    @classmethod
    def compute_error_hash_if_empty(cls, v: str, info: Any) -> str:
        if v:
            return v
        return ""


class RejectionSpec(BaseModel):
    """Unified rejection specification across template checks and publisher gates.
    
    Guarantees dual-key presence and synchronization:
    - failing_shards <-> affected_shards
    - grouped_by_rule <-> groups
    - status is strictly normalized to uppercase 'REJECTED'
    """

    status: str = Field(default="REJECTED")
    course_id: str = Field(default="")
    total_issues: int = Field(default=0)
    consolidated_blocks: int = Field(default=0)
    failing_competencies: List[str] = Field(default_factory=list)
    failing_shards: List[str] = Field(default_factory=list)
    affected_shards: List[str] = Field(default_factory=list)
    specific_error_report_path: str = Field(default="")
    proposed_repair_command: str = Field(default="")
    followup_commands: List[str] = Field(default_factory=list)
    gate_failures: List[str] = Field(default_factory=list)
    grouped_by_rule: Dict[str, Any] = Field(default_factory=dict)
    groups: Dict[str, Any] = Field(default_factory=dict)
    diagnostics_by_competency: Dict[str, Any] = Field(default_factory=dict)
    report_text: str = Field(default="")

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, v: Any) -> str:
        return "REJECTED"

    @model_validator(mode="before")
    @classmethod
    def synchronize_dual_keys(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        # Normalize status to uppercase REJECTED
        data["status"] = "REJECTED"

        # Synchronize failing_shards and affected_shards
        shards_pool: Set[str] = set()
        for k in ("failing_shards", "affected_shards"):
            val = data.get(k)
            if isinstance(val, list):
                for item in val:
                    if item:
                        shards_pool.add(str(item))
            elif isinstance(val, str) and val.strip():
                shards_pool.add(val.strip())

        unified_shards = sorted(list(shards_pool))
        data["failing_shards"] = unified_shards
        data["affected_shards"] = unified_shards

        # Synchronize grouped_by_rule and groups
        g_rule = data.get("grouped_by_rule")
        g_groups = data.get("groups")
        chosen_groups = {}
        if isinstance(g_rule, dict) and g_rule:
            chosen_groups = g_rule
        elif isinstance(g_groups, dict) and g_groups:
            chosen_groups = g_groups

        data["grouped_by_rule"] = chosen_groups
        data["groups"] = chosen_groups

        if not isinstance(data.get("diagnostics_by_competency"), dict):
            data["diagnostics_by_competency"] = {}

        return data

    def to_dict(self) -> Dict[str, Any]:
        """Serializes rejection spec with dual keys synchronized."""
        dumped = self.model_dump()
        dumped["status"] = "REJECTED"
        dumped["failing_shards"] = sorted(self.failing_shards)
        dumped["affected_shards"] = sorted(self.failing_shards)
        dumped["grouped_by_rule"] = self.grouped_by_rule
        dumped["groups"] = self.grouped_by_rule
        return dumped

    def write_json(self, path: Union[str, Path]) -> Path:
        """Writes JSON to disk ensuring parent directories exist."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return p

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RejectionSpec:
        """Creates RejectionSpec instance from dictionary."""
        return cls(**data)

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> RejectionSpec:
        """Loads and normalizes RejectionSpec from JSON file."""
        p = Path(path)
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls(**data)
