"""Tests for Milestone 7.4 Weighted Cognitive Sharding, 1-Skill Anti-Straggler SLA, and Wave Dispatch.

Validates:
1. Exact 32-competency distribution of ab30cf91 (6 Fact, 16 Concept, 10 Skill in mixed curriculum order).
   - All 10 Hab-* shards have competency_count == 1.
   - All 10 Hab-* shards are assigned to Wave 1 (wave_index == 1) under max_wave_size = 10.
   - Concept/Fact shards have <= 2 competencies.
   - 100% of 32 competencies are accounted for without duplicates or drops.
2. Edge cases:
   - 1 competency (Skill vs Concept).
   - All-Skill course (all 1-competency shards).
   - Large 45-competency course (total_waves >= 2 with max_wave_size = 10).
   - Legacy explicit k parameter compatibility (preserves uniform partitioning).
3. 3-Fact grouping exception rule (allowed only when all 3 are fact and total N >= 30).
4. DSL_REFERENCE updates (@var@ tokens in raw strings, stem_variants, shard_fixes).
"""

import json
import math
from pathlib import Path
import pytest

import sys
_skill_dir = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_dir) not in sys.path:
    sys.path.insert(0, str(_skill_dir))

from plan_shards import (
    DEFAULT_COMPS_PER_SHARD,
    DEFAULT_MAX_WAVE_SIZE,
    DSL_REFERENCE,
    calculate_competency_weight,
    determine_shard_count,
    is_concept_competency,
    is_fact_competency,
    is_skill_competency,
    main,
    partition_competencies_into_shards,
    partition_competencies_weighted,
    plan_shards,
)


def _build_test_cta(competencies, course_id="test_course"):
    return {
        "course_id": course_id,
        "title": f"Course {course_id}",
        "description": "Test Course Description",
        "competencies": competencies,
    }


def _seed_workspace(tmp_path, competencies, course_id="test_course"):
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)

    cta_path = work_dir / "cta.json"
    cta_data = _build_test_cta(competencies, course_id)
    cta_path.write_text(json.dumps(cta_data, indent=2), encoding="utf-8")

    pre_cta_path = work_dir / "pre_cta_manifest.json"
    pre_cta_data = {
        "course_id": course_id,
        "cta_mode": "direct",
        "total_files": 1,
        "files": [{"doc": "doc.pdf", "type": "pdf"}],
        "documents": [{"doc_name": "doc.pdf", "path": "content/doc.pdf"}],
    }
    pre_cta_path.write_text(json.dumps(pre_cta_data, indent=2), encoding="utf-8")

    return cta_path, shards_dir


def _make_ab30cf91_competencies():
    """Exact 32-competency curriculum from the ab30cf91 audit.
    
    Order:
      H-01, C-01, C-02, Hab-01, H-02, Hab-02, C-03, C-04, H-03, C-05,
      Hab-03, Hab-04, C-06, Hab-05, C-07, C-08, H-04, C-09, Hab-06, C-10,
      C-11, C-12, Hab-07, H-05, C-13, C-14, Hab-08, Hab-09, C-15, C-16,
      H-06, Hab-10
    """
    spec = [
        ("H-01", "fact"), ("C-01", "concept"),
        ("C-02", "concept"), ("Hab-01", "skill"),
        ("H-02", "fact"), ("Hab-02", "skill"),
        ("C-03", "concept"), ("C-04", "concept"),
        ("H-03", "fact"), ("C-05", "concept"),
        ("Hab-03", "skill"), ("Hab-04", "skill"),
        ("C-06", "concept"), ("Hab-05", "skill"),
        ("C-07", "concept"), ("C-08", "concept"),
        ("H-04", "fact"), ("C-09", "concept"),
        ("Hab-06", "skill"), ("C-10", "concept"),
        ("C-11", "concept"), ("C-12", "concept"),
        ("Hab-07", "skill"), ("H-05", "fact"),
        ("C-13", "concept"), ("C-14", "concept"),
        ("Hab-08", "skill"), ("Hab-09", "skill"),
        ("C-15", "concept"), ("C-16", "concept"),
        ("H-06", "fact"), ("Hab-10", "skill"),
    ]
    comps = []
    for cid, ctype in spec:
        comps.append({
            "id": cid,
            "name": f"Competency {cid}",
            "type": ctype,
            "distractors": [{"id": f"D-{cid}-{i:02d}", "evidence": {"doc": "doc.pdf"}} for i in range(1, 7)],
            "evidence": [{"doc": "doc.pdf"}],
        })
    return comps


