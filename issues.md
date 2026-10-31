# Static analysis issue table

The table records findings from Pylint 4.1.3, Bandit 1.9.4, and Flake8 7.5.0 against the original `digital_wallet.py` from commit `0d188e2`. High and medium severity security findings appear first, followed by low severity and code quality findings.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| SHA-1 used to hash the wallet PIN | Security (Bandit B324, High) | 14 | SHA-1 is a weak general-purpose hash and should not protect PIN credentials. | Replace it with PBKDF2-HMAC-SHA256, a random salt, and constant-time digest comparison. |
| Race-prone temporary filename | Security (Bandit B306, Medium) | 60 | `tempfile.mktemp()` returns a name without creating the file, leaving a race for another process to claim it. | Create the receipt file atomically with `NamedTemporaryFile`. |
| Hard-coded gateway credential | Security (Bandit B105, Low) | 6 | The gateway key is embedded in source and would be exposed to anyone who can read it. | Read the gateway key from the `GATEWAY_SECRET` environment variable and compare it in constant time. |
| Predictable OTP generator | Security (Bandit B311, Low) | 64 | `random.randint()` is not intended for security-sensitive codes. | Generate the one-time code with `secrets.randbelow()`. |
| Mutable default argument | Correctness (Pylint W0102) | 17 | The default `log=[]` is shared across calls, so data can leak between invocations. | Use `None` as the default and append only when a list is supplied. |
| Global daily-limit update | Maintainability (Pylint W0603) | 28 | The setter changes module state through a `global` statement. | Store the setting in a configuration mapping and update that mapping. |
| Naming and missing documentation | Maintainability (Pylint C0103, C0114, C0116) | throughout | CamelCase names and missing module/function docstrings reduce consistency and clarity. | Use snake_case names and add concise docstrings. |
| Formatting violations | Style (Flake8 E261, E225, E231, E305, W292) | 76, 78-80 | The original file has inline-comment spacing, operator/comma spacing, missing blank lines, and no final newline. | Apply consistent spacing and blank lines, and end the file with one newline. |

The final program fixes every reported Bandit finding, the documented Pylint findings, and all Flake8 findings. The before/after tool outputs and final Pylint score are saved in the corresponding report files.
