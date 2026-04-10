---
name: python-tdd-with-uv
description: Test-driven development in Python using uv as the package manager. Covers the red-green-refactor cycle, vertical slicing, and uv project setup.
user-invocable: true
---

# Python TDD with uv

Write Python code test-first using `uv` for fast dependency and environment management.

## Setting Up the Project

1. Check if `uv` is installed: `uv --version`
2. If the project doesn't have a `pyproject.toml`, initialize:
   ```bash
   uv init
   ```
3. Add pytest as a dev dependency:
   ```bash
   uv add --dev pytest pytest-cov
   ```
4. Confirm the test runner works:
   ```bash
   uv run pytest --co
   ```

## TDD Workflow — Vertical Slicing

Work in small cycles. Never write more than one failing test at a time.

### Planning Phase

Before writing code, answer:
1. What interface changes are needed? (functions, classes, APIs)
2. Which behaviors matter most? (prioritize critical paths)
3. Can we design for testability? (inject dependencies, avoid global state)

### The Cycle

```
RED   → Write ONE failing test for the next behavior
GREEN → Write the MINIMUM code to make it pass
REFACTOR → Clean up without changing behavior
REPEAT
```

**Rules:**
- Never write implementation before a failing test exists
- Never write more than one failing test at a time
- Run `uv run pytest` after every change
- Tests must assert observable behavior, not implementation details
- Mocks should only be used at system boundaries (I/O, network, clock)

### Test File Structure

```python
# tests/test_<module>.py

class TestFeatureName:
    """Group related behaviors."""

    def test_does_expected_thing_when_given_input(self):
        result = function_under_test(input_value)
        assert result == expected

    def test_raises_when_given_invalid_input(self):
        with pytest.raises(ValueError):
            function_under_test(bad_input)
```

### Running Tests

```bash
uv run pytest                      # all tests
uv run pytest tests/test_foo.py    # single file
uv run pytest -k "test_name"       # by name pattern
uv run pytest --cov=src            # with coverage
uv run pytest -x                   # stop on first failure
```

## uv Essentials

```bash
uv add <package>           # add dependency
uv add --dev <package>     # add dev dependency
uv remove <package>        # remove dependency
uv sync                    # sync environment from lockfile
uv run <command>           # run in managed environment
uv lock                    # regenerate lockfile
```

- Always use `uv run` to execute commands — never activate venvs manually
- Commit both `pyproject.toml` and `uv.lock`

## References

- [mattpocock/skills — TDD skill](https://github.com/mattpocock/skills) — vertical-slice TDD philosophy
- [nizos/tdd-guard](https://github.com/nizos/tdd-guard) — automated TDD enforcement via hooks
- [s2005/uv-skill](https://github.com/s2005/uv-skill) — uv workflow patterns