# =============================================================================
# 1. CORE TEST: ab30cf91 Weighted Cognitive Sharding & Wave Dispatch
# =============================================================================

class TestWeightedShardingAb30cf91:
    """Validates the 32-competency distribution of ab30cf91 under Milestone 7.4 rules."""

    def test_ab30cf91_anti_straggler_isolation_and_wave_1(self, tmp_path):
        """Verifies that all 10 Hab-* skills are isolated to 1-comp shards and sit in Wave 1."""
        comps = _make_ab30cf91_competencies()
        assert len(comps) == 32
        facts = [c for c in comps if c["type"] == "fact"]
        concepts = [c for c in comps if c["type"] == "concept"]
        skills = [c for c in comps if c["type"] == "skill"]
        assert len(facts) == 6
        assert len(concepts) == 16
        assert len(skills) == 10

        cta_path, shards_dir = _seed_workspace(tmp_path, comps, course_id="ab30cf91_course")

        # Execute plan_shards with default max_wave_size = 10
        manifest = plan_shards(cta_path, shards_dir, max_wave_size=10)

        assert manifest["total_competencies"] == 32
        shards = manifest["shards"]
        assert len(shards) == manifest["total_shards"]

        # Collect all sharded competency IDs
        all_sharded_ids = []
        hab_shards = []
        concept_fact_shards = []

        for s in shards:
            cids = s["competency_ids"]
            all_sharded_ids.extend(cids)
            # Check if shard contains a skill
            if any(cid.startswith("Hab-") for cid in cids):
                hab_shards.append(s)
            else:
                concept_fact_shards.append(s)

        # 1. Hard Skill Isolation Rule: Every Hab-* competency MUST be in its own exclusive 1-comp shard
        assert len(hab_shards) == 10, f"Expected exactly 10 Hab shards, got {len(hab_shards)}"
        for s in hab_shards:
            assert s["competency_count"] == 1, f"Skill shard {s['shard_id']} had {s['competency_count']} comps"
            assert len(s["competency_ids"]) == 1
            cid = s["competency_ids"][0]
            assert cid.startswith("Hab-"), f"Unexpected non-skill in hab_shard: {cid}"

        # 2. Heaviest-First Wave 1 Rule: All 10 Hab-* shards MUST be assigned to Wave 1 (wave_index == 1)
        # Because max_wave_size = 10 and shards are sorted heaviest first (Hab weights = 6.6 > Concept weights <= 6.2)
        wave_1_shards = [s for s in shards if s["wave_index"] == 1]
        assert len(wave_1_shards) == 10, f"Expected 10 shards in Wave 1, got {len(wave_1_shards)}"
        for s in wave_1_shards:
            assert s["competency_count"] == 1
            assert s["competency_ids"][0].startswith("Hab-"), f"Non-skill {s['competency_ids']} found in Wave 1"

        # 3. Concept/Fact shards have <= 2 competencies
        for s in concept_fact_shards:
            assert s["competency_count"] <= 2, f"Concept/Fact shard {s['shard_id']} had {s['competency_count']} comps"
            assert len(s["competencies"]) <= 2

        # 4. 100% of 32 competencies accounted for without duplicates or drops
        assert len(all_sharded_ids) == 32
        assert len(set(all_sharded_ids)) == 32
        assert set(all_sharded_ids) == {c["id"] for c in comps}

        # 5. Manifest and shard JSON verification
        assert manifest["total_waves"] == math.ceil(len(shards) / 10)
        assert len(manifest["waves"]) == manifest["total_waves"]
        assert manifest["max_wave_size"] == 10

        # Verify physical files written
        pre_shard_file = shards_dir / "pre_shard_manifest.json"
        assert pre_shard_file.is_file()
        for s in shards:
            s_file = shards_dir / f"{s['shard_id']}.json"
            assert s_file.is_file()
            data = json.loads(s_file.read_text(encoding="utf-8"))
            assert data["shard_id"] == s["shard_id"]
            assert data["wave_index"] == s["wave_index"]
            assert data["weight"] == s["weight"]
            assert "dsl_reference" in data


