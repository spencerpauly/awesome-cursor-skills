---
name: jumpcloud-qa-automation
description: Fully automates acceptance test implementation from feature files. Use when asked to automate acceptance tests, implement feature files, or act as a QE automation engineer. Takes JIRA ID and feature file path, creates branch, implements tests, runs in devspace, iterates on failures, and creates PR with labels. Self-contained with all necessary testing patterns embedded. Extensible with team-specific supplementary skills.
---

# JumpCloud QA Automation Agent

## Quick Start

Automate acceptance test implementation from a feature file:

```bash
# Via CLI wrapper
jc-automate-test AUTH-123 jumpcloud-acceptance/features/auth/example.feature

# With service context for better troubleshooting
jc-automate-test AUTH-123 features/auth/example.feature \
  --repos "https://github.com/TheJumpCloud/jumpcloud-auth" \
  --services "auth-api"

# Via Cursor chat
@automate-acceptance --jira AUTH-123 --feature jumpcloud-acceptance/features/auth/example.feature

# Cursor chat with service context
@automate-acceptance --jira AUTH-123 --feature features/auth/example.feature \
  --repos "https://github.com/TheJumpCloud/jumpcloud-auth" \
  --services "auth-api"
```

The agent will:
1. ✅ Create branch from JIRA ID
2. ✅ Read ALL convention guides (mandatory, no exceptions)
3. ✅ Analyze feature file and implement step definitions (following conventions strictly)
4. ✅ Run tests in devspace automatically
5. ✅ Iterate on failures (up to 3 attempts)

**🚨 CRITICAL: Agent MUST Run Tests – Never Defer to User**

- **NEVER** ask the user to run tests manually
- **NEVER** provide instructions for the user to run tests
- **ALWAYS** run tests yourself using the Shell tool (devspace_runner.py, kubectl exec, or bin/run_tests)
- Use `~/.jumpcloud-qa-automation/scripts/devspace_runner.py` or equivalent – execute it, don’t hand off to the user
6. ✅ Run `/PR-REVIEW` quality gate (fix all issues found)
7. ✅ Run pre-commit/lint checks (fix all issues found)
8. ✅ Re-run tests to confirm fixes didn't break anything
9. ✅ Commit, push, and create PR with `ai-full` and `patch` labels

---

## 🚨 START HERE: When You Receive a Command

**When the user invokes you with a command like:**

```bash
@automate-acceptance --jira NA-3215,NA-2997 --feature file1.feature,file2.feature --parallel 2 --fix-flaky
```

**YOU MUST DO THIS FIRST (before anything else):**

### 1. Parse ALL Flags

```python
# Extract flags from command
flags = {
    'jira_ids': ["NA-3215", "NA-2997"],  # Split by comma
    'features': ["file1.feature", "file2.feature"],  # Split by comma
    'parallel_count': 2,  # --parallel 2
    'fix_flaky': True,  # --fix-flaky present
    'extensions': ["auth", "login"],  # --extension auth,login
    'repos': ["https://github.com/..."],  # --repos "url1,url2"
    'services': ["auth-api", "login-api"],  # --services "auth-api,login-api"
}
```

### 2. Determine Execution Mode (Decision Tree)

```python
# DECISION TREE - FOLLOW THIS EXACTLY:

if flags['parallel_count'] > 1 and len(flags['features']) > 1:
    # ═══════════════════════════════════════════════════════════════
    # PARALLEL COORDINATOR MODE
    # ═══════════════════════════════════════════════════════════════
    
    print("═══════════════════════════════════════════════════════════")
    print("🎯 EXECUTION MODE: PARALLEL COORDINATOR")
    print("═══════════════════════════════════════════════════════════")
    print(f"Tests to coordinate: {len(flags['features'])}")
    print(f"Git worktrees: ✅ WILL CREATE")
    print(f"Testing: Sequential devspace (one at a time)")
    print(f"Max parallel: {flags['parallel_count']}")
    print()
    
    # Jump directly to "Parallel Execution" section
    # DO NOT continue to standard workflow!
    
else:
    # ═══════════════════════════════════════════════════════════════
    # STANDARD DEVSPACE MODE (DEFAULT)
    # ═══════════════════════════════════════════════════════════════
    
    print("═══════════════════════════════════════════════════════════")
    print("🎯 EXECUTION MODE: STANDARD DEVSPACE")
    print("═══════════════════════════════════════════════════════════")
    print(f"Test: {flags['jira_ids'][0]}")
    print(f"Devspace: ✅ LOCAL POD")
    print(f"Test runner: DevspaceRunner")
    print()
    
    # Continue to standard workflow below
    # Use DevspaceRunner for test execution
```

### 3. Import Correct Test Runner

Based on mode detected above:

```python
# Mode 1: Parallel Coordinator (worktrees + sequential devspace)
from parallel_coordinator import ParallelCoordinator

# Mode 2: Standard Devspace (single agent)
from devspace_runner import DevspaceRunner
```

---

## Adaptive Learning Philosophy

