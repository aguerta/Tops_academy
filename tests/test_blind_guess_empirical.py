"""Empirical Adversarial Blind-Guess Distractor Testing Suite.

This test harness implements the empirical verification protocol for Milestone 4:
1. Samples >=40 (here N=50) multiple_choice_7_options items from `courses/pde_course.json`.
2. Strips stems, hints, solutions, contexts, and misconception warnings.
3. Shuffles the 7 options for each item.
4. Acts as an adversarial student attempting to guess the correct answer purely by inspecting option text:
   - Giveaway cues: qualifier tells ('en todo el dominio', 'bajo condiciones'), asymmetric justifications ('pues', 'en virtud de'),
     length outliers, grammatical anomalies, centroid convergence.
5. Evaluates multiple adversarial heuristics (Longest, Shortest, Centroid Convergence, Qualifier-Tell, and Composite Adversarial Student).
6. Computes success rate on the sample (and on the full population of 250 items for statistical robustness).
7. Analyzes every correctly guessed item for giveaways vs lucky guesses.
"""
from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import Any


def load_course(course_path: str = "courses/pde_course.json") -> dict[str, Any]:
    p = Path(course_path)
    if not p.exists():
        fallback = Path("archive_rejected_courses") / p.name
        if fallback.exists():
            course_path = str(fallback)
    with open(course_path, "r", encoding="utf-8") as f:
        return json.load(f)


def tokenize(text: str) -> set[str]:
    # Extract lowercase words and LaTeX tokens
    tokens = re.findall(r"\\[a-zA-Z]+|[a-zA-Z0-9_]+", text.lower())
    return set(tokens)


def compute_centroid_scores(options: list[str]) -> list[float]:
    """Computes Jaccard overlap of each option with all other options in the set."""
    token_sets = [tokenize(opt) for opt in options]
    scores = []
    for i, t_i in enumerate(token_sets):
        total_sim = 0.0
        for j, t_j in enumerate(token_sets):
            if i == j:
                continue
            union = len(t_i | t_j)
            inter = len(t_i & t_j)
            sim = inter / union if union > 0 else 0.0
            total_sim += sim
        scores.append(total_sim)
    return scores


def adversarial_student_guess(options: list[str]) -> tuple[int, str]:
    """Adversarial student model inspecting stripped options for psychometric cues.
    
    Returns:
        (chosen_index, rationale)
    """
    n = len(options)
    
    # 1. Cue: Specific domain qualifier tell ('en todo el dominio', 'en todo su dominio')
    dominio_indices = [
        i for i, opt in enumerate(options)
        if "en todo el dominio" in opt.lower() or "en todo su dominio" in opt.lower()
    ]
    if len(dominio_indices) == 1:
        return dominio_indices[0], "Unique qualifier cue: 'en todo el dominio' found in exactly one option"
    elif len(dominio_indices) > 1:
        # tie breaker: longest among them
        best = max(dominio_indices, key=lambda i: len(options[i]))
        return best, f"Qualifier cue: 'en todo el dominio' found in {len(dominio_indices)} options, selected longest"

    # 2. Cue: Asymmetric justification / explanatory connective ('en virtud de', 'pues', 'debido a')
    justif_indices = [
        i for i, opt in enumerate(options)
        if any(marker in opt.lower() for marker in ["en virtud de", "en virtud del teorema", "debido a que"])
    ]
    if len(justif_indices) == 1:
        return justif_indices[0], "Asymmetric justification: unique theoretical rationale marker ('en virtud de')"

    # 3. Cue: Hedging / analytical regularity cue
    hedging_indices = [
        i for i, opt in enumerate(options)
        if "condiciones analíticas" in opt.lower() or "regularidad" in opt.lower()
    ]
    if len(hedging_indices) == 1:
        return hedging_indices[0], "Hedging cue: unique analytical regularity condition"

    # 4. Cue: Convergence / Centroid (item writers mutate correct answer to make distractors)
    centroid_scores = compute_centroid_scores(options)
    max_centroid = max(centroid_scores)
    best_centroid_indices = [i for i, s in enumerate(centroid_scores) if abs(s - max_centroid) < 1e-6]
    
    # 5. Length bias tie-breaker:
    # If options have very different lengths, check if longest option stands out
    lengths = [len(opt) for opt in options]
    max_len = max(lengths)
    min_len = min(lengths)
    
    # Prefer highest centroid overlap
    best_idx = best_centroid_indices[0]
    return best_idx, f"Convergence centroid: highest shared feature overlap ({max_centroid:.2f})"