# =============================================================================
# 2. EDGE CASES & ADVERSARIAL SIZES
# =============================================================================

class TestWeightedShardingEdgeCases:
    """Verifies edge cases: 1 competency, all-skill, large 45-comp course, and legacy overrides."""

    def test_single_competency_concept(self, tmp_path):
        """Single concept course produces 1 shard in Wave 1."""
        comps = [{"id": "C-01", "name": "Solo Concept", "type": "concept", "distractors": []}]
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "single_concept")

        manifest = plan_shards(cta_path, shards_dir)
        assert manifest["total_competencies"] == 1
        assert manifest["total_shards"] == 1
        assert manifest["total_waves"] == 1

        s0 = manifest["shards"][0]
        assert s0["shard_id"] == "shard_01"
        assert s0["competency_count"] == 1
        assert s0["wave_index"] == 1

    def test_single_competency_skill(self, tmp_path):
        """Single skill course produces 1 shard in Wave 1."""
        comps = [{"id": "Hab-01", "name": "Solo Skill", "type": "skill", "distractors": []}]
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "single_skill")

        manifest = plan_shards(cta_path, shards_dir)
        assert manifest["total_competencies"] == 1
        assert manifest["total_shards"] == 1
        assert manifest["total_waves"] == 1

        s0 = manifest["shards"][0]
        assert s0["shard_id"] == "shard_01"
        assert s0["competency_count"] == 1
        assert s0["wave_index"] == 1

    def test_all_skill_course(self, tmp_path):
        """A course with 8 skills produces 8 exclusive 1-competency shards."""
        comps = [
            {"id": f"Hab-{i:02d}", "name": f"Skill {i}", "type": "skill", "distractors": []}
            for i in range(1, 9)
        ]
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "all_skills")

        manifest = plan_shards(cta_path, shards_dir, max_wave_size=10)
        assert manifest["total_competencies"] == 8
        assert manifest["total_shards"] == 8
        assert manifest["total_waves"] == 1
        for s in manifest["shards"]:
            assert s["competency_count"] == 1
            assert s["wave_index"] == 1

    def test_large_45_competency_course_multi_wave(self, tmp_path):
        """45 competencies (15 skills, 20 concepts, 10 facts) produces total_waves >= 2."""
        comps = []
        # Mixed curriculum: 15 skills, 20 concepts, 10 facts
        for i in range(1, 16):
            comps.append({"id": f"C-{i:02d}", "name": f"Concept {i}", "type": "concept", "distractors": []})
            comps.append({"id": f"Hab-{i:02d}", "name": f"Skill {i}", "type": "skill", "distractors": []})
        for i in range(1, 11):
            comps.append({"id": f"H-{i:02d}", "name": f"Fact {i}", "type": "fact", "distractors": []})
        for i in range(16, 21):
            comps.append({"id": f"C-{i:02d}", "name": f"Concept {i}", "type": "concept", "distractors": []})

        assert len(comps) == 45
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "large_45_course")

        manifest = plan_shards(cta_path, shards_dir, max_wave_size=10)

        assert manifest["total_competencies"] == 45
        assert manifest["total_waves"] >= 2
        assert manifest["max_wave_size"] == 10

        # Shards in Wave 1 must be exactly 10 and all must be Skills (heaviest-first)
        wave_1_shards = [s for s in manifest["shards"] if s["wave_index"] == 1]
        assert len(wave_1_shards) == 10
        for s in wave_1_shards:
            assert s["competency_count"] == 1
            assert s["competency_ids"][0].startswith("Hab-")

        # Wave 2 should contain the remaining 5 skills plus the first non-skills
        wave_2_shards = [s for s in manifest["shards"] if s["wave_index"] == 2]
        assert len(wave_2_shards) == 10
        skills_in_wave_2 = [s for s in wave_2_shards if s["competency_ids"][0].startswith("Hab-")]
        assert len(skills_in_wave_2) == 5

        # All 15 skills across the curriculum must have competency_count == 1
        all_skills = [s for s in manifest["shards"] if any(cid.startswith("Hab-") for cid in s["competency_ids"])]
        assert len(all_skills) == 15
        assert all(s["competency_count"] == 1 for s in all_skills)

        # 100% accountability
        all_ids = []
        for s in manifest["shards"]:
            all_ids.extend(s["competency_ids"])
        assert len(all_ids) == 45
        assert set(all_ids) == {c["id"] for c in comps}

    def test_legacy_explicit_k_override(self, tmp_path):
        """Passing an explicit k parameter preserves legacy uniform partitioning."""
        comps = [
            {"id": f"C-{i:02d}", "name": f"Concept {i}", "type": "concept", "distractors": []}
            for i in range(1, 25)
        ]
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "legacy_k")

        # Explicitly request k = 4
        manifest = plan_shards(cta_path, shards_dir, k=4)
        assert manifest["total_shards"] == 4
        for s in manifest["shards"]:
            # 24 / 4 = 6 per shard
            assert s["competency_count"] == 6

    def test_no_isolate_skills_flag(self, tmp_path):
        """Setting isolate_skills=False falls back to legacy uniform partitioning."""
        comps = [
            {"id": f"Hab-{i:02d}", "name": f"Skill {i}", "type": "skill", "distractors": []}
            for i in range(1, 9)
        ]
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "no_isolate")

        manifest = plan_shards(cta_path, shards_dir, isolate_skills=False, max_comps=2)
        # In legacy mode with max_comps=2, 8 comps -> 4 shards of 2 comps each
        assert manifest["total_shards"] == 4
        for s in manifest["shards"]:
            assert s["competency_count"] == 2