The agent follows KISS (Keep It Simple, Stupid) and YAGNI (You Aren't Gonna Need It) principles:

### KISS Principles
- ✅ Write straightforward, readable code
- ✅ Use clear, descriptive names
- ✅ Prefer simple solutions over clever ones
- ✅ Extract helpers only when pattern repeats 2-3 times
- ❌ Don't over-engineer solutions
- ❌ Don't add complexity for "future flexibility"

### YAGNI Principles
- ✅ Implement only what's needed NOW
- ✅ Add features when they're actually requested
- ✅ Wait for patterns to emerge before abstracting
- ❌ Don't add "might need later" functionality
- ❌ Don't create generic solutions for specific problems

### Pattern Discovery
1. Search for similar implementations (3+ files minimum)
2. Extract patterns only when repeated 2-3 times
3. Question rules if existing code consistently differs
4. Balance consistency with pragmatism

## Advanced Conventions

**🚨 MANDATORY: Before writing ANY code, the agent MUST read and internalize ALL 4 convention guides. Every line of code must comply. No exceptions.**

- **API Testing**: `qa-automation-conventions/api-test-conventions.md` - Import order, response validation, error handling, logging
- **BDD Patterns**: `qa-automation-conventions/bdd-step-patterns.md` - Given/When/Then decorators, target_fixture, parsers.parse patterns
- **Helper Functions**: `qa-automation-conventions/helper-function-patterns.md` - Single responsibility, DRY, type hints on ALL params/returns, action-oriented naming
- **Anti-Flakiness**: `qa-automation-conventions/anti-flakiness-guide.md` - Polling strategies, retry logic, timing patterns, service-specific delays

**Convention adherence is verified during the /PR-REVIEW quality gate step. Any violations will be caught and must be fixed before PR creation.**

### Key Convention Highlights

#### Session Creation Pattern
Always create helper functions for `requests.Session()`:

```python
# ✅ GOOD: Helper function
def create_api_session() -> requests.Session:
    """Create a requests session for API calls."""
    return requests.session()

# ❌ BAD: Direct creation
session = requests.session()  # Violates DRY
```

#### Context Validation Pattern
Use combined conditions (avoid nested ifs):

```python
# ✅ GOOD: Combined condition
def get_routing_policy_id_from_context(context: Any) -> str:
    if not hasattr(context, "routing_policy_id") or context.routing_policy_id is None:
        raise ValueError("Routing policy ID not found in context or is None")
    return str(context.routing_policy_id)

# ❌ BAD: Nested if statements
def get_routing_policy_id_from_context(context: Any) -> str:
    if not hasattr(context, "routing_policy_id"):
        raise ValueError("ID not found")
    routing_policy_id = context.routing_policy_id
    if routing_policy_id is None:
        raise ValueError("ID is None")
    return str(routing_policy_id)
```

#### Constants Extraction Pattern
Extract hard-coded values to module-level constants:

```python
# Constants at module level (after imports)
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
CONTENT_TYPE_JSON = "application/json"

# Use in code
validate_response_status_code(response, HTTP_NO_CONTENT)
```

#### Data Table Parsing Pattern
Always use `parsers.parse()` with `\n{table}` (NEVER `parsers.re()` for tables):

```python
# ✅ GOOD
@given(parsers.parse("an identity provider is created:\n{table}"))
def create_identity_provider_from_table(admin, context, table: str):
    rows = datatable_from(table)[1:]  # Skip header
    pass

# ❌ BAD
@given(parsers.re("an identity provider is created:(?s:(?P<table>.*))"))
```

## Prerequisites

### Required Tools & Versions

Before using this agent, ensure you have:

- **kubectl** v1.24+ - Kubernetes CLI
- **GitHub CLI (gh)** v2.0+ - GitHub operations
- **Python** 3.8+ - Automation scripts
- **devspace** v6.0+ - Local Kubernetes development
- **Git** 2.30+ - Version control

### Environment Setup

#### 1. Kubernetes/WoK Access

```bash
# Verify kubectl is configured
kubectl config current-context

# Set your namespace
devspace use namespace wok-{username}

# Test access
kubectl get pods -n wok-{username}
```

#### 2. GitHub Authentication

```bash
# Login to GitHub CLI
gh auth login

# Verify authentication
gh auth status
```

**Important**: GitHub CLI authentication enables:
- PR creation and label management
- **Reading private repository source code** (via `--repos` parameter)
- Accessing any GitHub repos you have permission to
- No additional setup needed for private repos

#### 3. Repository Access

```bash
# Clone if needed
git clone git@github.com:TheJumpCloud/jumpcloud-acceptance.git

# Verify write access
cd jumpcloud-acceptance
git remote -v
```

#### 4. WoK/Devspace Setup

```bash
# First time setup
cd jumpcloud-acceptance
devspace use namespace wok-{username}

# Test devspace (this may take 5-10 minutes first time)
devspace dev --skip-build

# Exit with Ctrl+C once pod is running
```

#### 5. Python Dependencies

```bash
# Install automation script dependencies
pip3 install -r ~/.jumpcloud-qa-automation/scripts/requirements.txt
```

### Verification Checklist

Before invoking the agent, verify:

- [ ] kubectl works: `kubectl version --client`
- [ ] GitHub CLI authenticated: `gh auth status`
- [ ] Python 3.9+: `python3 --version`
- [ ] devspace installed: `devspace version`
- [ ] Git configured: `git config user.name` and `git config user.email`
- [ ] WoK namespace accessible: `kubectl get pods -n wok-{username}`
- [ ] Repository cloned and accessible
- [ ] Devspace pod can run (test once)

If any checks fail, see the Troubleshooting section below.

## 🚨 CRITICAL: Initial Mode Detection (READ THIS FIRST!)

**BEFORE starting any work, the agent MUST detect execution mode based on flags:**

### Step 0: Parse Command Flags and Choose Execution Mode

```python
# Extract flags from user's command
parallel_count = extract_parallel_flag(user_command)  # e.g., "--parallel 2" → 2
fix_flaky = "--fix-flaky" in user_command
jira_ids = extract_jira_ids(user_command)  # e.g., "NA-3215,NA-2997" → ["NA-3215", "NA-2997"]
features = extract_features(user_command)  # e.g., "file1,file2" → ["file1", "file2"]

# Decision tree (FOLLOW THIS EXACTLY):
if parallel_count > 1 and len(features) > 1:
    # ═══════════════════════════════════════════════════════════════════════
    # PARALLEL COORDINATOR MODE (worktrees + sequential devspace)
    # ═══════════════════════════════════════════════════════════════════════
    
    print("🎯 MODE: Parallel Coordinator")
    print(f"   Tests: {len(features)}")
    print(f"   Parallel agents: {parallel_count}")
    print(f"   Worktrees: ✅ WILL CREATE")
    print(f"   Testing: Sequential devspace")
    print()
    
    # Import coordinator
    from parallel_coordinator import ParallelCoordinator
    
    # Create test specs
    test_specs = list(zip(jira_ids, features))
    
    # Create coordinator
    coordinator = ParallelCoordinator(
        acceptance_repo=Path("/path/to/jumpcloud-acceptance"),
        namespace="wok-username",
        max_parallel=parallel_count
    )
    
    # Run parallel implementation + sequential devspace testing
    results = coordinator.run_parallel_implementation(test_specs, service_names=[...])
    
    # Create PRs for each result
    for result in results:
        if result.success:
            create_pr(result.jira_id)
        else:
            create_draft_pr(result.jira_id, result.error)
    
    # Done! Exit here - don't continue to standard workflow
    exit(0)

else:
    # ═══════════════════════════════════════════════════════════════════════
    # STANDARD DEVSPACE MODE (DEFAULT)
    # ═══════════════════════════════════════════════════════════════════════
    
    print("🎯 MODE: Standard Devspace")
    print(f"   Test: {jira_ids[0]}")
    print(f"   Devspace: ✅ LOCAL POD")
    print()
    
    # Import devspace runner
    from devspace_runner import DevspaceRunner
    
    # Use devspace runner (standard mode)
    runner = DevspaceRunner(
        acceptance_repo=Path("/path/to/jumpcloud-acceptance"),
        namespace="wok-username"
    )
    
    # Continue to standard workflow below
```

### 🚨 Critical Rules for Mode Selection:

| Flags | Mode | Runner | Git Isolation |
|-------|------|--------|---------------|
| `--parallel N` + multiple features | Parallel Coordinator | `ParallelCoordinator` → sequential `DevspaceRunner` | ✅ Worktrees |
| No flags / single feature | Standard Devspace | `DevspaceRunner` | ❌ Main repo |

**IMPORTANT**: 
- ⚠️ If `--parallel N` but only ONE feature → ignore parallel, use standard mode
- ⚠️ Parallel coordinator handles EVERYTHING internally (don't continue to Phase 1!)

---

## Complete Automation Workflow

**NOTE**: This workflow applies to **Standard Devspace Mode**.
**For Parallel Coordinator Mode**, see "Parallel Execution" section instead.

### Phase 1: Setup (5 minutes)

**Automated by agent:**

1. **Validate prerequisites** - Check kubectl, gh, devspace, etc.
2. **Create branch** - From JIRA ID, updated from master
3. **Parse feature file** - Extract scenarios, steps, and complexity
4. **Generate implementation plan** - Identify required step definitions and helpers

**Manual prerequisite (user must ensure):**
- WoK devspace pod is running or can be started

### Phase 2: Implementation (15-30 minutes)

**🚨 MANDATORY FIRST STEP: Before writing ANY code, read ALL convention guides:**

```python
# The agent MUST read and internalize these BEFORE writing a single line of code:
# 1. qa-automation-conventions/api-test-conventions.md
#    → Import order, response validation, error handling, logging
# 2. qa-automation-conventions/bdd-step-patterns.md
#    → Given/When/Then decorators, target_fixture, parsers.parse
# 3. qa-automation-conventions/helper-function-patterns.md
#    → Single responsibility, DRY, type hints, naming conventions
# 4. qa-automation-conventions/anti-flakiness-guide.md
#    → Polling, retry logic, timing patterns, service delays
#
# NO EXCEPTIONS. Every line of code must comply with these guides.
# Convention adherence is verified during /PR-REVIEW quality gate.
```

**Automated by agent:**

1. **🚨 Read ALL 4 convention guides** - Load and internalize before writing code (NO EXCEPTIONS)
2. **Analyze existing step definitions** - Search for reusable steps
3. **Identify missing steps** - Compare feature file with existing implementations
4. **Implement step definitions** - Follow convention guides strictly (see Implementation Patterns section)
5. **Implement helper functions** - Create helpers in `tests/python/helpers/` following helper-function-patterns.md
6. **⚠️ CRITICAL: Remove `@not_yet_implemented` tag** - From feature file IMMEDIATELY after implementation

**Why removing `@not_yet_implemented` is critical:**
```python
# This tag causes pytest to SKIP the test
# If you don't remove it, Phase 3 tests will show "0 failures" but "0 tests ran"!

# Remove the tag:
feature_path = Path(feature_file)
content = feature_path.read_text()
content = content.replace('@not_yet_implemented', '')
feature_path.write_text(content)

print("✅ Removed @not_yet_implemented - tests will now run")
```

**Agent uses convention guides AND embedded patterns for:**
- BDD step definition structure (bdd-step-patterns.md)
- pytest-bdd decorators and fixtures (bdd-step-patterns.md)
- API test conventions - import order, helper patterns (api-test-conventions.md)
- Helper function design - type hints, naming, DRY (helper-function-patterns.md)
- Anti-flakiness patterns - polling, retries, timing (anti-flakiness-guide.md)
- Authentication flows (OAuth, TOTP, elevated users)
- gRPC service communication
- Error handling and validation

### Phase 3: Automated Testing Loop (20-60 minutes)

**You MUST run tests yourself using the Shell tool.** Invoke `python3 ~/.jumpcloud-qa-automation/scripts/devspace_runner.py <namespace> <jira_id> [acceptance_repo_path]` or use DevspaceRunner programmatically. Do NOT ask the user to run tests – execute them.

**Fully automated by agent using DevspaceRunner:**

```python
from devspace_runner import DevspaceRunner

runner = DevspaceRunner(
    acceptance_repo=acceptance_path,
    namespace=namespace
)

print("📦 Using WoK devspace pod for test execution")

# Standard devspace testing loop
for attempt in range(1, 4):  # Max 3 attempts
    # 1. Find or start devspace pod
    devspace_pod = find_devspace_pod(namespace)
    if not devspace_pod:
        start_devspace(namespace)
        wait_for_pod_ready(timeout=300)
    
    # 2. TEMPORARILY add JIRA tag to feature file for testing
    add_jira_tag_to_feature(feature_file, jira_id)  # e.g., @NA-3177
    wait_for_file_sync(30)  # Wait for devspace sync
    
    # 3. Run tests via kubectl exec
    test_result = run_tests_in_devspace(jira_id)
    
    # 4. IMMEDIATELY remove JIRA tag (don't commit it)
    remove_jira_tag_from_feature(feature_file, jira_id)
    
    # 5. Check if all tests passed
    if test_result.all_passed:
        break
    
    # 6. Analyze failures
    failures = analyze_test_failures(test_result.output)
    
    # 7. Apply fixes based on error patterns
    fixes_applied = apply_automated_fixes(failures)
    
    # 8. Wait for devspace file sync
    time.sleep(30)
else:
    # After 3 attempts, create draft PR with failures documented
    create_draft_pr_with_failures(jira_id, failures)
```

**JIRA Tag Workflow:**
```bash
# DURING TESTING: Temporarily add JIRA tag
echo "@auth @auth-api @mfa @webauthn @NA-3177" > feature_file
bin/run_tests api --tags @NA-3177

# AFTER TESTING: Remove JIRA tag immediately
echo "@auth @auth-api @mfa @webauthn" > feature_file

# NEVER commit the JIRA tag
```

**Testing commands used:**
```bash
# Inside devspace pod (via kubectl exec)
bin/run_tests api --tags @{jira_id}
```

**Failure analysis:**
- Parse pytest output for errors
- Categorize failures (imports, assertions, connectivity, etc.)
- Match against error patterns (see Error Patterns section)
- Generate fixes automatically
- Apply fixes and retry

### Phase 4: Quality Gate and Finalization (5-15 minutes)

**🚨 STRICT WORKFLOW SEQUENCE - NO SHORTCUTS, NO SKIPPING STEPS:**

The agent MUST follow this exact quality gate loop after all tests pass. This ensures clean PRs with minimal Bugbot review comments.

```
Tests Pass → /PR-REVIEW → Fix Issues → Lint/Pre-commit → Fix Issues → Re-test → Commit → PR
```

**Step-by-step quality gate:**

```python
# ═══════════════════════════════════════════════════════════════════════
# QUALITY GATE LOOP (MANDATORY - DO NOT SKIP ANY STEP)
# ═══════════════════════════════════════════════════════════════════════

quality_gate_passed = False

while not quality_gate_passed:
    
    # ─── GATE 1: All tests must pass ───────────────────────────────
    # (Already verified in Phase 3 testing loop above)
    
    # ─── GATE 2: Remove temporary tags ─────────────────────────────
    # Clean up ALL temporary tags before review:
    remove_focus_tags(feature_file)        # @focus
    remove_jira_tags(feature_file, jira_id) # @NA-3177, @AUTH-123
    # Keep only permanent tags: @smoke, @regression, @api, etc.
    
    # ─── GATE 3: Run /PR-REVIEW command ────────────────────────────
    # This is a Cursor command that self-reviews all code changes.
    # The agent MUST invoke /PR-REVIEW and analyze the output.
    #
    # /PR-REVIEW checks for:
    #   - Error handling issues
    #   - Security vulnerabilities (SQL injection, etc.)
    #   - Performance risks
    #   - Resource leaks
    #   - Architectural inconsistencies
    #   - Convention violations (from qa-automation-conventions/)
    #   - Code clarity, DRY, nesting depth
    #   - Type annotations, naming conventions
    #
    # Review output ends with one of:
    #   "Safe to commit."
    #   "Commit with caution: review recommended changes."
    #   "Not safe to commit until severe issues are fixed."
    
    pr_review_result = run_pr_review()  # Invoke /PR-REVIEW
    
    if pr_review_result == "Not safe to commit":
        # Fix ALL high-severity findings
        fix_pr_review_issues(pr_review_result.findings)
        # Must re-run tests after fixes
        rerun_tests()
        continue  # Loop back to Gate 1
    
    # If "Commit with caution" - fix recommended changes too
    if pr_review_result.has_recommendations:
        fix_pr_review_issues(pr_review_result.recommendations)
    
    # ─── GATE 4: Run pre-commit/lint checks ────────────────────────
    # Run against CHANGED FILES ONLY (not entire repo)
    
    changed_files = get_changed_files()  # git diff --name-only
    
    # Python linting (black, flake8, isort, pylint, mypy)
    lint_py = run_precommit(
        files=changed_files,
        config=".pre-commit-config-py.yaml"
    )
    
    # Feature file linting (reformat-gherkin, gherkin-lint, skip-tags, jira-tags)
    lint_feature = run_precommit(
        files=changed_files,
        config=".pre-commit-config-feature-files.yaml"
    )
    
    if lint_py.has_errors or lint_feature.has_errors:
        # Fix lint issues (black/isort auto-fix, manual for flake8/pylint)
        fix_lint_issues(lint_py.errors + lint_feature.errors)
        # Must re-run tests after fixes
        rerun_tests()
        continue  # Loop back to Gate 1
    
    # ─── GATE 5: Final test verification ───────────────────────────
    # Re-run tests one final time to confirm nothing broke
    final_result = run_tests_in_devspace(jira_id)
    
    if not final_result.all_passed:
        # Something broke during fixes - loop back
        continue
    
    # ─── ALL GATES PASSED ──────────────────────────────────────────
    quality_gate_passed = True

# ═══════════════════════════════════════════════════════════════════════
# COMMIT, PUSH, AND CREATE PR
# ═══════════════════════════════════════════════════════════════════════

git_add_and_commit(jira_id)
git_push(branch_name)
create_pr(
    jira_id=jira_id,
    labels=["ai-full", "patch"],
    title=f"[{jira_id}] Description",
    body=generate_pr_description()  # From implementation context
)
```

**Pre-commit commands used:**
```bash
# In jumpcloud-acceptance repo:
pre-commit run --files <changed_files> --config .pre-commit-config-py.yaml
pre-commit run --files <changed_files> --config .pre-commit-config-feature-files.yaml
```

**Why this quality gate matters:**
- `/PR-REVIEW` catches code quality issues BEFORE creating the PR
- Pre-commit/lint catches formatting and style issues
- Re-testing after fixes ensures nothing is broken
- Result: Bugbot has minimal review comments, saving time on back-and-forth

**PR details:**
- **Labels**: `["ai-full", "patch"]`
- **Title**: `[JIRA-ID] Description`
- **Description**: Generated from implementation context (NOT separate .md files)

### Phase 5: ROI Tracking (Continuous)

**⚠️ IMPORTANT: Track ROI metrics throughout the automation run**

The agent MUST track these metrics to demonstrate time savings and efficiency:

#### Token Usage Tracking

**At each major agent interaction, estimate and log token usage:**

```python
# Example: After reading feature file and planning implementation
logger.update_token_usage(
    input_tokens=8000,  # Estimate: SKILL.md (~6k) + feature file + context
    output_tokens=2000,  # Estimate: Implementation plan response
    agent_turn=True     # This is a new agent interaction
)
```

**Estimation guidelines:**
- SKILL.md: ~6,000 tokens (loaded at start)
- Feature file: ~100-500 tokens (depending on size)
- Generated code: Count characters and divide by 4
- Agent response: Estimate based on output length
- Extension files: ~1,000-2,000 tokens each

**Track agent turns:**
- Each back-and-forth with the user = 1 turn
- Planning phase = 1 turn
- Implementation = 1-2 turns
- Each test iteration = 1 turn
- Typical run: 3-5 turns

#### Productivity Metrics Tracking

**After implementation, count and log:**

```python
# Count what was created/modified
scenarios_count = count_scenarios_in_feature(feature_file)
step_defs_count = count_step_definitions_created(step_files)
loc_count = count_lines_of_code(all_modified_files)
helper_count = count_helper_functions_created(helper_files)
has_auth = check_if_uses_authentication(feature_file, step_files)
has_api = check_if_uses_api_calls(step_files)

# Update logger
logger.update_productivity_metrics(
    scenarios=scenarios_count,
    step_definitions=step_defs_count,
    lines_of_code=loc_count,
    helper_functions=helper_count,
    files_modified=len(all_modified_files),
    has_authentication=has_auth,
    has_api_calls=has_api
)
```

**Metrics to track:**
- Number of scenarios implemented (from feature file)
- Number of step definitions created (new @given/@when/@then)
- Lines of code generated (approximate, exclude imports/blank lines)
- Number of helper functions created
- Number of files modified
- Whether feature includes authentication (login, OAuth, TOTP)
- Whether feature includes API calls (REST, gRPC)

#### Logging ROI Data

**The automation_log.py module handles all ROI calculations:**

```python
from automation_log import AutomationLogger

# Initialize logger (done by automation script)
logger = AutomationLogger(log_dir=Path("automation_runs"))

# Start run (done automatically)
run = logger.start_run(
    jira_id="AUTH-123",
    feature_file_path="features/auth/example.feature",
    namespace="wok-username",
    repo_path="/path/to/jumpcloud-acceptance"
)

# During automation: Track tokens at each agent turn
logger.update_token_usage(
    input_tokens=estimated_input,
    output_tokens=estimated_output,
    agent_turn=True
)

# After implementation: Track what was created
logger.update_productivity_metrics(
    scenarios=3,
    step_definitions=8,
    lines_of_code=245,
    helper_functions=2,
    has_authentication=True,
    has_api_calls=True
)

# Complete run (done automatically)
# This automatically calculates:
# - Time saved based on manual baseline (2-4 hours per test)
# - Productivity metrics (tests created, LOC, scenarios)
# - Quality improvements (pass rates, flaky fixes)
logger.complete_run(status="success", pr_url="...")
```

**The agent does NOT need to:**
- Manually calculate time savings (AutomationLog handles it)
- Estimate manual baseline (automatically uses 2-4 hours per test)
- Write summary documents (embedded in PR description)

**Benefits of productivity tracking:**
- Teams see real time savings data
- Justifies agent adoption and expansion
- Identifies most valuable use cases
- Tracks efficiency improvements over time

## Org-Aware Log Collection

When tests fail, service logs can be **filtered by organization ID**, removing 90% of noise:

```python
from org_aware_logs import OrgAwareLogCollector

# Create collector with org ID (extracted from test output)
collector = OrgAwareLogCollector(
    namespace="wok-username",
    org_id="507f1f77bcf86cd799439011"
)

# Collect logs from multiple services
service_logs = collector.collect_logs_for_services(
    service_names=["auth-api", "login-api", "sso-api"],
    tail_lines=200,
    since="10m"
)

# Format for agent analysis (highlights errors/warnings)
formatted = collector.format_for_agent(service_logs)
```

**Example output:**
```
================================================================================
SERVICE LOGS FOR ORGANIZATION: 507f1f77bcf86cd799439011
================================================================================

Summary:
  - auth-api: 12/198 lines (94% noise removed) - 2 errors
  - login-api: 5/187 lines (97% noise removed) - 1 warnings
  - sso-api: 0/142 lines (100% noise removed)
```

---

## Flaky Test Fixing Mode (Automated De-flaking)

### Overview

The agent can automatically detect and fix flaky tests that are already implemented but exhibit instability. When a feature file contains `@flaky` tags, the agent enters a specialized fixing mode that:

1. **Detects** flaky scenarios automatically
2. **Analyzes** existing implementation for anti-patterns
3. **Applies** anti-flakiness patterns from the guide
4. **Validates** stability with 5 consecutive runs
5. **Learns** from successful fixes (updates skill)
6. **Removes** `@flaky` tag if stable
7. **Creates PR** with `flaky-fix` label

### When Flaky Mode is Triggered

**Auto-detection** (recommended):
```bash
# CLI detects @flaky tag in feature file
jc-automate-test NA-3124 features/auth/duo_mfa.feature

# Agent automatically enters flaky fixing mode if @flaky detected
```

**Explicit mode**:
```bash
# Force flaky fixing mode even without @flaky tag
jc-automate-test NA-3124 features/test.feature --fix-flaky
```

### Detection Logic

When invoked, the agent should:

1. **Check for `--fix-flaky` flag** in the command
2. **Or scan feature file** for `@flaky` tag:
   ```python
   from pathlib import Path
   
   feature_content = Path(feature_file).read_text()
   is_flaky = '@flaky' in feature_content.lower()
   
   if is_flaky or fix_flaky_flag:
       print("⚠️  Flaky test detected - entering fix mode")
       # Run flaky fixing workflow
   ```

### Flaky Fixing Workflow

**Phase 0: Remove Skip Tags (CRITICAL!)**

⚠️ **CRITICAL FIRST STEP**: Remove tags that cause tests to be skipped!

```python
# BEFORE doing anything else, remove skip tags from feature file
feature_path = Path(feature_file)
content = feature_path.read_text()

# Remove @flaky tag (causes test skip in some configurations)
content = content.replace('@flaky', '')

# Remove @not_yet_implemented tag (ALWAYS causes skip)
content = content.replace('@not_yet_implemented', '')

# Save cleaned feature file
feature_path.write_text(content)

print("✅ Removed @flaky and @not_yet_implemented tags")
print("   Tests will now run during validation")
```

**Why this is critical:**
- `@flaky` tag may cause pytest to skip the test
- `@not_yet_implemented` **ALWAYS** causes pytest to skip the test
- If tags are present, validation runs will skip tests → false positive (0 failures, but 0 tests run!)
- **Must remove BEFORE running any tests**

**Phase 1: Analysis (5-10 minutes)**

1. **Detect flaky scenarios**:
   ```python
   from flaky_test_detector import FlakyTestDetector
   
   detector = FlakyTestDetector(feature_path)
   
   if not detector.has_flaky_tag():
       print("No @flaky tags found")
       # Run normal automation
   
   flaky_scenarios = detector.get_flaky_scenarios()
   print(f"Found {len(flaky_scenarios)} flaky scenario(s)")
   
   for scenario in flaky_scenarios:
       print(f"  - {scenario.name} (line {scenario.line_number})")
       print(f"    Tags: {scenario.feature_tags}")
       
       # Get fix strategies
       strategies = detector.suggest_fix_strategies(scenario)
       print(f"    Strategies: {strategies[:3]}")  # Top 3
   ```

2. **Locate implementation**:
   - Read existing step definition file
   - Search for steps from flaky scenario
   - Identify which functions implement these steps

3. **Analyze code** for anti-patterns:
   ```python
   from flakiness_analyzer import FlakinessAnalyzer
   
   analyzer = FlakinessAnalyzer(step_def_path)
   
   issues = analyzer.analyze_implementation()
   print(f"Detected issues:")
   print(f"  Fixed sleeps: {len(issues['fixed_sleeps'])}")
   print(f"  Missing retries: {len(issues['missing_retries'])}")
   print(f"  TOTP reuse: {len(issues['totp_reuse'])}")
   print(f"  Short timeouts: {len(issues['short_timeouts'])}")
   
   # Get specific fixes
   fixes = analyzer.suggest_fixes()
   for fix in fixes:
       print(f"\n  Line {fix.line_number}: {fix.issue_type}")
       print(f"  Current: {fix.current_code}")
       print(f"  Fix: {fix.suggested_fix}")
   ```

4. **Check historical learnings**:
   ```python
   from skill_updater import SkillUpdater
   
   updater = SkillUpdater(skill_path)
   
   # Query similar past fixes
   similar = updater.get_similar_learnings(
       issue_type="missing_polling",
       tags=scenario.feature_tags
   )
   
   if similar:
       print(f"Found {len(similar)} similar historical fix(es):")
       for learning in similar:
           print(f"  - {learning['scenario_name']} ({learning['jira_id']})")
           # Agent can reference these successful patterns!
   ```

**Phase 2: Fix Application (10-20 minutes)**

1. **Apply fixes** based on detected anti-patterns:

   **Anti-Pattern: Fixed Sleep**
   ```python
   # ❌ BEFORE (flaky):
   time.sleep(2)
   assert user.mfa_enabled
   
   # ✅ AFTER (stable):
   from jumpcloud.tdk.helpers import poll_truthy
   
   poll_truthy(
       lambda: systemusers.get_systemuser(admin, user.id).mfa_enabled,
       timeout=60,
       interval=2
   )
   ```

   **Anti-Pattern: Missing Retry**
   ```python
   # ❌ BEFORE (flaky):
   response = SESSION.put(url, json=payload)
   # Fails on transient 503 errors
   
   # ✅ AFTER (stable):
   for attempt in range(3):
       response = SESSION.put(url, json=payload)
       if response.status_code == 200:
           break
       if response.status_code in [428, 503, 504] and attempt < 2:
           time.sleep(2 ** attempt)  # Exponential backoff
           continue
       break
   ```

   **Anti-Pattern: TOTP Reuse**
   ```python
   # ❌ BEFORE (flaky):
   code = totp_pin.now()
   # Might reuse same code from previous step
   
   # ✅ AFTER (stable):
   def get_fresh_totp_code(context, step_name):
       totp_pin = context.totp_pin
       last_code = getattr(context, 'last_totp_code', None)
       
       current_code = totp_pin.now()
       if current_code == last_code:
           wait_time = 30 - (time.time() % 30) + 1
           time.sleep(wait_time)
           current_code = totp_pin.now()
       
       context.last_totp_code = current_code
       return current_code
   
   code = get_fresh_totp_code(context, "mfa_verification")
   ```

   **Anti-Pattern: Missing Propagation Delay**
   ```python
   # ❌ BEFORE (flaky):
   create_conditional_policy(policy_data)
   assert user_login_denied()  # Policy not propagated!
   
   # ✅ AFTER (stable):
   create_conditional_policy(policy_data)
   time.sleep(5)  # Policy propagation delay
   poll_truthy(
       lambda: check_policy_active(policy_id),
       timeout=15,
       interval=2
   )
   assert user_login_denied()
   ```

2. **Service-specific fixes** based on tags:

   **Duo MFA** (`@duo` tag):
   - Add 2s delay after Duo account/app creation
   - Use `poll_truthy` for account availability
   - Increase timeout to 15s for Duo operations

   **Conditional Policies** (`@conditional-policies` tag):
   - Add 5-10s delay after policy creation
   - Use 2x timeout for location-based policies
   - Poll for policy activation before testing

   **Dynamic Groups** (`@dynamic-groups` tag):
   - Add 2s delay after user attribute changes
   - Use `poll_assertion` for group membership
   - Check both count AND member IDs

3. **Consult similar historical fixes** (if available):
   - Read similar learnings from skill
   - Apply proven patterns from past successes
   - Adapt to current scenario

**Phase 3: Stability Validation (15-30 minutes)**

1. **Run stability tests**:
   ```python
   from flaky_test_runner import FlakyTestRunner
   
   flaky_runner = FlakyTestRunner(
       devspace_runner=devspace_runner,
       jira_id=jira_id,
       namespace=namespace
   )
   
   stability = flaky_runner.run_stability_test(
       runs=5,
       cool_down=10,
       service_names=service_names
   )
   
   print(f"Pass rate: {stability.pass_rate}")
   print(f"Stable: {stability.stable}")
   ```

2. **Interpret results**:
   - **5/5 passes**: Test is stable ✅
   - **4/5 passes**: Might still be flaky, try different fix
   - **3/5 or less**: Not stable, need different approach

3. **On failure**, analyze patterns:
   ```python
   if not stability.stable:
       patterns = flaky_runner.get_failure_patterns()
       print(f"Failure patterns: {patterns}")
       # Example: {'timeout': 2, 'assertion_error': 1}
       
       # Try different fix based on patterns
       if 'timeout' in patterns:
           print("Increase timeouts and retry")
       elif 'assertion_error' in patterns:
           print("Add more polling/delays")
   ```

4. **Max 3 fix attempts**:
   - Try 3 different fix approaches
   - If still unstable after 3 attempts, create draft PR

**Phase 4: Finalization (2-5 minutes)**

1. **If stable (5/5 passes)**:
   
   a. **Verify `@flaky` and `@not_yet_implemented` tags removed**:
   ```bash
   # Tags should already be removed from Phase 0
   # But verify to be sure
   grep -n '@flaky\|@not_yet_implemented' features/auth/duo_mfa.feature
   # Should not find either tag
   
   # If somehow still present, remove:
   sed -i '' 's/@flaky //g' features/auth/duo_mfa.feature
   sed -i '' 's/@not_yet_implemented //g' features/auth/duo_mfa.feature
   ```
   
   **Note**: Tags should have been removed in Phase 0 (before running tests). This is just a verification step.
   
   b. **Record learning**:
   ```python
   from skill_updater import SkillUpdater
   
   updater = SkillUpdater(skill_path)
   updater.append_learning(
       scenario_name=scenario.name,
       issue_type="missing_polling",
       original_code=original_code,
       fixed_code=fixed_code,
       jira_id=jira_id,
       test_results="5/5 passed",
       tags=scenario.feature_tags
   )
   ```
   
   c. **Create PR** with special label:
   ```bash
   gh pr create \
       --title "[NA-3124] Fix flaky test: Duo accounts can be retrieved" \
       --body "$(cat <<'EOF'
   ## Summary
   Fixed flaky test by replacing fixed sleep with polling.
   
   **Issue**: Missing polling after Duo account creation
   **Fix**: Added poll_truthy with 15s timeout
   **Stability**: 5/5 consecutive runs passed ✅
   
   **Changes**:
   - Replaced time.sleep(2) with poll_truthy()
   - Increased timeout from 5s to 15s
   - Added Duo propagation delay
   
   **Test Results**:
   - Run 1: ✅ PASSED
   - Run 2: ✅ PASSED
   - Run 3: ✅ PASSED
   - Run 4: ✅ PASSED
   - Run 5: ✅ PASSED
   
   EOF
   )" \
       --label "ai-full" \
       --label "patch" \
       --label "flaky-fix"
   ```

2. **If still flaky (< 5/5 passes)**:
   
   a. **DO NOT add `@flaky` tag back**:
   ```python
   # Tags were removed in Phase 0
   # DO NOT add them back even if test still flaky!
   # 
   # Why: Tags cause tests to be skipped
   # Better: Create draft PR with "STILL FLAKY" warning
   # Team will review and decide next steps
   ```
   
   b. **Create draft PR** with analysis:
   ```bash
   gh pr create \
       --draft \
       --title "[NA-3124] Attempted flaky fix: Duo accounts (STILL FLAKY)" \
       --body "$(cat <<'EOF'
   ## Summary
   Attempted to fix flaky test but still unstable after fixes.
   
   **Pass Rate**: 3/5 (60%) - Still flaky ⚠️
   
   **Attempted Fixes**:
   1. Replaced fixed sleep with polling
   2. Added retry logic for 503 errors
   3. Increased timeout to 20s
   
   **Failures**:
   - Run 2: Timeout after 20s
   - Run 4: Duo account not available
   
   **Failure Patterns**:
   - timeout: 2 occurrences
   
   **Recommendations**:
   - May need longer propagation delay (try 5s+)
   - Consider Duo API external dependency issues
   - Manual investigation needed
   
   EOF
   )" \
       --label "ai-full" \
       --label "patch" \
       --label "needs-investigation"
   ```

### Critical: Apply Main Automation Skills

**IMPORTANT**: When fixing flaky tests, STILL apply ALL main automation skills!

The agent MUST:
- ✅ Use embedded testing patterns (OAuth, TOTP, gRPC, WebAuthn)
- ✅ Follow BDD conventions
- ✅ Create helper functions where appropriate
- ✅ Load service-specific extensions if applicable
- ✅ Use service context (repos, logs) for debugging
- ✅ Follow KISS and YAGNI principles
- 🆕 **ADDITIONALLY** apply anti-flakiness patterns
- 🆕 **ADDITIONALLY** run stability tests (5 runs)
- 🆕 **ADDITIONALLY** record learnings

**Think of it as:**
```
Normal Automation Skills + Anti-Flakiness Enhancements = Stable Tests
```

**Never**: Skip main skills in flaky mode! The test still needs proper implementation.

### Flaky Test Examples

#### Example 1: Duo MFA (Missing Polling)

**Feature file:**
```gherkin
@flaky @NA_3122 @duo
Scenario: User Portal Duo can be enabled and retrieved
  Given a registered administrator
  And a Duo account exists
  When the admin executes a PUT on v1: /userportal/mfa/duo
  Then the response has the status code "200"
  And the response has the field: enabled set to: true
  When the admin executes a GET on v1: /userportal/mfa/duo
  Then the response has the status code "200"
  And the response has the field: enabled set to: true
```

**Step definition (flaky):**
```python
@when(parsers.parse("the admin executes a PUT on {version}: /userportal/mfa/duo"))
def call_put_duo_mfa(context, admin, version):
    response = SESSION.put(url, json=payload)
    context.response = response

@when(parsers.parse("the admin executes a GET on {version}: /userportal/mfa/duo"))
def call_get_duo_mfa(context, admin, version):
    response = SESSION.get(url)  # Immediately - may not be propagated!
    context.response = response
```

**Issue detected**: Fixed immediate GET after PUT (no propagation delay)

**Fix applied:**
```python
@when(parsers.parse("the admin executes a PUT on {version}: /userportal/mfa/duo"))
def call_put_duo_mfa(context, admin, version):
    response = SESSION.put(url, json=payload)
    context.response = response
    
    # Add Duo propagation delay
    time.sleep(2)

@when(parsers.parse("the admin executes a GET on {version}: /userportal/mfa/duo"))
def call_get_duo_mfa(context, admin, version):
    # Poll for Duo config propagation
    poll_truthy(
        lambda: SESSION.get(url).json().get('enabled') is True,
        timeout=15,
        interval=2
    )
    response = SESSION.get(url)
    context.response = response
```

**Result**: 5/5 passes ✅, `@flaky` removed, learning recorded

#### Example 2: Conditional Policies (Policy Propagation)

**Feature file:**
```gherkin
@flaky @ZR_2101 @user-login-conditional-policies
Scenario: A user from location in Conditional Policy is denied login
  Given a registered administrator
  And an activated user with TOTP MFA required and enrolled
  And an user_portal authn policy with location condition which denies login with password
  And User's location which is 'present' in conditional List
  When User attempts to login to userportal from valid location
  Then the response has the status code "403"
```

**Issue**: Policy not propagated immediately after creation

**Fix strategy**:
- Add 5-10s delay after policy creation
- Use 2x timeout for location policies (geolocation data)
- Poll for policy activation

**Applied fix:**
```python
@given("an user_portal authn policy with location condition which denies login with password")
def create_location_policy(context, admin):
    policy = create_conditional_policy(admin, policy_data)
    context.policy = policy
    
    # Policy propagation delay (critical for conditional policies!)
    time.sleep(5)
    
    # Poll for policy activation
    poll_truthy(
        lambda: check_policy_active(policy.id, admin),
        timeout=20,  # 2x normal timeout for location policies
        interval=2
    )
```

**Result**: 5/5 passes ✅

#### Example 3: Dynamic Groups (Membership Update)

**Feature file:**
```gherkin
@flaky @HY_3974 @dynamic-groups
Scenario: Filter users with multiple conditions using AND logic
  Given the org has n number of users created with attributes
  When a dynamic group is created with AND filter
  Then the group should contain exactly the matching users
```

**Issue**: Group membership not updated immediately after user attribute changes

**Fix strategy**:
- Add 2s delay after user attribute changes
- Use `poll_assertion` for group membership
- Check both count AND member IDs

**Applied fix:**
```python
@when("a dynamic group is created with AND filter")
def create_dynamic_group(context, admin, users):
    group = create_group_with_filter(admin, filter_data)
    context.group = group
    
    # Small delay for backend indexing
    time.sleep(2)
    
    # Poll for group membership (eventual consistency)
    poll_assertion(
        lambda: check_group_members(group.id, expected_ids, admin),
        timeout=30,
        interval=2
    )
```

**Result**: 5/5 passes ✅

### Anti-Pattern Detection Reference

| Anti-Pattern | Detection | Suggested Fix | Pattern Name |
|--------------|-----------|---------------|--------------|
| `time.sleep(N)` without polling | Direct sleep, no `poll_truthy` after | Replace with `poll_truthy()` | polling_strategy |
| No retry for 428/503 | `SESSION.get/put/post` without retry check | Add retry loop with backoff | retry_with_backoff |
| TOTP code reuse | `totp_pin.now()` without fresh check | Use `get_fresh_totp_code()` | fresh_totp_token |
| Missing propagation delay | Policy/config creation → immediate test | Add 5s delay + polling | service_propagation |
| Short timeout (`< 10s`) | `timeout=5` for complex ops | Increase to operation-specific | operation_timeout |
| No delay between auth steps | Multi-step flow without pauses | Add 1-2s between steps | flow_timing |

### Learning System

After each successful fix (5/5 stability), record the learning:

```python
from skill_updater import SkillUpdater

updater = SkillUpdater(Path("skills/jumpcloud-qa-automation/SKILL.md"))

updater.append_learning(
    scenario_name="Duo accounts can be retrieved",
    issue_type="missing_polling",
    original_code="""time.sleep(2)
response = SESSION.get(url)
assert response.json()['enabled']""",
    fixed_code="""time.sleep(2)  # Duo propagation delay
poll_truthy(
    lambda: SESSION.get(url).json().get('enabled') is True,
    timeout=15,
    interval=2
)""",
    jira_id="NA-3122",
    test_results="5/5 passed",
    tags=["@duo", "@user-portal"]
)
```

**This learning will:**
- Be appended to SKILL.md in "Flakiness Patterns Learned" section
- Be available for future similar issues
- Help agent fix similar Duo tests faster
- Build institutional knowledge

### PR Labels for Flaky Fixes

**Stable (5/5 passes):**
- `ai-full` - Created by AI agent
- `patch` - Minor changes
- `flaky-fix` - Specifically fixes flakiness

**Still unstable (< 5/5 passes):**
- `ai-full`
- `patch`
- `needs-investigation` - Manual review needed
- Keep `@flaky` tag in feature file

### Integration with Other Features

**Flaky fixing (standard mode):**
```bash
jc-automate-test NA-3124 features/auth/duo_mfa.feature --fix-flaky
```
- ✅ Fixes flaky test
- ✅ Runs in devspace

**Flaky fixing + Parallel execution:**
```bash
# Fix 5 flaky tests in parallel!
jc-automate-test NA-3124,NA-3125,HY-3974,ZR-2101,AUTH-567 \
  features/duo.feature,features/policies.feature,features/groups.feature,features/location.feature,features/oauth.feature \
  --fix-flaky --parallel 5
```
- ✅ Each agent fixes its own flaky test
- ✅ Each in isolated worktree (no Git conflicts)
- ✅ Each in isolated org (no test conflicts)
- ✅ 5 PRs created with `flaky-fix` label

### Key Reminders

1. **⚠️ REMOVE SKIP TAGS FIRST** - Remove `@flaky` and `@not_yet_implemented` BEFORE running tests!
2. **Read existing implementation first** (test is already implemented!)
3. **Don't reimplement from scratch** (just fix the flakiness)
4. **Run 5 consecutive stability tests** (verify fix works)
5. **Only remove `@flaky` if 5/5 passes** (be conservative)
6. **Record learning if successful** (help future fixes)
7. **Use all main automation skills** (don't skip patterns!)

**Why removing skip tags is critical:**
- Tests tagged with `@not_yet_implemented` are **ALWAYS skipped** by pytest
- Tests tagged with `@flaky` may be skipped depending on configuration
- If tests are skipped, validation will show "0 failures" but **0 tests ran** → false positive!
- You must remove these tags BEFORE Phase 2 (Implementation) to ensure tests actually run during validation

---

### Git Workspace Isolation (Parallel Mode)

When `--parallel N` flag is used (N > 1), each agent runs in an **isolated Git worktree** to prevent Git conflicts during concurrent operations.

#### What are Git Worktrees?

Git worktrees allow multiple working directories from the same repository:

```
jumpcloud-acceptance/          (main repo)
├── .git/                      (shared Git metadata)
├── features/
├── tests/
└── worktrees/                 (isolated workspaces)
    ├── AUTH-123/              (Agent 1 workspace, branch: AUTH-123)
    │   ├── features/
    │   └── tests/
    ├── AUTH-124/              (Agent 2 workspace, branch: AUTH-124)
    │   ├── features/
    │   └── tests/
    └── AUTH-125/              (Agent 3 workspace, branch: AUTH-125)
        ├── features/
        └── tests/
```

Each worktree:
- Has its own working directory (files, index)
- Shares the `.git` directory (efficient, no re-cloning)
- Has its own branch checked out
- Can perform Git operations independently

#### When Worktrees Are Used

**Single agent mode** (default):
- Works in main repo: `jumpcloud-acceptance/`
- No worktrees created
- Branch operations in main repo

**Parallel mode** (`--parallel N` where N > 1):
- Worktrees created automatically by coordinator
- Each agent works in `jumpcloud-acceptance/worktrees/{JIRA-ID}/`
- Branch already created and checked out
- Complete Git isolation

#### Detection Logic

The agent can detect if running in worktree mode:

```bash
# Check if in worktree (worktree has .git file, main repo has .git directory)
if [ -f .git ]; then
    echo "Running in worktree (parallel mode)"
    MAIN_REPO=$(git rev-parse --git-common-dir | xargs dirname)
    WORKTREE_PATH=$(pwd)
else
    echo "Running in main repo (single agent mode)"
fi
```

Or in Python:
```python
from pathlib import Path

git_path = Path(".git")
is_worktree = git_path.is_file()  # Worktree has .git file
is_main_repo = git_path.is_dir()  # Main repo has .git directory
```

#### Agent Workflow in Worktree Mode

**Key difference**: Branch is already created by coordinator!

**Phase 1: Setup**
```bash
# ✅ Branch already exists (created by coordinator)
git branch --show-current  # Shows: AUTH-123

# ❌ Don't create branch again!
# git checkout -b AUTH-123  # Will fail - branch exists
```

**Phase 2: Implementation**
```bash
# Work normally - all operations are isolated!
vim tests/python/step_definitions/auth/login_steps.py
vim tests/python/conftest.py

# Add files
git add tests/python/step_definitions/auth/login_steps.py

# Check status (only shows this agent's changes)
git status
```

**Phase 3: Commit**
```bash
# Commit in worktree (no conflicts with other agents!)
git commit -m "[AUTH-123] Implement login tests"

# Push branch
git push -u origin AUTH-123
```

**Phase 4: PR Creation**
```bash
# Create PR (same as single agent mode)
gh pr create \
  --title "[AUTH-123] Implement login acceptance tests" \
  --body "$(cat pr_body.txt)" \
  --label "ai-full" \
  --label "patch"
```

#### Important Notes

1. **Branch Pre-Creation**: Coordinator creates branch + worktree before agent starts
2. **Isolation**: Each agent's Git operations are completely isolated
3. **Cleanup**: Worktrees are automatically cleaned up after PR creation
4. **Backward Compat**: Single agent mode works exactly as before (no worktrees)

#### Troubleshooting

**Issue**: "Branch AUTH-123 already exists"

**Solution**: Coordinator handles this by creating unique branch name: `AUTH-123-retry-{timestamp}`

**Issue**: "Worktree already exists"

**Solution**: Coordinator detects and cleans up stale worktrees automatically

**Issue**: Agent can't push to remote

**Solution**: Same as single agent mode - ensure GitHub CLI is authenticated

### Parallel Execution

**Run 2-5 tests in parallel with `--parallel` flag!**

#### When to Use Parallel

**Use `--parallel N` when:**
- ✅ User explicitly requests it with `--parallel N` flag
- ✅ Have multiple independent tests to automate
- ✅ Want 2-5x speedup for batch implementation
- ✅ Tests are NOT already automated (manual implementation needed)

**Requirements:**
- ⚠️  Max 5 parallel agents (resource conservative)
- ⚠️  Git worktrees created for each agent (zero Git conflicts)
- ⚠️  Tests run sequentially in devspace (reliable, no org conflicts)

#### Parallel Execution Flow

**🚨 CRITICAL REQUIREMENTS:**

1. **Multiple features REQUIRED**: `--parallel N` is ignored if only one feature provided
2. **Coordinator handles EVERYTHING**: Don't continue to standard workflow after this!
3. **Same quality gate applies**: Each test goes through /PR-REVIEW + lint before PR

```python
# ═══════════════════════════════════════════════════════════════════════
# PARALLEL COORDINATOR WORKFLOW (Worktrees + Sequential Devspace)
# ═══════════════════════════════════════════════════════════════════════

from pathlib import Path
from parallel_coordinator import ParallelCoordinator

# STEP 1: Validate
if len(test_specs) < 2:
    print("⚠️  Only 1 test provided, using standard mode")
    # Fall back to standard workflow

# STEP 2: Create coordinator
coordinator = ParallelCoordinator(
    acceptance_repo=Path("/path/to/jumpcloud-acceptance"),
    namespace="wok-username",
    max_parallel=parallel_count  # max 5
)

# STEP 3: Define test specs
test_specs = [
    ("AUTH-123", "features/auth/login.feature"),
    ("AUTH-124", "features/auth/mfa.feature"),
    ("SSO-201", "features/sso/saml.feature")
]

print("═══════════════════════════════════════════════════════════")
print("🚀 STARTING PARALLEL COORDINATOR")
print("═══════════════════════════════════════════════════════════")
print(f"Tests: {len(test_specs)}")
print(f"Worktrees: ✅ WILL CREATE")
print(f"Implementation: Parallel (simultaneous)")
print(f"Testing: Sequential devspace (one at a time)")
print()

# STEP 4: Run parallel implementation + sequential testing
# Coordinator handles:
# - Creating Git worktrees for each test
# - Each agent implements in its own worktree (parallel)
# - Tests run sequentially in devspace (reliable)
# - Quality gate (test -> /PR-REVIEW -> lint -> retest)
# - Commits and pushes from each worktree
results = coordinator.run_parallel_implementation(
    test_specs=test_specs,
    service_names=["auth-api", "login-api"],
    fix_flaky=flags.get('fix_flaky', False)
)

# STEP 5: Create PRs for each result
for result in results:
    if result.success:
        print(f"✅ {result.jira_id} passed")
        create_pr(jira_id=result.jira_id, labels=["ai-full", "patch"])
    else:
        print(f"❌ {result.jira_id} failed")
        create_draft_pr(jira_id=result.jira_id, error=result.error)

# STEP 6: Summary
print(f"Total: {len(results)}, Passed: {sum(1 for r in results if r.success)}")

exit(0)  # Workflow complete!
```

**🚨 CRITICAL NOTES:**

1. **Coordinator handles ENTIRE workflow** - don't implement standard phases manually
2. **Exit after coordinator completes** - don't continue to Phase 1 below!
3. **Same quality gate** - each test goes through /PR-REVIEW + lint + retest

#### Key Parallel Benefits

**Performance:**
- 2-3x speedup vs serial execution (implementation is parallel)
- Tests run sequentially in devspace (reliable, proven)

**Safety:**
- Zero Git conflicts (each agent in its own worktree)
- Zero test data conflicts (sequential devspace execution)

#### Parallel Best Practices

**DO:**
- ✅ Use for multiple independent features
- ✅ Let coordinator handle worktree management
- ✅ Create separate PRs for each test
- ✅ Report combined summary to user

**DON'T:**
- ❌ Try to parallelize single feature (no benefit)
- ❌ Exceed max_parallel=5
- ❌ Run tests in parallel (devspace is sequential)

## Critical Testing Rules

### Rule 0: NEVER Skip Tests

**⚠️ This is MANDATORY and NON-NEGOTIABLE**

Skipping tests is invalid practice. When encountering complex scenarios:

**❌ NEVER DO:**
```gherkin
@skip
Scenario: User authenticates with WebAuthn
  # Skipped because it requires cryptographic signing
```

**✅ ALWAYS DO:**
1. **Research service's own tests** - How does the service test this scenario?
2. **Find existing patterns** - Check for similar implementations in the codebase
3. **Implement proper solution** - Use appropriate libraries (cryptography, cbor2, etc.)
4. **Ask for help if stuck** - But never skip tests

**Why this matters:**
- Skipped tests don't provide value
- They give false confidence
- They hide implementation gaps
- User feedback: "we should never skip test it's invalid practice"

**When tests seem too complex:**
- ✅ Research how the service itself tests this (check functional tests)
- ✅ Look for helper libraries or utilities
- ✅ Implement simplified but valid approach (e.g., 'none' attestation)
- ✅ Use real APIs with generated test data
- ❌ Don't skip and move on

**Example: WebAuthn seemed complex but was solved by:**
1. Reading auth-api's functional tests
2. Generating real ECDSA keys with cryptography library
3. Creating 'none' attestation format
4. Making real gRPC calls
Result: All 4 tests passing with proper signatures

### Rule 1: NEVER Commit Without Testing in Devspace

**⚠️ This is MANDATORY and NON-NEGOTIABLE**

Tests MUST pass in devspace before committing. The agent will:
- Start devspace automatically if not running
- Run all scenarios in the feature file
- Iterate on failures up to 3 times
- Only proceed to commit after all tests pass

**The agent MUST run the tests – use the Shell tool to execute devspace_runner.py or kubectl exec. NEVER ask the user to run tests manually.**

**Why devspace is mandatory:**
- Local environment lacks system dependencies
- Python version mismatches
- No access to WoK services (auth-api, kafka, etc.)
- Missing grpcio compilation
- Devspace provides realistic test environment matching CI/CD

### Rule 2: Pre-commit Checks are Mandatory

**⚠️ CRITICAL: Pre-commit checks MUST be run BEFORE committing**

**Before committing, the agent MUST run BOTH pre-commit configs:**

```bash
cd jumpcloud-acceptance

# 1. Run Python pre-commit checks on modified Python files
pre-commit run --all-files --config .pre-commit-config-py.yaml

# 2. Run feature file pre-commit checks on modified feature files
pre-commit run --all-files --config .pre-commit-config-feature-files.yaml
```

**Common linter fixes:**
- `flake8 F401`: Remove unused imports
- `flake8 F841`: Remove unused variables
- `mypy attr-defined`: Add `# type: ignore` for dynamic Context attributes
- `mypy assignment`: Use `str | None` instead of `str = None` for optional parameters
- `mypy union-attr`: Add explicit type checks for union types (see cryptography pattern)
- `pylint W9008`: Remove "Returns:" sections from void functions
- `flake8 E501`: Refactor lines to ≤88 characters
- `isort`: Auto-fix import order
- `black`: Auto-fix formatting

**Cryptography-specific mypy fixes:**
```python
# ❌ Causes mypy union type errors
loaded_key = serialization.load_pem_private_key(...)
signature = loaded_key.sign(...)  # Error: union type has no sign()

# ✅ Add type check to narrow union
if not isinstance(loaded_key, ec.EllipticCurvePrivateKey):
    raise ValueError("Expected EC key")
signature = loaded_key.sign(...)  # OK: mypy knows exact type
```

### Rule 3: Clean Up Temporary Tags Before Committing

**⚠️ MANDATORY: Remove all temporary tags from feature files before committing**

Feature files should only contain permanent, functional tags. Remove ALL temporary tags used during development.

**Temporary Tag Workflow:**

```bash
# ✅ GOOD: Add JIRA tag temporarily for testing
sed -i '' '1s/@auth/@auth @NA-3177/' features/auth/webauthn.feature
bin/run_tests api --tags @NA-3177

# ✅ GOOD: Remove JIRA tag immediately after testing
sed -i '' 's/@NA-3177 //g' features/auth/webauthn.feature

# ❌ BAD: Commit feature file with JIRA tag
git add features/auth/webauthn.feature  # With @NA-3177 still in file
git commit -m "Add tests"  # DON'T DO THIS!
```

**Temporary tags to ADD for testing (then REMOVE):**
```gherkin
✅ @NA-3177                  # Add temporarily to run: bin/run_tests api --tags @NA-3177
✅ @focus                    # Add temporarily to run specific scenarios
↓ (Run tests)
❌ Remove before commit!     # ALWAYS remove these before git commit
```

**Temporary tags to REMOVE before committing:**
```gherkin
❌ @focus                    # Used for running specific scenarios during dev
❌ @NA-3177                  # JIRA ID tags (only for test execution)
❌ @AUTH-123                 # Any ticket-specific tags
❌ @wip                      # Work-in-progress markers
❌ @debug                    # Debugging tags
```

**Permanent tags to KEEP:**
```gherkin
✅ @smoke                    # Smoke test indicators
✅ @regression               # Regression suite markers
✅ @api                      # Test type tags
✅ @slow                     # Performance indicators
✅ @critical                 # Priority markers
✅ @auth @mfa @webauthn      # Feature area tags
```

**Why this matters:**
- JIRA tags like `@NA-3177` are ONLY for running tests during development: `bin/run_tests api --tags @NA-3177`
- They help target specific scenarios while iterating on failures
- These are implementation artifacts, not test metadata
- Clean feature files improve maintainability
- Avoid clutter and confusion for other developers
- Only functional/permanent tags should be in version control

**The agent's workflow:**
1. **During testing**: Temporarily add `@{jira_id}` to feature file
2. **Run tests**: Use tag to target specific scenarios
3. **After testing**: Immediately remove `@{jira_id}` tag
4. **Before committing**: Verify no temporary tags remain
5. **Commit**: Only permanent tags in feature file

**Cleanup checklist before commit:**
```bash
# 1. Remove JIRA tag from feature file
sed -i '' '/@NA-3177/d' features/auth/webauthn_challenge_assert_authentication.feature

# 2. Remove @focus tags
sed -i '' '/@focus/d' features/**/*.feature

# 3. Remove @not_yet_implemented (critical for new implementations!)
sed -i '' 's/@not_yet_implemented //g' features/**/*.feature

# 4. Remove @flaky (if fixing flaky tests and validation passed)
sed -i '' 's/@flaky //g' features/**/*.feature

# 5. Verify no temporary or skip tags remain
grep -r "@NA-\|@AUTH-\|@focus\|@wip\|@debug\|@not_yet_implemented\|@flaky" features/
# Should return nothing
```

### Rule 4: Never Create Summary .md Files

**❌ DO NOT commit files like:**
- `IMPLEMENTATION_SUMMARY_*.md`
- `IMPLEMENTATION_STATUS_*.md`
- `NA_3129_FINAL_STATUS.md`
- `*_IMPLEMENTATION_*.md`

**✅ INSTEAD:**
- Use implementation context for PR descriptions directly
- Include details in PR body
- Delete any summary files before committing

### Rule 5: Source Code is Source of Truth

When tests fail, the agent will:
1. Read the actual service implementation from provided GitHub repos
2. Understand expected behavior from code
3. Not assume or guess behavior
4. Verify patterns in existing helpers
5. Check service logs for runtime behavior

**Providing Service Context:**

Via command-line:
```bash
jc-automate-test AUTH-123 features/test.feature \
  --repos "https://github.com/TheJumpCloud/jumpcloud-auth" \
  --services "auth-api"
```

Via environment variables:
```bash
export JUMPCLOUD_SERVICE_REPOS="https://github.com/org/jumpcloud-auth,https://github.com/org/login"
export JUMPCLOUD_SERVICE_NAMES="auth-api,login-api"
```

Via extension (see Extensibility section).

**Example:** Reading `jumpcloud-auth/services/oauth.go` from provided repo to understand:
- USER_PORTAL vs ADMIN_PORTAL behavior
- Policy evaluation order
- MFA enrollment indications
- Token response structures

**Service Log Inspection:**

When tests fail, the agent automatically:
1. Collects logs from specified services using `kubectl logs -l app={service}`
2. Extracts error lines (containing "error", "exception", "failed", "panic")
3. Includes logs in failure analysis
4. Correlates service errors with test failures

Example collected logs:
```
=== SERVICE LOGS ===
--- Logs for auth-api ---
2026-02-06T10:15:23Z ERROR: Invalid totp code: token already used
2026-02-06T10:15:24Z ERROR: Authentication failed: grpc code 16

--- Errors in auth-api ---
2026-02-06T10:15:23Z ERROR: Invalid totp code: token already used
```

## BDD & Step Definition Patterns

### pytest-bdd Step Structure

**Step decorators:**
```python
from pytest_bdd import given, when, then, parsers

@given('the authentication service is running')
def auth_service_running(context):
    """Verify auth service is accessible."""
    response = requests.get(f"{context.base_url}/health")
    assert response.status_code == 200

@given(parsers.parse('a user exists with email "{email}"'))
def create_user(context, admin, email):
    """Create test user with email."""
    context.user = factories.rest.systemusers.SystemuserFactory(
        admin=admin,
        email=email
    )

@when('the user authenticates with valid credentials')
def authenticate(context):
    """Authenticate user."""
    # Implementation

@then('the authentication should succeed')
def verify_success(context):
    """Verify authentication succeeded."""
    assert context.response.status_code == 200
```

### Fixtures and Context

**Context management:**
```python
from tests.python.helpers.context import Context

@given("a service account")
def create_service_account(context: Context, admin: models.rest.User):
    """Create service account and store in context."""
    service_account = create_service_account_api(admin)
    context.service_account = service_account
    context.service_account_id = service_account["id"]
    return service_account
```

**Common context attributes:**
- `context.user` - Current test user
- `context.rest_admin` - REST API admin
- `context.response` - Last API response
- `context.totp_pin` - TOTP generator
- `context.last_totp_code` - Last used TOTP code

### Parameter Parsing

```python
# Simple parameters
@given(parsers.parse('a user with email "{email}"'))
def user_with_email(context, email: str):
    pass

# Type conversion
@given(parsers.parse("{count:d} users exist"))
def users_exist(count: int):
    pass

# Data tables (ALWAYS use parsers.parse with \n{table})
@given(parsers.parse("an identity provider is created:\n{table}"))
def create_idp_from_table(admin, context, table: str):
    from tests.python.helpers.datatable import datatable_from
    rows = datatable_from(table)[1:]  # Skip header
    for row in rows:
        key = row[0].strip()
        value = row[1].strip()
        # Process
```

### Target Fixtures

**⚠️ CRITICAL: Always specify `target_fixture` when steps create reusable objects**

```python
@given("a registered administrator", target_fixture="admin")
def admin(context: Context) -> models.rest.User:
    """Create admin and return as fixture."""
    admin, orm_admin = make_registered_admin()
    context.orm_admin = orm_admin
    context.rest_admin = admin
    return admin

@given("a user exists with a password", target_fixture="user")
def user_with_password(admin: models.rest.User, context: Context) -> models.rest.User:
    """Create a user with a password and return as fixture."""
    context.user_password = fake.password()
    kwargs = {"password": context.user_password}
    user = factories.rest.systemusers.SystemuserFactory(admin=admin, **kwargs)
    context.user = user
    context.user_email = user.email  # type: ignore[attr-defined]
    return user  # CRITICAL: Must return the fixture object
```

**Why this matters:**
- Other steps expecting `user` fixture will get `FixtureLookupError` if this is missing
- Missing `target_fixture` can cause cascading failures across dozens of unrelated tests
- BOTH `target_fixture="user"` AND `return user` are required

**Common mistake pattern:**
```python
# ❌ WRONG: Missing target_fixture and return statement
@given("a user exists with a password")
def user_with_password(admin: models.rest.User, context: Context):
    user = factories.rest.systemusers.SystemuserFactory(admin=admin)
    context.user = user
    # Missing: target_fixture parameter and return statement

# ✅ CORRECT: With target_fixture and return
@given("a user exists with a password", target_fixture="user")
def user_with_password(admin: models.rest.User, context: Context) -> models.rest.User:
    user = factories.rest.systemusers.SystemuserFactory(admin=admin)
    context.user = user
    return user  # CRITICAL
```

## Authentication Flow Patterns

### OAuth/OIDC Flows

**Two distinct authentication paths - DO NOT confuse them:**

#### Flow 1A: Standalone Admin Authentication (SI REST)

**User Type:** Admin (User collection only)  
**Service:** SI (REST API)  
**Endpoints:** `POST /auth`, `POST /auth/mfa`  
**NOT via:** auth-api gRPC

```python
# Step 1: Password Authentication
def authenticate_admin_with_password_si_rest(context, admin_email, password):
    """Authenticate admin with password via SI REST."""
    session = requests.Session()
    
    # Get XSRF token
    xsrf_response = session.get(f"{SI_ROOT_URL}/xsrf", verify=False)
    xsrf_token = xsrf_response.json().get("xsrf")
    
    # Authenticate
    auth_response = session.post(
        f"{SI_ROOT_URL}/auth",
        headers={"Content-Type": "application/json", "X-Xsrftoken": xsrf_token},
        json={"email": admin_email, "password": password},
        verify=False,
    )
    
    context.si_session = session
    context.si_headers = {"Content-Type": "application/json", "X-Xsrftoken": xsrf_token}
    context.auth_response = auth_response

# Step 2: TOTP/MFA Authentication
def authenticate_admin_with_totp_si_rest(context, admin_email):
    """Authenticate admin with TOTP via SI REST."""
    totp_code = get_fresh_totp_code(context, "Admin TOTP Auth")
    
    response = context.si_session.post(
        f"{SI_ROOT_URL}/auth/mfa",
        headers=context.si_headers,
        json={"otp": totp_code},
        verify=False,
    )
    
    context.auth_response = response
```

#### Flow 1B: Elevated User Authentication (auth-api gRPC)

**User Type:** SystemUser (with or without linked admin)  
**Service:** jumpcloud-auth (gRPC)  
**Endpoints:** `UserCredentials.Assert`, `Totp.Assert`, `OAuth.UserAssertionsToken`

```python
# Step 1: Get password assertion token
def assert_user_credentials(context, email, password):
    """Get password assertion token."""
    from jumpcloud.auth import UserCredentials_pb2
    
    request = UserCredentials_pb2.UserCredentialsAssertRequest(
        user_identifier={"email": email},
        user_password_credential={"password": password}
    )
    response = user_credentials_stub.Assert(request)
    return response.assertion.token

# Step 2: Initial authentication (triggers MFA if required)
def call_user_assertions_token(context, email, assertion_token, resource_type="USER_PORTAL"):
    """Authenticate with assertion token."""
    from jumpcloud.auth import OAuth_pb2
    
    request = OAuth_pb2.UserAssertionsTokenRequest(
        context={
            "resource": {"type": resource_type},  # USER_PORTAL or ADMIN_PORTAL
            "user_identifier": {"email": email}
        },
        assertion={"token": assertion_token}
    )
    
    try:
        response = oauth_stub.UserAssertionsToken(request)
        return response
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.UNAUTHENTICATED:
            # MFA required - extract state_token
            context.state_token = extract_state_token(e)
            context.mfa_required = True
            raise
        raise

# Step 3: Get TOTP assertion token (if MFA required)
def assert_totp(context, email, totp_code):
    """Get TOTP assertion token."""
    from jumpcloud.auth import Totp_pb2
    
    request = Totp_pb2.TotpAssertRequest(
        userIdentifier={"email": email},
        otp=totp_code
    )
    response = totp_stub.Assert(request)
    return response.assertion.token

# Step 4: Complete authentication with TOTP
def complete_authentication_with_totp(context, email, totp_token, resource_type="USER_PORTAL"):
    """Complete authentication after MFA."""
    request = OAuth_pb2.UserAssertionsTokenRequest(
        context={
            "resource": {"type": resource_type},
            "state_token": context.state_token
        },
        assertion={"token": totp_token}
    )
    response = oauth_stub.UserAssertionsToken(request)
    return response
```

### Resource Types

**CRITICAL: Resource type determines authentication policies**

**ADMIN_PORTAL:**
- Used by admin console
- ALWAYS requires MFA (system-wide policy)
- MFA grace period applies
- Returns both id_token and access_token

**USER_PORTAL:**
- Used by user portal
- MFA enforcement can be configured
- Returns id_token only (in some configs)

## TOTP/MFA Testing Patterns

### Critical Pattern: Database-Only TOTP Configuration

**❌ WRONG: API-Based TOTP Enrollment**
```python
# DON'T DO THIS - authenticates user before test!
def enroll_user_totp(context, email, password):
    session = requests.Session()
    auth_response = session.post("/userconsole/auth", json={"email": email, "password": password})
    # This creates authenticated session with USER_PORTAL context
    # Uses a TOTP token during setup
    # Interferes with OAuth flow
```

**✅ CORRECT: Database-Only Configuration**
```python
def configure_totp_in_database(admin, system_user, totp_key):
    """Configure TOTP directly in database without API authentication."""
    # Update database directly
    models.orm.Systemuser.objects.get(id=system_user.id).update(
        totp_enabled=True,
        totp_key=totp_key,
        enable_user_portal_multifactor=True,
    )
    
    # Trigger MFA sync to auth-api
    sdk.call(SystemusersApi(), "systemusers_mfasync", system_user.id)
    
    # Store for test
    context.totp_key = totp_key
    context.totp_pin = pyotp.TOTP(totp_key)
    
    # CRITICAL: Mark current token as "used"
    context.last_totp_code = pyotp.TOTP(totp_key).now()
    
    # CRITICAL: Wait for NEXT token window (30s + 3s buffer)
    wait_time = (30 - (time.time() % 30)) + 3
    log.info(f"Waiting {wait_time:.1f}s for fresh TOTP token and MFA sync")
    time.sleep(wait_time)
```

### Fresh TOTP Token Helper

**Always use this helper for getting TOTP codes:**

```python
def get_fresh_totp_code(context: Context, step_name: str) -> str:
    """Get a fresh TOTP code that hasn't been used yet."""
    totp_pin = context.totp_pin
    last_code = getattr(context, "last_totp_code", None)
    
    current_code = totp_pin.now()
    
    # If same as last used code, wait for next window
    if current_code == last_code:
        wait_time = 30 - (time.time() % 30) + 1
        log.info(f"{step_name}: Waiting {wait_time:.1f}s for fresh TOTP code")
        time.sleep(wait_time)
        current_code = totp_pin.now()
    
    # Mark as used
    context.last_totp_code = current_code
    log.info(f"{step_name}: Using fresh TOTP code: {current_code}")
    
    return current_code
```

### MFA Policy Enforcement

```python
def ensure_mfa_required(admin, system_user):
    """Ensure MFA is required by removing exclusions."""
    # Enable MFA at user level
    models.orm.Systemuser.objects.get(id=system_user.id).update(
        enable_user_portal_multifactor=True,
    )
    
    # Remove MFA exclusion flag
    systemuser_api = jcapiv1.SystemusersApi(sdk.get_jcapiv1_client(admin))
    user = sdk.call(systemuser_api, "systemusers_get", system_user.id)
    
    if hasattr(user, 'mfa') and user.mfa and user.mfa.exclusion:
        user.mfa.exclusion = False
        sdk.call(systemuser_api, "systemusers_put", system_user.id, body=user)
    
    # Sync changes
    sdk.call(systemuser_api, "systemusers_mfasync", system_user.id)
```

## gRPC & API Testing Patterns

### Real API Testing Philosophy

**⚠️ CRITICAL: Always Prefer Real APIs Over Mocking**

When implementing acceptance tests, follow this preference hierarchy:

**Preference Hierarchy:**
1. ✅ **Real gRPC/API calls with real data** → BEST (validates actual service behavior)
2. ✅ **Real gRPC/API calls with simplified data** → GOOD (e.g., 'none' attestation for WebAuthn)
3. ⚠️ **Database seeding + real API calls** → ACCEPTABLE (when full flow is impractical)
4. ❌ **HTTP/gRPC mocking** → AVOID (unless absolutely necessary for CI/CD constraints)

**Why Real APIs?**
- Users explicitly prefer real API testing for acceptance tests
- Validates actual service behavior, not assumptions
- Catches integration issues and edge cases
- Tests API contracts and error handling
- Provides confidence in production behavior

**When to Use Simplified Data:**
- Full real-world simulation requires browser/hardware (e.g., WebAuthn with actual authenticators)
- Complex cryptographic operations can use simplified formats (e.g., 'none' attestation)
- Focus on testing API behavior, not recreating entire environments
- Balance: Real API behavior + Practical CI/CD constraints

### Learning from Service Tests

**Before implementing complex scenarios, research the service's own tests:**

**Step 1: Clone Service Repository**
```bash
# Clone to /tmp for reference (agent can do this automatically)
cd /tmp
gh repo clone TheJumpCloud/jumpcloud-auth
cd jumpcloud-auth
```

**Step 2: Find Functional Tests**
```bash
# Look for test directories
find . -type d -name "test" -o -name "tests"

# Common patterns:
# - test/functional/
# - test/integration/
# - internal/*/test/
```

**Step 3: Search for Similar Test Patterns**
```bash
# Example: Finding WebAuthn test patterns
grep -r "WebAuthn" test/functional/
grep -r "attestation" test/functional/
grep -r "mock" test/functional/conftest.py
```

**Step 4: Adapt Patterns to Acceptance Tests**
```python
# Example: auth-api uses 'none' attestation for WebAuthn tests
# Found in: test/functional/conftest.py and grpcutils/webauthn_registration.py

# Service pattern (Go with mock service):
# - Uses webauthnmock service for credential generation
# - Generates real signatures with mock authenticator
# - Validates 'none' attestation format

# Acceptance test adaptation:
# - Generate real ECDSA keys in Python
# - Create 'none' attestation format directly
# - Make real gRPC calls to auth-api
# - Validate signature verification works end-to-end
```

**Benefits:**
- ✅ Discover service-specific test utilities
- ✅ Understand expected data formats
- ✅ Learn about test-friendly configuration options
- ✅ Find mock services or test fixtures
- ✅ Avoid reinventing patterns

### gRPC Service Communication

**Status code extraction:**
```python
import grpc

try:
    response = stub.SomeMethod(request)
except grpc.RpcError as e:
    # ✅ CORRECT: Use .code() method
    if hasattr(e, "code") and callable(e.code):
        grpc_code = e.code()
        
    # Map to HTTP status codes
    if grpc_code == grpc.StatusCode.UNAUTHENTICATED:
        http_status = 401
    elif grpc_code == grpc.StatusCode.PERMISSION_DENIED:
        http_status = 403
    elif grpc_code == grpc.StatusCode.NOT_FOUND:
        http_status = 404
    else:
        http_status = 500
    
    # ❌ WRONG: Don't use .status_code attribute
    # grpc_code = e.status_code  # This doesn't exist!
```

### MockResponse Pattern

For gRPC calls that need to work with generic step definitions expecting `requests.Response`:

```python
class MockResponse:
    """Mock HTTP response object for gRPC calls."""
    def __init__(self, status_code: int, content: str = ""):
        self.status_code = status_code
        self.content = content
        self.text = content
        self.body = content
        self.data = content

# Usage
try:
    grpc_response = stub.SomeMethod(request)
    context.response = MockResponse(200)
except grpc.RpcError as e:
    http_status = map_grpc_to_http_status(e.code())
    context.response = MockResponse(http_status)
```

### Service Discovery

**Find service addresses and ports:**
```bash
# Check available services
kubectl get svc -n wok-{username}

# Common ports:
# - auth-api gRPC: 6060 (NOT 9080)
# - auth-api HTTP: 9080
# - login gRPC: 6060
```

## Real Cryptographic Operations

### When Cryptography is Required

**Scenarios requiring real cryptographic operations:**
- WebAuthn credential enrollment and assertion
- Digital signature verification (JWT, SAML, etc.)
- Encryption/decryption testing
- Certificate-based authentication
- Public/private key management

**❌ DON'T: Skip tests requiring cryptography**

**✅ DO: Implement proper cryptographic operations**

### WebAuthn/ECDSA Pattern

**Complete WebAuthn flow with real cryptography:**

**Step 1: Generate Real ECDSA P-256 Key Pair**
```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import cbor2
import base64

def create_webauthn_credential(user_id: str) -> dict:
    """Generate real ECDSA P-256 key pair for WebAuthn.
    
    Returns credential_id, public_key (COSE format), and private_key_pem.
    """
    # Generate real ECDSA P-256 key pair (WebAuthn standard: ES256)
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    
    # Get public key in uncompressed point format (0x04 || X || Y)
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    
    # Extract x and y coordinates (skip the 0x04 prefix)
    x_coord = public_key_bytes[1:33]   # 32 bytes
    y_coord = public_key_bytes[33:65]  # 32 bytes
    
    # Convert to COSE format (CBOR Object Signing and Encryption)
    # This is the format auth-api expects
    cose_key = {
        1: 2,        # kty: EC2 (Elliptic Curve key type)
        3: -7,       # alg: ES256 (ECDSA with SHA-256)
        -1: 1,       # crv: P-256 (curve identifier)
        -2: x_coord, # x coordinate (32 bytes)
        -3: y_coord  # y coordinate (32 bytes)
    }
    
    # Encode COSE key to CBOR
    public_key_cose = cbor2.dumps(cose_key)
    public_key_b64 = base64.urlsafe_b64encode(public_key_cose).decode().rstrip("=")
    
    # Create credential ID
    credential_id = f"test_webauthn_cred_{user_id}"
    credential_id_b64 = base64.urlsafe_b64encode(credential_id.encode()).decode().rstrip("=")
    
    # Export private key in PEM format for later signing
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()
    
    return {
        "credential_id": credential_id_b64,
        "public_key": public_key_b64,      # COSE format, base64url encoded
        "private_key_pem": private_key_pem  # For signing assertions
    }
```

**Step 2: Enroll with Real gRPC API (Hybrid Approach)**
```python
def enroll_webauthn_credential(user_id: str, credential: dict):
    """Enroll credential using real gRPC with 'none' attestation."""
    from grpc_requests import Client
    
    # Call real BeginRegistration gRPC
    client = Client("auth-api:6060", ssl=False)
    begin_response = client.request(
        "jumpcloud.auth.WebAuthnCredentials",
        "BeginRegistration",
        {
            "organization_object_id": org_id_b64,
            "user_object_id": user_id_b64,
            "self_register": False,
            "attachment": 2  # CROSS_PLATFORM
        }
    )
    
    # Create 'none' attestation with REAL public key
    # Note: The public_key from credential is already COSE-encoded
    attestation_object = create_none_attestation(
        credential["credential_id"],
        credential["public_key"],  # Already COSE format
        begin_response["creation_options"]["challenge"]
    )
    
    # Call real FinishRegistration gRPC
    finish_response = client.request(
        "jumpcloud.auth.WebAuthnCredentials",
        "FinishRegistration",
        {
            "organization_object_id": org_id_b64,
            "user_object_id": user_id_b64,
            "token": begin_response["token"],
            "name": f"Test Key {user_id[:8]}",
            "public_key_credential": attestation_object
        }
    )
    # Now credential is enrolled with the real public key
```

**Step 3: Sign Assertions with Private Key**
```python
def create_webauthn_assertion(
    credential_id: str,
    challenge: str,
    private_key_pem: str
) -> dict:
    """Create cryptographically valid assertion."""
    import hashlib
    import json
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    
    # Create authenticator data
    webui_host = os.environ.get("WEBUI_HOST")
    rp_id_hash = hashlib.sha256(webui_host.encode()).digest()
    flags = bytes([0x01])  # User Present
    sign_count = (0).to_bytes(4, 'big')
    authenticator_data_bytes = rp_id_hash + flags + sign_count
    
    # Create client data JSON
    client_data_dict = {
        "type": "webauthn.get",
        "challenge": challenge,
        "origin": f"https://{webui_host}",
        "crossOrigin": False
    }
    client_data_json_str = json.dumps(client_data_dict)
    
    # Load private key
    loaded_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )
    
    # Type check for mypy
    if not isinstance(loaded_key, ec.EllipticCurvePrivateKey):
        raise ValueError("Expected EC private key")
    
    # Sign: authenticator_data || SHA256(client_data_json)
    client_data_hash = hashlib.sha256(client_data_json_str.encode()).digest()
    signed_data = authenticator_data_bytes + client_data_hash
    
    # Create ECDSA signature (ASN.1 DER encoded)
    signature_bytes = loaded_key.sign(
        signed_data,
        ec.ECDSA(hashes.SHA256())
    )
    
    # Return base64url encoded components
    return {
        "credential_id": credential_id,
        "authenticator_data": base64.urlsafe_b64encode(authenticator_data_bytes).decode().rstrip("="),
        "client_data_json": base64.urlsafe_b64encode(client_data_json_str.encode()).decode().rstrip("="),
        "signature": base64.urlsafe_b64encode(signature_bytes).decode().rstrip("=")
    }
```

**Step 4: Verify with Real gRPC API**
```python
def verify_webauthn_assertion(user_email: str, token: str, assertion: dict):
    """Verify assertion using real gRPC - signature validated by auth-api."""
    client = Client("auth-api:6060", ssl=False)
    
    response = client.request(
        "jumpcloud.auth.WebAuthn",
        "Assert",
        {
            "user_identifier": {"email": user_email},
            "webauthn_response": {
                "token": token,
                "public_key_credential": {
                    "id": assertion["credential_id"],
                    "raw_id": assertion["credential_id"],
                    "type": "public-key",
                    "assertion_response": {
                        "client_data_json": assertion["client_data_json"],
                        "authenticator_data": assertion["authenticator_data"],
                        "signature": assertion["signature"]
                    }
                }
            }
        }
    )
    # auth-api validates signature against enrolled public key
    return response
```

### COSE Format Critical Rules

**⚠️ CRITICAL: Common COSE Mistakes**

**❌ WRONG: Re-encoding already-encoded COSE keys**
```python
# public_key is already COSE-encoded and base64url
cose_key = {
    1: 2,
    3: -7,
    -1: 1,
    -2: base64.urlsafe_b64decode(public_key)[:32],  # ❌ This is wrong!
    -3: base64.urlsafe_b64decode(public_key)[:32]   # ❌ Already encoded!
}
```

**✅ CORRECT: Use COSE bytes directly**
```python
# If public_key is already COSE-encoded, just decode it
cose_key_bytes = base64.urlsafe_b64decode(public_key + "==")
# Use directly in attestation object
```

**COSE Key Structure:**
```
COSE Key (CBOR encoded):
{
  1: 2,        // kty: EC2 (Elliptic Curve)
  3: -7,       // alg: ES256 (ECDSA + SHA-256)
  -1: 1,       // crv: P-256 (NIST curve)
  -2: <bytes>, // x coordinate (32 bytes for P-256)
  -3: <bytes>  // y coordinate (32 bytes for P-256)
}

Total size: ~77 bytes when CBOR-encoded
```

### Type Hints for Cryptography

**mypy pattern for union type handling:**
```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def sign_data(private_key_pem: str, data: bytes) -> bytes:
    """Sign data with EC private key."""
    # Load key - returns union of all key types
    loaded_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )
    
    # Type check for mypy - narrows union type
    if not isinstance(loaded_key, ec.EllipticCurvePrivateKey):
        raise ValueError("Expected EC private key")
    
    # Now mypy knows loaded_key is EllipticCurvePrivateKey
    # No union type errors!
    signature = loaded_key.sign(data, ec.ECDSA(hashes.SHA256()))
    return signature
```

**Without type check, mypy errors:**
```
error: Item "DHPrivateKey" has no attribute "sign"
error: Item "X25519PrivateKey" has no attribute "sign"
error: Too many arguments for "sign" of "Ed25519PrivateKey"
```

### Required Libraries

**⚠️ CRITICAL: Always Update pyproject.toml AND poetry.lock**

When adding new dependencies for tests, you MUST update both `pyproject.toml` and `poetry.lock` to ensure they're available in CI:

**Step 1: Install in devspace (for immediate testing):**
```bash
# Inside devspace pod
pip install cryptography  # For ECDSA, RSA, key generation
pip install cbor2         # For CBOR encoding (WebAuthn, COSE)
pip install grpc_requests # For gRPC client calls
```

**Step 2: Add to pyproject.toml (for CI/CD):**
```toml
[tool.poetry.group.dev.dependencies]
cryptography = "^41.0.0"
cbor2 = "^5.6.5"
grpc_requests = "^1.0.0"
```

**Step 3: Update poetry.lock (CRITICAL for CI):**
```bash
# IMPORTANT: Use the project's Poetry version (check pyproject.toml)
grep 'poetry-version' pyproject.toml  # Or check CI config for POETRY_VERSION

# Match your local Poetry version to the project's version
pip install --upgrade poetry==2.1.3

# Verify version
poetry --version  # Should show: Poetry (version 2.1.3)

# Update lock file (Poetry 2.x automatically doesn't update existing packages)
poetry lock

# Verify the change
git diff poetry.lock | head -20
# Should show: @generated by Poetry 2.1.3
```

**Why this matters:**
- ✅ Tests pass in devspace (has pip install)
- ❌ Tests fail in CI (only installs from pyproject.toml + poetry.lock)
- 🐛 CI errors like: `ModuleNotFoundError: No module named 'cbor2'`

**Common mistake pattern:**
1. Install library in devspace with pip → Tests pass locally
2. Commit and push → CI fails with ModuleNotFoundError
3. **FIX:** Add library to `pyproject.toml` AND run `poetry lock` → CI passes

**Poetry Version Consistency:**
- ⚠️ Always match your local Poetry version to the project's version
- Check `pyproject.toml` or CI config for `POETRY_VERSION`
- Mismatched versions can cause lock file format issues
- Poetry 2.x: Use `poetry lock` (no `--no-update` flag)
- Poetry 1.x: Use `poetry lock --no-update`

**Import pattern:**
```python
# Third Party
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
import cbor2
from grpc_requests import Client
```

## Common Test Patterns

### TDK Factories

```python
from jumpcloud.si.tdk import factories, models

# REST factory (creates via API)
user = factories.rest.systemusers.SystemuserFactory(admin=admin)

# ORM factory (creates directly in DB)
orm_user = factories.orm.users.UserFactory(organization=org)
```

### API Request Pattern

```python
from jumpcloud.si.tdk.constants import WEBUI_URL
from tests.python.helpers.requests import headers_apiKey

# Create session
def create_api_session() -> requests.Session:
    """Create requests session for API calls."""
    return requests.session()

session = create_api_session()

# Build URL
endpoint = f"{WEBUI_URL}/api/service_accounts"

# Make request
response = session.get(
    endpoint,
    headers=headers_apiKey(admin),
    verify=False
)

# Validate
from jumpcloud.tdk.helpers import validate_response_status_code
validate_response_status_code(response, 200)
```

### Polling for Async Operations

```python
from jumpcloud.tdk.helpers import poll_truthy, poll_assertion

# Poll until condition is true
poll_truthy(
    lambda: check_user_exists(user_id),
    timeout=60,
    interval=2,
    error_message="User did not appear within timeout"
)

# Poll until assertion passes
poll_assertion(
    lambda: assert response.status_code == 200,
    timeout=30,
    interval=1
)
```

## Devspace Testing Loop

### Finding Devspace Pod

```python
def find_devspace_pod(namespace: str) -> str:
    """Find devspace pod in namespace."""
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace, "-l", "app=devspace", "-o", "name"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0 and result.stdout:
        return result.stdout.strip().split("/")[-1]
    return None
```

### Starting Devspace

```python
def start_devspace_if_needed(namespace: str) -> bool:
    """Start devspace if not running."""
    pod = find_devspace_pod(namespace)
    if pod:
        return True
    
    # Start devspace
    subprocess.Popen(
        ["devspace", "dev", "--skip-build"],
        cwd=ACCEPTANCE_REPO,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for pod to be ready
    return wait_for_pod_ready(namespace, timeout=300)
```

### Running Tests

```python
def run_tests_in_devspace(pod_name: str, namespace: str, jira_id: str) -> TestResult:
    """Run tests in devspace pod via kubectl exec."""
    result = subprocess.run(
        [
            "kubectl", "exec", "-n", namespace, pod_name, "--",
            "bin/run_tests", "api", "--tags", f"@{jira_id}"
        ],
        capture_output=True,
        text=True,
        timeout=600
    )
    
    return parse_pytest_output(result.stdout)
```

### Parsing Test Results

```python
def parse_pytest_output(output: str) -> TestResult:
    """Parse pytest output to extract pass/fail status."""
    # Look for final line: "===== X passed, Y failed in Z.ZZs ====="
    match = re.search(r"=+ (\d+) passed(?:, (\d+) failed)? in [\d.]+s =+", output)
    
    if match:
        passed = int(match.group(1))
        failed = int(match.group(2)) if match.group(2) else 0
        
        return TestResult(
            all_passed=(failed == 0),
            passed_count=passed,
            failed_count=failed,
            output=output
        )
    
    # No tests run or error
    return TestResult(all_passed=False, passed_count=0, failed_count=1, output=output)
```

## Error Patterns & Automated Fixes

### Common Error Patterns

| Error Pattern | Cause | Automated Fix |
|---------------|-------|---------------|
| `ModuleNotFoundError: No module named 'X'` (in devspace) | Missing import | Add import statement |
| `ModuleNotFoundError: No module named 'X'` (in CI) | Dependency not in pyproject.toml | Add library to `[tool.poetry.group.dev.dependencies]` and run `poetry lock` |
| `FixtureLookupError: pytest-bdd could not find fixture 'user'` | Step definition missing `target_fixture="user"` | Add `target_fixture="user"` parameter and `return user` statement to the step definition |
| `grpc._channel._InactiveRpcError: UNAVAILABLE` | Service not reachable | Verify service address and port (use kubectl get svc) |
| `AssertionError: assert 500 == 200` | gRPC error not mapped correctly | Fix status code extraction (use `.code()` method) |
| `ERROR: TOTP code already used` | Token reuse in same window | Use `get_fresh_totp_code()` helper |
| `AttributeError: 'Context' object has no attribute 'X'` | Context attribute not set | Ensure fixture sets attribute or add `# type: ignore` |
| `flake8 F401: imported but unused` | Unused import | Remove import |
| `flake8 E501: line too long` | Line >88 chars | Refactor line |
| `mypy attr-defined` | Dynamic Context attribute | Add `# type: ignore` comment |

### Failure Analysis

```python
def analyze_test_failures(test_output: str) -> List[Failure]:
    """Analyze test output and categorize failures."""
    failures = []
    
    # Extract tracebacks
    traceback_pattern = r"_{10,}\n(.*?)\n(?:_{10,}|={10,})"
    tracebacks = re.findall(traceback_pattern, test_output, re.DOTALL)
    
    for tb in tracebacks:
        if "ModuleNotFoundError" in tb:
            module = extract_module_name(tb)
            failures.append(Failure(
                type="import_error",
                message=f"Missing module: {module}",
                fix=f"Add import: import {module}"
            ))
        elif "AssertionError" in tb and "status_code" in tb:
            failures.append(Failure(
                type="assertion_error",
                message="Status code mismatch",
                fix="Check gRPC error handling - use .code() not .status_code"
            ))
        elif "TOTP code already used" in tb:
            failures.append(Failure(
                type="totp_reuse",
                message="TOTP token reused",
                fix="Use get_fresh_totp_code() helper"
            ))
        # More patterns...
    
    return failures
```

### Applying Automated Fixes

```python
def apply_automated_fixes(failures: List[Failure]) -> bool:
    """Apply automated fixes for known failure patterns."""
    fixes_applied = False
    
    for failure in failures:
        if failure.type == "import_error":
            # Add missing import
            add_import_to_file(failure.file_path, failure.module)
            fixes_applied = True
        
        elif failure.type == "totp_reuse":
            # Replace direct TOTP call with helper
            replace_totp_calls_with_helper(failure.file_path)
            fixes_applied = True
        
        elif failure.type == "grpc_status_code":
            # Fix gRPC status code extraction
            fix_grpc_status_extraction(failure.file_path)
            fixes_applied = True
    
    return fixes_applied
```

## Code Conventions

### Import Order

**Strict order with blank lines between sections:**

```python
# Standard Library
import json
import logging
import time
from typing import Any, Dict, List

# Third Party
import grpc
import pyotp
import requests
from pytest_bdd import given, parsers, then, when

# JumpCloud
from jumpcloud.si.tdk import factories, models
from jumpcloud.si.tdk.constants import WEBUI_URL
from jumpcloud.tdk.helpers import validate_response_status_code

# First Party
from tests.python.constants import DEFAULT_SERVICE_ACCOUNT_NAME
from tests.python.helpers.context import Context
from tests.python.helpers.datatable import datatable_from
```

### Helper Function Patterns

**Session creation:**
```python
# ✅ Good: Create helper function
def create_api_session() -> requests.Session:
    """Create requests session for API calls."""
    return requests.session()

# Use it
session = create_api_session()

# ❌ Bad: Direct creation multiple times
session = requests.session()  # Violates DRY
```

**Common validation:**
```python
# ✅ Good: Common validation function
def validate_routing_policy_in_list(
    routing_policy_id: str,
    routing_policies: Any,
    should_be_present: bool = True,
) -> None:
    """Validate policy presence in list."""
    policy_ids = [p.get("id") for p in extract_policies(routing_policies)]
    
    if should_be_present:
        assert routing_policy_id in policy_ids
    else:
        assert routing_policy_id not in policy_ids
```

**Extract constants:**
```python
# ✅ Good: Module-level constants
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_FORBIDDEN = 403
CONTENT_TYPE_JSON = "application/json"

# Use in code
validate_response_status_code(response, HTTP_NO_CONTENT)
```

## Pre-commit & Linting

### Running Pre-commit

```bash
cd jumpcloud-acceptance
pre-commit run --files <modified-files> --config .pre-commit-config-py.yaml
```

### Common Fixes

**flake8 F401 (unused imports):**
```python
# Remove unused imports
# import json  # ❌ Remove if not used
```

**flake8 E501 (line too long):**
```python
# ❌ Bad: Line too long
some_very_long_function_call(param1, param2, param3, param4, param5, param6)

# ✅ Good: Break into multiple lines
some_very_long_function_call(
    param1, param2, param3,
    param4, param5, param6
)
```

**mypy attr-defined:**
```python
# Add type ignore for dynamic Context attributes
context.some_dynamic_attr = value  # type: ignore[attr-defined]
```

## PR Creation

### PR Labels

**Always add these labels:**
- `ai-full` - Full AI review requested
- `patch` - Patch/minor change

**Command:**
```bash
gh pr create \
  --title "[JIRA-ID] Description" \
  --body "$(cat pr_body.txt)" \
  --label "ai-full" \
  --label "patch"
```

### PR Title Format

```
[JIRA-ID] Description

Examples:
[AUTH-123] Acceptance test automation for OAuth flows
[NA-3129] Add elevated user admin login tests
```

### PR Description Template

```markdown
## Summary
- **JIRA**: [JIRA-ID](https://jumpcloud.atlassian.net/browse/JIRA-ID)
- Implement acceptance tests for [feature_name]
- {scenario_count} scenarios automated

## Implementation Details
- Implemented step definitions for:
  - Scenario 1: Description
  - Scenario 2: Description
- Created helpers in `tests/python/helpers/`
- Followed API test conventions

## Changes
- Created/updated step definitions in `tests/python/step_definitions/`
- Added/updated helpers in `tests/python/helpers/`
- Updated feature file: {feature_file_path}

## Testing
- [x] All scenarios pass in devspace (WoK)
- [x] Pre-commit checks passed
- [x] No linter errors introduced

## AI Generation Notes
This PR was automatically generated by the JumpCloud QA Automation Agent.
- Implementation patterns follow existing conventions
- Tests validated in live devspace environment
- {retry_count} iteration(s) to resolve test failures
```

## Extensibility

### Loading Supplementary Skills

At runtime, the agent will:

1. Check for supplementary skills in `.cursor/skills/qa-automation-extensions/`
2. Load any skills matching pattern: `*-qa-extension.md`
3. Incorporate their patterns and knowledge into the automation workflow
4. Prioritize extension-specific patterns when conflicts arise

### When Extensions Are Loaded

Extensions are loaded when:
- **Auto-detection (NEW!)**: Feature file content/path analyzed for keywords
  - Keywords detected: "identity provider", "oauth", "mfa", "service account", etc.
  - Path detection: `features/auth/` → authentication, `features/sso/` → identity-providers
  - Smart detection from first 100 lines of feature file
- **JIRA ID prefix**: `SSO-123` → load `sso-service-qa-extension.md`
- **Explicit specification**: `--extension auth` or `--extension auth,identity-providers` (multi-extension support)
- **Skip auto-detection**: Use `--skip-auto-detect` for explicit control

**NEW: Multi-Extension Support**
```bash
# Load multiple extensions at once
jc-automate-test AUTH-123 features/oauth_idp.feature --extension authentication,identity-providers

# Auto-detection finds multiple (e.g., feature mentions "identity provider" and "oauth")
jc-automate-test AUTH-123 features/oauth_idp.feature  # Automatically loads both extensions
```

### Creating Team Extensions

Teams can create extensions containing:
- Service-specific testing patterns
- Common step definitions for their service
- Helper function patterns
- Known gotchas and solutions
- Service architecture specifics
- API/gRPC endpoint patterns
- **Service repository URLs** for source code context
- **Service names** for log inspection

**Example Extension with Service Context:**

`.cursor/skills/qa-automation-extensions/auth-service-qa-extension.md`:

```markdown
---
name: auth-service-qa-extension
description: Auth service testing patterns
extends: jumpcloud-qa-automation
service_repos:
  - https://github.com/TheJumpCloud/jumpcloud-auth
service_names:
  - auth-api
  - auth-internal-api
---

# Auth Service QA Extension

[Extension content...]
```

When this extension is loaded, the agent automatically:
- ✅ Clones/reads specified GitHub repos for source code understanding
- ✅ Collects logs from specified services on test failures
- ✅ Analyzes service behavior and correlates with test results

See EXTENSIBILITY.md for complete guide on creating extensions.

## Troubleshooting

### Prerequisites Issues

| Issue | Solution |
|-------|----------|
| `kubectl: command not found` | Install: `brew install kubectl` |
| `Error: Unauthorized` | Run `aws sso login` or configure kubeconfig |
| `namespace "wok-{username}" not found` | Request namespace from DevOps |
| `gh: command not found` | Install: `brew install gh` |
| `gh auth status: not logged in` | Run: `gh auth login` |
| `devspace: command not found` | Install: `brew install devspace` |
| `devspace pod failing to start` | Check logs: `kubectl logs -n wok-{username} {pod}` |

### Test Failures

**Connection refused to service:**
```bash
# Check service is running
kubectl get pods -n wok-{username}

# Check service address
kubectl get svc -n wok-{username}

# Port forward if needed
kubectl port-forward svc/auth-api 50051:50051 -n wok-{username}
```

**TOTP code already used:**
- Ensure using `get_fresh_totp_code()` helper
- Wait for fresh token window after TOTP configuration

**gRPC status code errors:**
- Use `.code()` method, not `.status_code` attribute
- Map gRPC codes to HTTP codes correctly

### Devspace Issues

**Pod not starting:**
```bash
# Check pod status
kubectl describe pod -n wok-{username} {pod-name}

# Check logs
kubectl logs -n wok-{username} {pod-name}

# Restart devspace
devspace purge
devspace dev --skip-build
```

**File sync not working:**
```bash
# Devspace auto-sync may not work immediately
# Manual copy is more reliable for testing
kubectl cp local/path/file.py wok-{username}/{pod}:/opt/jumpcloud-acceptance/path/file.py

# Copy multiple files
kubectl cp tests/python/helpers/webauthn.py wok-{username}/{pod}:/opt/jumpcloud-acceptance/tests/python/helpers/webauthn.py
kubectl cp tests/python/step_definitions/webauthn_mfa.py wok-{username}/{pod}:/opt/jumpcloud-acceptance/tests/python/step_definitions/webauthn_mfa.py
kubectl cp features/auth/webauthn.feature wok-{username}/{pod}:/opt/jumpcloud-acceptance/features/auth/webauthn.feature

# Verify files are synced
kubectl exec -n wok-{username} {pod} -- head -5 features/auth/webauthn.feature

# Clear Python cache after sync
kubectl exec -n wok-{username} {pod} -- rm -rf /opt/jumpcloud-acceptance/**/__pycache__
```

## Key Takeaways

1. **NEVER skip tests** - Implement properly, research service tests, ask for help
2. **Prerequisites are mandatory** - Validate before starting
3. **Real APIs > Mocking** - Always prefer real gRPC/API calls for acceptance tests
4. **Learn from service tests** - Clone service repos, study functional test patterns
5. **Devspace testing is non-negotiable** - NEVER commit without testing
6. **Implement real cryptography** - Use cryptography library, proper signatures
7. **Database-only TOTP** - Never use API enrollment in setup
8. **Fresh TOTP tokens** - Always wait for new token window
9. **gRPC status codes** - Use `.code()` method
10. **COSE format matters** - Don't re-encode COSE keys, use bytes directly
11. **Type hints for crypto** - Use isinstance() checks for union types
12. **Pre-commit checks** - Run BOTH configs (py + feature-files) before every commit
13. **No summary files** - Use PR descriptions directly
14. **Source code is truth** - Read service implementations
15. **Iterate on failures** - Up to 3 attempts with automated fixes
16. **Proper PR format** - Labels, title, description
17. **Dependency management** - Always update pyproject.toml AND poetry.lock with correct Poetry version
18. **Clean up temporary tags** - Remove @focus and @{jira_id} tags before committing
19. **target_fixture is critical** - ALWAYS add `target_fixture` parameter and return statement for fixtures
20. **Manual file sync** - Use `kubectl cp` for reliable devspace file sync; auto-sync may be delayed

## Agent Invocation

### Via CLI

```bash
jc-automate-test AUTH-123 jumpcloud-acceptance/features/auth/example.feature
```

### Via Cursor Chat

```
@automate-acceptance --jira AUTH-123 --feature jumpcloud-acceptance/features/auth/example.feature
```

### With Extensions

```
# Auto-detection (default)
@automate-acceptance --jira AUTH-123 --feature features/auth/oauth_idp.feature
# Agent auto-detects: authentication + identity-providers

# Single extension
@automate-acceptance --jira SSO-456 --feature features/sso/login.feature --extension sso

# Multiple extensions (NEW!)
@automate-acceptance --jira AUTH-123 --feature features/test.feature --extension authentication,identity-providers,users

# Skip auto-detection (explicit control)
@automate-acceptance --jira NA-3129 --feature features/test.feature --skip-auto-detect --extension users
```

---

**This agent is self-contained and ready for company-wide distribution. All necessary patterns and knowledge are embedded. Extensions are optional and service-specific.**
