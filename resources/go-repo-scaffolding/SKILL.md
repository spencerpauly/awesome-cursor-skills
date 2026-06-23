---
name: go-repo-scaffolding
description: Scaffold a new JumpCloud Go application repository following internal standards, including CI configuration, Go module setup, service structure, database scaffolding, and cross-repo PRs for inventory-mapping, spacelift, and terraform-aws-oidc. Supports Taskfile or Origin CI pipelines and optional gRPC internal-api services. Use when setting up a new JumpCloud repo, scaffolding a Go service, bootstrapping a jumpcloud-{app} project, or following the JumpCloud new repo runbook.
---

# JumpCloud New Repo Setup

[Runbook](https://jumpcloud.atlassian.net/wiki/spaces/ET/pages/2840985671/Runbook+Creating+a+new+Repo) | Single-shot: [PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md)

## Critical Rules

- **Always use `gh api` or `gh` CLI to fetch files from GitHub.** Never use raw `https://` URLs, `curl`, or `wget` against GitHub — `gh` handles auth automatically.
- **NEVER run `docker login` or `aws ecr get-login-password`.** Origin images use pre-configured ECR credentials. Docker login is not needed at any step.
- **NEVER create repos via `gh repo create`.** Only clone existing repos.
- **Auto-detect app name** from the current `jumpcloud-{app}` directory when possible; ask the user otherwise.

## 0. Prerequisites

**Run all checks. Stop on any failure — ask user to fix before continuing.**

```bash
gh auth status          # gh auth login if needed
git --version
go version
aws sts get-caller-identity  # aws sso login if expired
docker info             # open -a Docker on macOS if not running
```

**If Taskfile CI**: also verify `task --version` (install: `brew install go-task/tap/go-task`).

## 1. Gather Inputs

| Input | Required | Valid Values |
|-------|----------|-------------|
| Ticket ID | yes | e.g. `GIR-2119` |
| App name | auto-detect or ask | e.g. `connector` |
| Team name | yes | Any string |
| CI type | yes | `Taskfile` or `Origin` |
| gRPC Service | yes | `Yes` or `No` |

Error on invalid CI or gRPC values.

## 2. Clone Repos

Clone these repos: app repo, inventory-mapping, spacelift-terraform-infra, terraform-aws-oidc.

- **Exists locally**: `git status --porcelain`. Untracked (`??`) OK. Modified tracked files → stop, ask user to resolve.
- **Not exists**: `git clone git@github.com:TheJumpCloud/repo-name.git`. Clone fails → stop with error.

**App repo only — establish `master` as default branch BEFORE creating a feature branch.**
An empty GitHub repo has no default branch. The first branch pushed becomes the default.

```bash
BASE_PATH="${BASE_PATH:-/Users/${USER}/go/src/github.com/TheJumpCloud}"
cd $BASE_PATH/jumpcloud-{app_name}
# Check if repo is empty (no commits)
if ! git rev-parse HEAD >/dev/null 2>&1; then
  git checkout -b master
  echo "# jumpcloud-${app_name}" > README.md
  git add README.md
  git commit -m "Initial commit"
  git push -u origin master
fi
```

Then for all repos: `git checkout -b <ticket_id>`

## 3. Go Module Init

```bash
go mod init github.com/TheJumpCloud/jumpcloud-{app_name}
```

Run `go mod tidy` after each step that adds imports. Never manually edit go.mod or go.sum.

## 4. Origin Setup

Create `.origin/cicd/cicd.lock.yaml` BEFORE running Origin:

```yaml
artifact_name: jumpcloud-{app_name}
cd:
  strategy: github-actions
  create_release_and_testrails: true
  kargo: true
  environments:
    prd:
      strategy: none
    stg01:
      strategy: github-actions
ci:
  build:
    python: false
  migration:
    enabled: true
    tool: github.com/pressly/goose/cmd/goose
acceptance_tests: false
image_promotion_config:
  push_to_cicd: true
  secure_promotion_process: true
  remove_prod_access: true
```

Create `app.yaml`:

**CLI only** (gRPC = No):
```yaml
name: {app_name}
team: {team_name}
generate:
  cicd: true
images:
  - name: cli
    type: cobra
```

**CLI + gRPC** (gRPC = Yes):
```yaml
name: {app_name}
team: {team_name}
generate:
  cicd: true
images:
  - name: cli
    type: cobra
  - name: internal-api
    type: grpc
services:
  - name: internal-api
    image: internal-api
```

Run Origin and create `.origin/version` (required by CI `install-origin` action). Do **not** modify Origin-generated files except `.origin/version`.

```bash
ORIGIN_VERSION=$(gh release view --repo TheJumpCloud/jumpcloud-origin --json tagName -q .tagName)
docker run --rm --workdir "$(pwd)" -v "$(pwd):$(pwd)" 868503801984.dkr.ecr.us-west-2.amazonaws.com/jumpcloud/origin:${ORIGIN_VERSION} init
docker run --rm --workdir "$(pwd)" -v "$(pwd):$(pwd)" 868503801984.dkr.ecr.us-west-2.amazonaws.com/jumpcloud/origin:${ORIGIN_VERSION} generate
echo "${ORIGIN_VERSION}" > .origin/version
```

## 5. Service Structure

**CLI** (always): Create `cmd/cli/main.go` — standard cobra CLI.

**Always create `tools.go`** at repo root — required by Origin Dockerfile (`COPY tools.go`) and `bin/configure` even for CLI-only repos. See [references/service-patterns.md § tools.go](references/service-patterns.md) for exact code.

**If gRPC = Yes**: Read [references/service-patterns.md](references/service-patterns.md) for exact code. Create:
- `cmd/connect.go` (NOT services.go), `cmd/internal-api/main.go`
- `config/source.go`, `config/build.go`, `config/common.go`, `config/internal_api.go`
- `services/{name}_service.go`

Then: `go mod tidy`

## 6. CI Configuration

Fetch `.gitignore` from [jumpcloud-public-workflows](https://github.com/TheJumpCloud/jumpcloud-public-workflows) (common to both CI types — keeps `bins/`, build artifacts, and IDE files out of git):

```bash
gh api repos/TheJumpCloud/jumpcloud-public-workflows/contents/.gitignore --jq '.content' | base64 -d > .gitignore
```

**If Taskfile**: Read [references/taskfile-ci.md](references/taskfile-ci.md). Fetch workflows, Dockerfile.TaskFile, and `.golangci.yml` from [jumpcloud-public-workflows](https://github.com/TheJumpCloud/jumpcloud-public-workflows) via `gh api`. Create `Taskfile.yml`. Run verification — all task commands must pass.

**If Origin**: Read [references/origin-ci.md](references/origin-ci.md). Create Dockerfile, docker-compose.common.yml, docker-compose.yml, docker-compose.ci.yml. Do NOT modify Origin-generated bin/ scripts.

## 7. Database & Env Files

Fetch db scripts from [jumpcloud-public-workflows/db](https://github.com/TheJumpCloud/jumpcloud-public-workflows/tree/master/db):

```bash
mkdir -p db env
for f in create drop wait dbconf.yml; do
  gh api repos/TheJumpCloud/jumpcloud-public-workflows/contents/db/$f --jq '.content' | base64 -d > db/$f
done
chmod +x db/create db/drop db/wait
mkdir -p db/migrations
```

Create env files — replace `{app_name}` (use underscores for db name):

- `env/common.env` — POSTGRES_HOST, PORT, USER, PASSWORD, DATABASE={app_name}_local
- `env/cli.env` — CLI-specific vars
- `env/internal-api.env` — INTERFACE=[::], PORT=8080

## 8. Verify

**Mandatory. Do not skip. Run every command, fix every failure before proceeding.**

```bash
go mod tidy
```

- **Taskfile CI**: Run full verification from [references/taskfile-ci.md § Verification](references/taskfile-ci.md). All tasks must pass.
- **Origin CI**: Run full verification from [references/origin-ci.md § Verification](references/origin-ci.md). All builds, lint, and tests must pass.

## 9. Inventory Mapping, Spacelift & Terraform OIDC

**inventory-mapping**: Add `TheJumpCloud/jumpcloud-{app_name}` under team's `repos:` in `inventory.yaml`. Alphabetical order.

**spacelift**: Add in `app-stacks/app_stacks.tf` under `locals.apps`:
```hcl
{short_name} = { slack_channel = "#maintainers-jumpcloud-{app_name}" }
```

**terraform-aws-oidc**: Add `"{app_name}"` (the short name, without the `jumpcloud-` prefix) to the `standard_apps` list in `terraform/ci/data.tf`. Insert in **alphabetical order** among existing entries. This registers the repo for CI OIDC role provisioning.

Example — if app name is `identity-risk`, the entry `"identity-risk"` is inserted between `"identity-providers"` and `"idm"`:
```hcl
      "identity-providers",
      "identity-risk",
      "idm",
```

## 10. Labels & PR Creation

**Ask user for confirmation first.** Once confirmed:

**1. Create repo labels** — read [references/labels.md](references/labels.md) and run all `gh label create` commands for the app repo. New repos only have 9 default GitHub labels; this adds the 18 JumpCloud-standard labels (version labels, AI labels, testing labels, etc.).

**2. Create PRs:**

```bash
git add . && git commit -m "[TICKET_ID]: Add {app_name} setup" && git push -u origin <ticket_id>
gh pr create --title "[TICKET_ID] Initial setup for jumpcloud-{app_name}" --body "New repo setup." --base master
```

Repeat for inventory-mapping, spacelift, and terraform-aws-oidc repos with appropriate titles.

## 11. README

- **Taskfile CI**: Quick start with Task. Fetch structure from [jumpcloud-public-workflows README](https://github.com/TheJumpCloud/jumpcloud-public-workflows/blob/master/README.md).
- **Origin CI**: Fetch and customize from [jumpcloud-starter README](https://github.com/TheJumpCloud/jumpcloud-starter/blob/master/README.md). Only docker compose commands.

**Include a "Tests" note in the README** for Taskfile CI repos:
> Unit test reporting is disabled by default. When you add unit tests, uncomment the `test:unit-report` task in `Taskfile.yml` and uncomment the "Run unit tests" / "Publish Unit Tests Report" steps in `.github/workflows/new-ci.yml`.

End with: "**Repo scaffolding done with the help of Skills.**"

## Manual Checklist

Call out to user:
- Slack: `#alerts-jumpcloud-{app}`, `#maintainers-jumpcloud-{app}` — invite @Datadog, @OriginBot, @Github, @CI Messaging Bot
- PagerDuty escalation policy
- Readiness Review + Threat Model before production
- If Taskfile CI: disable `ci.origin.yml` in GitHub Actions

## CI Dependency: terraform-aws-oidc PR

The terraform-aws-oidc PR **must be merged** before the new repo's CI will pass. Without it, CI fails with `Not authorized to perform sts:AssumeRoleWithWebIdentity`. Always call this out to the user at the end.

## Completion Gate

Do not mark complete until every step 0–11 has executed and verified. Step 8 (Verify) must pass with all commands succeeding. Fix failures before moving on.