# =============================================================================
# 3. THREE-FACT GROUPING EXCEPTION RULE (N >= 30)
# =============================================================================

class TestThreeFactGroupingRule:
    """Verifies that up to 3 competencies per shard is allowed ONLY when all 3 are fact and N >= 30."""

    def test_three_facts_grouped_when_n_ge_30(self):
        """When total competencies N >= 30, a run of 3 facts is grouped into a 3-fact shard."""
        # 3 facts + 27 concepts = 30 competencies
        comps = [{"id": f"H-{i:02d}", "name": f"Fact {i}", "type": "fact"} for i in range(1, 4)]
        comps += [{"id": f"C-{i:02d}", "name": f"Concept {i}", "type": "concept"} for i in range(1, 28)]
        assert len(comps) == 30

        raw_shards = partition_competencies_weighted(comps)
        # Look for the shard containing H-01
        h_shards = [s for s in raw_shards if "H-01" in s["competency_ids"]]
        assert len(h_shards) == 1
        h_shard = h_shards[0]
        assert h_shard["competency_ids"] == ["H-01", "H-02", "H-03"]
        assert len(h_shard["competencies"]) == 3

    def test_three_facts_not_grouped_when_n_lt_30(self):
        """When total competencies N < 30, max 2 competencies per shard is strictly enforced."""
        # 3 facts + 12 concepts = 15 competencies (< 30)
        comps = [{"id": f"H-{i:02d}", "name": f"Fact {i}", "type": "fact"} for i in range(1, 4)]
        comps += [{"id": f"C-{i:02d}", "name": f"Concept {i}", "type": "concept"} for i in range(1, 13)]
        assert len(comps) == 15

        raw_shards = partition_competencies_weighted(comps)
        # All shards must have <= 2 competencies
        for s in raw_shards:
            assert len(s["competency_ids"]) <= 2

    def test_mixed_triplet_not_grouped_into_three(self):
        """Even with N >= 30, if any competency in the triplet is a concept, max 2 is enforced."""
        # 2 facts + 1 concept at the start, total N = 30
        comps = [
            {"id": "H-01", "type": "fact"},
            {"id": "H-02", "type": "fact"},
            {"id": "C-01", "type": "concept"},
        ]
        comps += [{"id": f"C-{i:02d}", "name": f"Concept {i}", "type": "concept"} for i in range(2, 29)]
        assert len(comps) == 30

        raw_shards = partition_competencies_weighted(comps)
        first_shard = raw_shards[0]
        # Must NOT group all 3 together because C-01 is a concept
        assert len(first_shard["competency_ids"]) <= 2


