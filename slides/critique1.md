# Critique: m7-tips.qmd and m8-agents.qmd

## Critical

1. **Wrong module cross-references in m7-tips**. Lines 201, 216, 220, 282 reference "Module 2 (portfolio)," "Module 3 (skills)," and "Module 4 (DCF)." Correct numbers: portfolio = M3, DCF = M5, skills = M5/M6.

2. **"AI in code-execution mode doesn't invent facts" is too strong**. Line 121 of m7-tips. LLMs can hallucinate constants in code, fabricated library calls, and facts inside narrative generation. Should qualify: "the *primary* risk shifts from..."

3. **"No analyst needed" in m8 contradicts m7's verification message**. Line 661 of m8. Module 7 spends 10+ slides arguing AI output needs human verification. Reword to "No manual data pulling or formatting needed."

4. **"Cowork" reference in m8 is unexplained**. Line 737. Students have no context for what Cowork is. Remove or introduce it.

## Warning

5. **Title "More Tips" undersells the module**. This covers verification, red-teaming, and critique -- core competency, not tips.

6. **Variance analysis promises decomposition but delivers line-item deltas**. The formula box says "Volume + Price + Mix" but the example only shows net misses. An FP&A-experienced student will notice. Either compute the actual decomposition or remove the formula.

7. **M&A due diligence "single prompt" claim is misleading**. Lines 433-443 of m7-tips. Calling this "M&A Due Diligence" trivializes real deal work. Scope it: "screening-level preliminary analysis."

8. **m8 covers too much for two sessions with no session break indicated**. API + FastAPI + agents + dashboards + pipelines + deployment. Add a divider slide marking where Session 1 ends.

9. **"9+ hours to 15 minutes" ops review comparison is not apples-to-apples**. The "After" omits validation time, agent setup, and edge cases.

10. **Gartner "20%" statistic is unattributed and dated**. From a 2017 forecast, not a measured fact. Cite properly or drop.

11. **AI Memory section is too thin**. One slide for a topic central to the course. Add a concrete CLAUDE.md example.

12. **Haiku/pirate system prompts risk losing MBAs**. Lead with the finance CFO prompt; mention novelty prompts briefly.

13. **ChatGPT is a bad example for "user-supplied API key"**. Line 274 of m8. ChatGPT uses subscription login, not user-supplied keys.

14. **"Later Course Integration: RAG" slide is premature**. Introduces ChromaDB and vector DBs students haven't encountered. Remove or simplify.

## Suggestion

15. **Dashboard replacement section in m8 is repetitive** -- FP&A/Treasury/Portfolio/Executive slides (lines 533-575) could consolidate to one "Examples Across Finance" slide.

16. **Variance analysis in m7 duplicates m8's FP&A dashboard content** -- consider moving it to m8 or removing the overlap.

17. **Agent loop pseudocode has `tool_result` undefined** (line 321 of m8) -- minor but students who try to run it will be confused.
