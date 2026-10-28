# Static analysis issue table

The original `digital_wallet.py` was reviewed from the repository's `main` branch. The analysis packages were not installed in the available runtime, so findings below are source-reviewed against common Pylint, Bandit, and Flake8 checks; line references refer to the original file and are approximate where reported tools could shift their own output.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| `tempfile.mktemp()` creates a race-prone temporary filename | Security (Bandit B306) | 58 | The name can be claimed by another process before the file is created. | Use `NamedTemporaryFile` to create the file atomically. |
| SHA-1 used for PIN comparison | Security (Bandit B324) | 14 | SHA-1 is not suitable for password/PIN storage. | Use salted PBKDF2-HMAC-SHA256 and constant-time digest comparison. |
| Non-cryptographic random OTP | Security (Bandit B311) | 62 | `random.randint` is predictable and inappropriate for authentication codes. | Generate the OTP with `secrets.randbelow`. |
| Embedded gateway credential and PIN | Security (Bandit B105) | 6-7 | Literal secret values can be recovered from source. | Read gateway secret from the environment and keep the demo PIN only as a salted PBKDF2 digest. |
| Mutable default `log=[]` | Correctness (Pylint W0102) | 17 | Calls without a log share one mutable list across invocations. | Default to `None`; append only when a caller supplies a list. |
| Unused cashback category | Maintainability (Pylint W0613) | 48 | `merchantType` is accepted but never affects the standard 2% calculation. | Mark the intentionally unused category with a leading underscore and document standard cashback behavior. |
| Naming, whitespace, and missing docstrings | Style (Pylint / Flake8) | throughout | CamelCase names, compressed statements, and absent documentation reduce readability and trigger style checks. | Use snake_case, consistent formatting, and concise docstrings. |

At least four concrete issues are fixed in the submitted version: the four security findings, the mutable default, and style issues. Exact tool counts and Pylint score are unavailable without the analysis packages.