# =============================================================================
# 4. DSL REFERENCE & CONTRACT SPECIFICATIONS
# =============================================================================

class TestDslReferenceUpdates:
    """Verifies that DSL_REFERENCE embeds the required syntax rules."""

    def test_dsl_reference_orthogonal_tokens(self):
        """Must teach @var@ and @var:fmt@ tokens in raw strings r'...' and forbid rf'...'."""
        rules = DSL_REFERENCE["rules"]
        assert "orthogonal_tokens_raw_strings" in rules
        rule_text = rules["orthogonal_tokens_raw_strings"]
        assert "@var@" in rule_text
        assert "@var:fmt@" in rule_text
        assert "PROHIBIDO usar rf" in rule_text

    def test_dsl_reference_mandatory_stem_variants(self):
        """Must require 3-5 stem_variants for diversity ratio >= 0.50."""
        rules = DSL_REFERENCE["rules"]
        assert "tpl_var_mandatory" in rules
        rule_text = rules["tpl_var_mandatory"]
        assert "3 y 5" in rule_text
        assert "stem_variants" in rule_text

    def test_dsl_reference_modular_overrides(self):
        """Must document modular per-competency overrides via shard_fixes/<CID>.py."""
        rules = DSL_REFERENCE["rules"]
        assert "modular_per_comp_overrides" in rules
        rule_text = rules["modular_per_comp_overrides"]
        assert "shard_fixes/<CID>.py" in rule_text


# =============================================================================
# 5. ADVERSARIAL INPUTS & GRACEFUL ERROR HANDLING
# =============================================================================