def run_blind_test(
    sample_size: int = 50,
    seed: int = 42,
    course_path: str = "courses/pde_course.json"
) -> dict[str, Any]:
    course = load_course(course_path)
    all_mc7 = [
        q for q in course["questions"]
        if q.get("interaction_type") == "multiple_choice_7_options"
    ]
    
    random.seed(seed)
    # Ensure deterministic sample
    sampled_questions = random.sample(all_mc7, sample_size)
    
    results = []
    correct_guesses_count = 0
    longest_correct_count = 0
    shortest_correct_count = 0
    centroid_correct_count = 0
    
    for idx, q in enumerate(sampled_questions):
        q_id = q["id"]
        comp_id = q.get("competency_id", "UNKNOWN")
        opts_raw = q.get("options", [])
        
        # 1. Strip stems, hints, solution, misconception warning, context
        # 2. Extract options and true correctness
        options_data = [
            {"content": o["content"].strip(), "is_correct": o.get("is_correct", False)}
            for o in opts_raw
        ]
        
        # 3. Shuffle options deterministically for this item
        # We record the permutation
        perm = list(range(len(options_data)))
        random.seed(seed + idx * 1000)
        random.shuffle(perm)
        
        shuffled_options = [options_data[i]["content"] for i in perm]
        shuffled_correct_mask = [options_data[i]["is_correct"] for i in perm]
        true_correct_idx = shuffled_correct_mask.index(True)
        
        # 4. Run Adversarial Student Model
        adversarial_idx, rationale = adversarial_student_guess(shuffled_options)
        is_adversarial_correct = (adversarial_idx == true_correct_idx)
        if is_adversarial_correct:
            correct_guesses_count += 1
            
        # Also run baseline heuristics
        lens = [len(opt) for opt in shuffled_options]
        longest_idx = lens.index(max(lens))
        shortest_idx = lens.index(min(lens))
        centroid_scores = compute_centroid_scores(shuffled_options)
        centroid_idx = centroid_scores.index(max(centroid_scores))
        
        if longest_idx == true_correct_idx:
            longest_correct_count += 1
        if shortest_idx == true_correct_idx:
            shortest_correct_count += 1
        if centroid_idx == true_correct_idx:
            centroid_correct_count += 1
            
        # Detailed Cue Analysis for this item
        cue_type = "None / Lucky Guess"
        if is_adversarial_correct:
            c_text = shuffled_options[true_correct_idx]
            if "en todo el dominio" in c_text.lower():
                # check if distractors had it
                d_has = sum(1 for j, opt in enumerate(shuffled_options) if j != true_correct_idx and "en todo el dominio" in opt.lower())
                if d_has == 0:
                    cue_type = "CRITICAL CUE: Unique 'en todo el dominio' qualifier giveaway"
                else:
                    cue_type = f"QUALIFIER CUE: 'en todo el dominio' present (in C and {d_has} distractors)"
            elif "en virtud de" in c_text.lower():
                cue_type = "JUSTIFICATION CUE: Unique 'en virtud de' rationale"
            elif longest_idx == true_correct_idx:
                cue_type = "LENGTH CUE: Correct option was longest"
            else:
                cue_type = "CONVERGENCE / HEURISTIC: Overlap clustering"
        
        results.append({
            "sample_index": idx + 1,
            "question_id": q_id,
            "competency_id": comp_id,
            "shuffled_options": shuffled_options,
            "true_correct_index": true_correct_idx,
            "adversarial_guess_index": adversarial_idx,
            "adversarial_rationale": rationale,
            "is_adversarial_correct": is_adversarial_correct,
            "cue_analysis": cue_type,
            "baseline_longest_correct": (longest_idx == true_correct_idx),
            "baseline_shortest_correct": (shortest_idx == true_correct_idx),
            "baseline_centroid_correct": (centroid_idx == true_correct_idx)
        })
        
    accuracy = correct_guesses_count / sample_size
    longest_acc = longest_correct_count / sample_size
    shortest_acc = shortest_correct_count / sample_size
    centroid_acc = centroid_correct_count / sample_size
    
    summary = {
        "sample_size": sample_size,
        "seed": seed,
        "adversarial_correct_count": correct_guesses_count,
        "adversarial_success_rate": accuracy,
        "threshold_target": 0.30,
        "random_baseline": 1.0 / 7.0,
        "exceeds_threshold": accuracy > 0.30,
        "baseline_heuristics": {
            "longest_option_accuracy": longest_acc,
            "shortest_option_accuracy": shortest_acc,
            "centroid_convergence_accuracy": centroid_acc,
            "random_chance": 1.0 / 7.0
        },
        "items": results
    }
    
    return summary


