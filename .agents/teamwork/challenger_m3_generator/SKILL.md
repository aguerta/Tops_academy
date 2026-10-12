# Content-to-Course Antigravity Skill (Local Copy for challenger_m3_generator)

An automated, psychometrically grounded educational engineering pipeline that converts raw academic PDFs into fully playable, interactive Top's Academy courses.

Key specs for batch generator & psychometrics:
- Volume quotas: >=30 per Skill [Hab], >=20 per Fact/Concept [H/C]
- 3 Interaction Types:
    * multiple_choice_7_options (exactly 7 options, 1 correct, randomized A-G)
    * fill_in_the_blank (canonical LaTeX + accepted_equivalents array)
    * multiple_select (4-6 options, 1 to n-1 correct, binary scoring)
- Psychometric Anti-Giveaway Engine:
    * Per-item length bounding: 0.80 * min(D) <= L_correct <= 1.20 * max(D)
    * Course distribution: L_correct longest in <= 25%, shortest in <= 25%
    * Symmetrical distractor rationales & grammatical parallelism
- Declarative Coordinate Plane vector graphs (axes, curves, points)
- Double-backslash escaped LaTeX: valid JSON without control character corruptions