class TestAdversarialInputsAndGracefulFailures:
    """Verifies robustness against malformed CTA files, missing inputs, and boundary conditions."""

    def test_empty_competencies_raises_value_error(self, tmp_path):
        """CTA with empty competencies list raises ValueError with clean message."""
        cta_path, shards_dir = _seed_workspace(tmp_path, [], "empty_course")
        with pytest.raises(ValueError, match="cta.json contains zero competencies"):
            plan_shards(cta_path, shards_dir)

    def test_missing_competencies_key_raises_value_error(self, tmp_path):
        """CTA without competencies key raises ValueError."""
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        cta_path = work_dir / "cta.json"
        cta_path.write_text(json.dumps({"course_id": "no_comps"}), encoding="utf-8")
        pre_cta = work_dir / "pre_cta_manifest.json"
        pre_cta.write_text(json.dumps({"files": []}), encoding="utf-8")

        with pytest.raises(ValueError, match="cta.json contains zero competencies"):
            plan_shards(cta_path, shards_dir)

    def test_dict_based_competencies_format(self, tmp_path):
        """CTA with competencies as a dict of objects is parsed and sharded seamlessly."""
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        cta_dict = {
            "course_id": "dict_course",
            "competencies": {
                "C-01": {"name": "Concept 1", "type": "concept", "distractors": []},
                "Hab-01": {"name": "Skill 1", "type": "skill", "distractors": []},
                "H-01": {"name": "Fact 1", "type": "fact", "distractors": []},
            },
        }
        cta_path = work_dir / "cta.json"
        cta_path.write_text(json.dumps(cta_dict, indent=2), encoding="utf-8")
        pre_cta = work_dir / "pre_cta_manifest.json"
        pre_cta.write_text(json.dumps({"files": []}), encoding="utf-8")

        manifest = plan_shards(cta_path, shards_dir)
        assert manifest["total_competencies"] == 3
        # 1 skill shard (Hab-01) + 1 non-skill shard (C-01, H-01) = 2 shards
        assert manifest["total_shards"] == 2
        skill_shard = manifest["shards"][0]
        assert skill_shard["competency_ids"] == ["Hab-01"]
        assert skill_shard["competency_count"] == 1

    def test_missing_cta_file_raises_filenotfound(self, tmp_path):
        """Missing cta.json file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="CTA file does not exist"):
            plan_shards(tmp_path / "nonexistent_cta.json", tmp_path / "shards")

    def test_missing_pre_cta_manifest_raises_blocker(self, tmp_path):
        """Missing pre_cta_manifest.json raises FileNotFoundError with BLOCKER:: format."""
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        cta_path = work_dir / "cta.json"
        cta_data = _build_test_cta([{"id": "C-01", "type": "concept"}])
        cta_path.write_text(json.dumps(cta_data), encoding="utf-8")

        with pytest.raises(FileNotFoundError, match="BLOCKER:: No existe pre_cta_manifest.json"):
            plan_shards(cta_path, shards_dir)


# =============================================================================
# 6. TYPE AND ID DISAMBIGUATION & ADVERSARIAL METADATA
# =============================================================================

class TestTypeAndIdDisambiguation:
    """Tests multilingual recognition (Spanish/English), case-insensitivity, and safe fallback."""

    def test_multilingual_skill_isolation(self, tmp_path):
        """Competencies declared with Spanish 'habilidad' or uppercase 'SKILL' are strictly isolated."""
        comps = [
            {"id": "SKILL-01", "name": "Uppercase Skill", "type": "SKILL"},
            {"id": "c-99", "name": "Spanish Skill", "type": "habilidad"},
            {"id": "hab_03", "name": "Underscore Skill", "type": "skills"},
            {"id": "HAB04", "name": "Concatenated Skill", "type": "habilidades"},
            {"id": "C-01", "name": "Ordinary Concept", "type": "concept"},
            {"id": "H-01", "name": "Ordinary Fact", "type": "fact"},
        ]
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "multilingual_course")

        manifest = plan_shards(cta_path, shards_dir, max_wave_size=10)
        assert manifest["total_competencies"] == 6

        # The 4 skills must all be isolated into 1-comp shards
        skill_cids = {"SKILL-01", "c-99", "hab_03", "HAB04"}
        for s in manifest["shards"]:
            if any(cid in skill_cids for cid in s["competency_ids"]):
                assert s["competency_count"] == 1
                assert s["competency_ids"][0] in skill_cids
                assert s["wave_index"] == 1

        # Non-skills (C-01, H-01) must be grouped together into 1 shard
        non_skill_shards = [s for s in manifest["shards"] if not any(cid in skill_cids for cid in s["competency_ids"])]
        assert len(non_skill_shards) == 1
        assert set(non_skill_shards[0]["competency_ids"]) == {"C-01", "H-01"}

    def test_multilingual_fact_and_concept_detection(self):
        """Verifies helper recognition for Spanish, plural, and underscore identifiers."""
        assert is_fact_competency({"id": "HECHO-01", "type": "hecho"})
        assert is_fact_competency({"id": "H_02", "type": "facts"})
        assert is_fact_competency({"id": "FACT-03", "type": "fact"})

        assert is_concept_competency({"id": "CONCEPTO-01", "type": "concepto"})
        assert is_concept_competency({"id": "C_02", "type": "concepts"})
        assert is_concept_competency({"id": "CONCEPT-03", "type": "concept"})

        # Skills must never be mistaken for facts or concepts
        skill_comp = {"id": "H-HAB-01", "type": "skill"}
        assert is_skill_competency(skill_comp)
        assert not is_fact_competency(skill_comp)
        assert not is_concept_competency(skill_comp)

    def test_distractor_none_or_malformed_weight_calculation(self):
        """Handles None or invalid type for distractors gracefully without crashing."""
        comp_none_d = {"id": "C-01", "type": "concept", "distractors": None}
        assert calculate_competency_weight(comp_none_d) == 2.5

        comp_dict_d = {"id": "Hab-01", "type": "skill", "distractors": "invalid_type"}
        assert calculate_competency_weight(comp_dict_d) == 6.0

        comp_missing_d = {"id": "H-01", "type": "fact"}
        assert calculate_competency_weight(comp_missing_d) == 1.5


# =============================================================================
# 7. WAVE SIZING BOUNDARIES & LIMITS
# =============================================================================

class TestWaveSizingAndLimits:
    """Verifies edge cases in wave computation: max_wave_size 1, 5, 0, and waves summary payload."""

    def test_max_wave_size_one(self, tmp_path):
        """Setting max_wave_size=1 creates a distinct wave for each individual shard."""
        comps = [
            {"id": f"Hab-{i:02d}", "type": "skill"} for i in range(1, 4)
        ] + [
            {"id": f"C-{i:02d}", "type": "concept"} for i in range(1, 5)
        ]
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "wave_size_one")

        manifest = plan_shards(cta_path, shards_dir, max_wave_size=1)
        total_shards = manifest["total_shards"]
        assert total_shards == 3 + 2  # 3 skills + 2 concept shards (4/2 = 2) = 5 shards
        assert manifest["total_waves"] == 5
        assert len(manifest["waves"]) == 5

        for idx, s in enumerate(manifest["shards"], start=1):
            assert s["wave_index"] == idx
            assert manifest["waves"][idx - 1]["wave_index"] == idx
            assert manifest["waves"][idx - 1]["shard_count"] == 1
            assert manifest["waves"][idx - 1]["shard_ids"] == [s["shard_id"]]

    def test_max_wave_size_zero_or_negative_fallback(self, tmp_path):
        """max_wave_size <= 0 falls back to DEFAULT_MAX_WAVE_SIZE without division by zero."""
        comps = [{"id": f"C-{i:02d}", "type": "concept"} for i in range(1, 15)]
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "wave_size_zero")

        manifest_zero = plan_shards(cta_path, shards_dir, max_wave_size=0)
        assert manifest_zero["max_wave_size"] == DEFAULT_MAX_WAVE_SIZE

        manifest_neg = plan_shards(cta_path, shards_dir, max_wave_size=-5)
        assert manifest_neg["max_wave_size"] == DEFAULT_MAX_WAVE_SIZE


# =============================================================================
# 8. CONSECUTIVE SKILLS ISOLATION & TIE-BREAKING
# =============================================================================

class TestConsecutiveSkillsAndTieBreaking:
    """Verifies consecutive skills isolation (e.g. Hab-03, Hab-04) and deterministic ordering."""

    def test_consecutive_skills_remain_isolated(self, tmp_path):
        """Consecutive skills Hab-01, Hab-02, Hab-03 in curriculum must each have competency_count == 1."""
        comps = [
            {"id": "Hab-01", "type": "skill"},
            {"id": "Hab-02", "type": "skill"},
            {"id": "Hab-03", "type": "skill"},
            {"id": "C-01", "type": "concept"},
            {"id": "C-02", "type": "concept"},
        ]
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "consecutive_skills")

        manifest = plan_shards(cta_path, shards_dir)
        skill_shards = [s for s in manifest["shards"] if s["competency_ids"][0].startswith("Hab-")]
        assert len(skill_shards) == 3
        for s in skill_shards:
            assert s["competency_count"] == 1
            assert s["wave_index"] == 1

    def test_deterministic_tie_breaking(self):
        """Shards with identical weights break ties deterministically by min_curriculum_idx."""
        comps = [
            {"id": "C-01", "type": "concept", "distractors": [{"id": "D1"}, {"id": "D2"}]},
            {"id": "C-02", "type": "concept", "distractors": [{"id": "D1"}, {"id": "D2"}]},
            {"id": "C-03", "type": "concept", "distractors": [{"id": "D1"}, {"id": "D2"}]},
            {"id": "C-04", "type": "concept", "distractors": [{"id": "D1"}, {"id": "D2"}]},
        ]
        # All 4 have identical weights. Grouping (C-01, C-02) and (C-03, C-04) both have weight 5.4.
        raw_shards = partition_competencies_weighted(comps)
        raw_shards.sort(key=lambda s: (0 if s.get("is_skill") else 1, -s["weight"], s.get("min_curriculum_idx", 0)))

        assert raw_shards[0]["competency_ids"] == ["C-01", "C-02"]
        assert raw_shards[1]["competency_ids"] == ["C-03", "C-04"]


# =============================================================================
# 9. PARAMETRIC OVERRIDE: CASE 2A (max_comps = 3)
# =============================================================================

class TestCase2AParametricOverride:
    """Verifies that setting max_comps=3 groups up to 3 non-skills while still isolating skills."""

    def test_case_2a_groups_three_concepts(self, tmp_path):
        """Under Case 2A (max_comps=3), 6 concepts group into 2 shards of 3."""
        comps = [
            {"id": f"C-{i:02d}", "type": "concept"} for i in range(1, 7)
        ] + [
            {"id": "Hab-01", "type": "skill"}
        ]
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "case_2a_course")

        manifest = plan_shards(cta_path, shards_dir, max_comps=3)
        # 1 skill shard (Hab-01) + 2 concept shards (3 each) = 3 shards
        assert manifest["total_shards"] == 3
        concept_shards = [s for s in manifest["shards"] if not s["competency_ids"][0].startswith("Hab-")]
        assert len(concept_shards) == 2
        for s in concept_shards:
            assert s["competency_count"] == 3

        skill_shard = [s for s in manifest["shards"] if s["competency_ids"][0] == "Hab-01"][0]
        assert skill_shard["competency_count"] == 1


# =============================================================================
# 10. CLI MAIN INVOCATION
# =============================================================================

class TestCliMainInvocation:
    """Tests the CLI entry point main() with various command-line arguments."""

    def test_cli_main_success(self, tmp_path, monkeypatch, capsys):
        """CLI invocation executes cleanly and outputs shard details with total waves."""
        comps = _make_ab30cf91_competencies()
        cta_path, shards_dir = _seed_workspace(tmp_path, comps, "cli_course")

        test_args = [
            "plan_shards.py",
            "--cta", str(cta_path),
            "--output-dir", str(shards_dir),
            "--max-wave-size", "8",
        ]
        monkeypatch.setattr("sys.argv", test_args)

        main()

        captured = capsys.readouterr()
        assert "Successfully partitioned 32 competencies" in captured.out
        assert "total waves: 3" in captured.out
        assert "(wave 1)" in captured.out