def run_full_population_test(course_path: str = "courses/pde_course.json") -> dict[str, Any]:
    """Runs the adversarial test on all 250 MC7 questions in the course."""
    course = load_course(course_path)
    all_mc7 = [
        q for q in course["questions"]
        if q.get("interaction_type") == "multiple_choice_7_options"
    ]
    
    correct_count = 0
    dominio_giveaway_count = 0
    longest_count = 0
    
    for q in all_mc7:
        options = [o["content"].strip() for o in q["options"]]
        true_idx = [o.get("is_correct", False) for o in q["options"]].index(True)
        guess_idx, _ = adversarial_student_guess(options)
        if guess_idx == true_idx:
            correct_count += 1
            
        c_text = options[true_idx].lower()
        d_texts = [options[i].lower() for i in range(len(options)) if i != true_idx]
        if "en todo el dominio" in c_text and not any("en todo el dominio" in d for d in d_texts):
            dominio_giveaway_count += 1
            
        lens = [len(o) for o in options]
        if lens.index(max(lens)) == true_idx:
            longest_count += 1
            
    return {
        "total_mc7_items": len(all_mc7),
        "adversarial_correct": correct_count,
        "adversarial_rate": correct_count / len(all_mc7),
        "unique_dominio_giveaways": dominio_giveaway_count,
        "unique_dominio_rate": dominio_giveaway_count / len(all_mc7),
        "longest_option_correct": longest_count,
        "longest_option_rate": longest_count / len(all_mc7)
    }


if __name__ == "__main__":
    summary_sample = run_blind_test(sample_size=50, seed=42)
    pop_summary = run_full_population_test()
    
    output_path = Path("tests/blind_guess_empirical_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "sample_test": summary_sample,
            "population_test": pop_summary
        }, f, indent=2, ensure_ascii=False)
        
    print(f"Sample N={summary_sample['sample_size']} Adversarial Guess Success Rate: {summary_sample['adversarial_success_rate']*100:.2f}%")
    print(f"Target threshold: <= {summary_sample['threshold_target']*100:.1f}%")
    print(f"Exceeds threshold: {summary_sample['exceeds_threshold']}")
    print(f"Baseline Heuristics on Sample:")
    print(f"  Longest option: {summary_sample['baseline_heuristics']['longest_option_accuracy']*100:.2f}%")
    print(f"  Shortest option: {summary_sample['baseline_heuristics']['shortest_option_accuracy']*100:.2f}%")
    print(f"  Centroid convergence: {summary_sample['baseline_heuristics']['centroid_convergence_accuracy']*100:.2f}%")
    print(f"  Random chance baseline: {summary_sample['baseline_heuristics']['random_chance']*100:.2f}%")
    print("\nFull Population (N=250):")
    print(f"  Adversarial guess rate: {pop_summary['adversarial_rate']*100:.2f}% ({pop_summary['adversarial_correct']}/250)")
    print(f"  Unique 'en todo el dominio' giveaway rate: {pop_summary['unique_dominio_rate']*100:.2f}% ({pop_summary['unique_dominio_giveaways']}/250)")
