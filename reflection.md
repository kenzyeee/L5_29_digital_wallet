# Reflection

The supplied handout contains learning outcomes about static analysis, but no separate list of reflection questions. These four responses address those outcomes directly.

1. **How does static analysis help code quality?** It checks source without needing test inputs and points out repeatable problems in security, correctness, and style. That gives a developer concrete items to review before code is run or shared.

2. **Which finding mattered most?** The temporary-file race and predictable OTP were the clearest security risks because an attacker could exploit unsafe file creation or guess an authentication code. The embedded demo credentials also show why real secrets should be configured outside source.

3. **How did the tools complement one another?** Bandit focuses on risky APIs and security patterns, Pylint reviews broader code quality and likely defects, and Flake8 catches formatting and whitespace problems. Their overlap helps prioritize higher-impact problems before cosmetic ones.

4. **What limits did this analysis have?** Static checks cannot prove the wallet is secure or that every behavior is correct. Here, the Pylint, Bandit, and Flake8 packages were unavailable, so the issue list is a source review rather than captured tool output, and no numeric Pylint score is claimed. The handout did not include explicit reflection prompts, so these answers are organized around its stated learning outcomes.
