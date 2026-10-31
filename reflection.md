# Reflection

The attached handout does not include a separate list of reflection questions. These responses address its four stated learning outcomes and the static-analysis work completed for the lab.

1. **How does static analysis contribute to code quality and maintainability?** It checks source without requiring a test case for each path. In this lab, it exposed security risks, a shared mutable default, maintainability concerns, and formatting violations early enough to address them before relying on the program.

2. **Which findings needed the most attention, and how were they fixed?** The weak PIN hash and unsafe temporary filename were the highest-severity findings. I replaced SHA-1 with PBKDF2-HMAC-SHA256 and constant-time comparison, generated a fresh random salt, and used `NamedTemporaryFile`. I also moved the gateway secret to an environment variable and generated OTPs with `secrets`.

3. **How did Pylint, Bandit, and Flake8 complement one another?** Bandit focused on risky security patterns, Pylint identified broader code quality issues such as the mutable default and global update, and Flake8 pointed out concrete spacing and line-layout problems. Using all three gave a more complete review than any single tool.

4. **What are the limits of static analysis, and what did the reports show?** Static analysis cannot prove that every behavior is correct or that the wallet is secure in deployment; the findings still need human review and runtime checks. The original program scored 5.52/10 in Pylint and had four Bandit issues and five Flake8 violations. After the fixes, Pylint scored 10.00/10, Bandit reported no issues, and Flake8 reported no violations. The demo retained its expected final balance of Rs. 1900.0 and total credited amount of Rs. 2500.
