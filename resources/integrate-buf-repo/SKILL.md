---
name: integrate-buf-repo
description: Integrate buf (protobuf lint and codegen) with protodep and Docker in a new or existing repository. Use when setting up buf in a new repo, adding or updating buf in an existing repo, adding protobuf tooling, or following JumpCloud-style buf + protodep workflow. When the integration is complete, open a draft PR and mark it ready after CI and review.
---

# Integrate Buf in a Repo (New or Existing)

Guides setting up [buf](https://buf.build/docs) for lint and code generation in a new or existing repo, with protodep for external proto dependencies and Docker for consistent tooling. For an existing repo, add or update only what is missing (e.g. add `buf.work.yaml` if absent, or update README.md and proto/README.md to match the current workflow).

## Prerequisites

- Repo has or will have `.proto` files under a `proto/` tree (e.g. `proto/jumpcloud/<service>/`).
- Optional: external proto deps (e.g. jumpcloud-protobuf) via [protodep](https://github.com/stormcat24/protodep).

**Existing repos:** Add only missing config files and steps; update README.md and proto/README.md so they reflect the current buf/protodep workflow (don’t duplicate or contradict existing content).

## Workflow Overview

1. Add buf config (workspace, module lint, codegen).
2. Add protodep config and wrapper if using external deps.
3. Add Docker Compose tool service for lint/generate.
4. Wire CI to run lint, generate, and verify generated files are committed.
5. Update **README.md** and **proto/README.md** so proto workflow is documented.

## Step 1: Buf configuration

**Root `buf.work.yaml`** – list all proto roots (repo protos + deps):

```yaml
version: v1
directories:
  - proto
  - .protodep
```

Omit `.protodep` if the repo has no protodep dependencies.

**Per-module `buf.yaml`** – one under `proto/` for repo protos:

```yaml
version: v1
lint:
  use:
    - MINIMAL
```

**If using protodep** – add `.protodep/buf.yaml` (commit it; `bin/protodep up` will overwrite it, so restore after `protodep up`):

```yaml
version: v1
lint:
  use:
    - BASIC
  ignore:
    - jumpcloud
```

**Root `buf.gen.yaml`** – codegen plugins and options. Adjust `module` and `out` for the repo’s Go module and paths. Example (Go + gRPC + optional grpcqueue + OpenAPI):

```yaml
version: v1
plugins:
  - name: go
    out: proto/
    opt:
      - module=<go-module-path>/proto
  - name: go-grpc
    out: proto/
    opt:
      - module=<go-module-path>/proto
      - require_unimplemented_servers=false
  - name: go-grpcqueue
    out: proto/
    opt:
      - module=<go-module-path>/proto
  - name: openapiv2
    out: proto/
    opt:
      - allow_merge=true
      - merge_file_name=index.yaml
      - openapi_naming_strategy=fqn
      - disable_default_errors=true
      - output_format=yaml
      - proto3_optional_nullable=true
```

Replace `<go-module-path>` with the repo’s Go module (e.g. `github.com/TheJumpCloud/jumpcloud-identity-risk`).

## Step 2: Protodep (optional)

If the repo imports protos from another repo (e.g. jumpcloud-protobuf):

1. **protodep.toml** at repo root – set `proto_outdir = "./.protodep"` and list dependencies with `target`, `revision`, and optional `includes`/`excludes`.
2. **bin/protodep** – wrapper script that runs `protodep "$@"` and, on `up`, restores `.protodep/buf.yaml` (because `protodep up` overwrites it).
3. Install protodep locally; document in proto/README or main README.
4. Add `bin/protodep up -f` to docs for “update proto deps”.

## Step 3: Docker Compose tools service

Add a `docker-compose.tools.yml` (or extend existing) with a service that uses the same image and working dir as CI:

```yaml
version: '3.8'
services:
  protobuf:
    image: "${AWS_ACCOUNT_NUMBER}.dkr.ecr.${AWS_ECR_REGION}.amazonaws.com/jumpcloud/protobuf:${JUMPCLOUD_PROTOBUF_VERSION}"
    tty: true
    working_dir: /go/src/github.com/<org>/<repo>
    volumes:
      - .:/go/src/github.com/<org>/<repo>
```

Ensure `.env` or CI provides `AWS_ACCOUNT_NUMBER`, `AWS_ECR_REGION`, `JUMPCLOUD_PROTOBUF_VERSION`. The image should have `buf` and codegen plugins; entrypoint typically runs `buf lint` for `lint` and `buf generate` for `generate`.

**Local commands:**

```bash
docker compose --file docker-compose.tools.yml run --rm protobuf lint
docker compose --file docker-compose.tools.yml run --rm protobuf generate
```

After generate: `go mod tidy` if Go files were generated.

## Step 4: CI

In the workflow that validates protos:

1. Checkout (with submodules if protodep uses them).
2. Run: `docker compose --file docker-compose.tools.yml run --rm protobuf lint`
3. Run: `docker compose --file docker-compose.tools.yml run --rm protobuf generate`
4. Ensure generated files are committed:  
   `git diff --compact-summary --exit-code --stat=1000 proto/`  
   (or equivalent path). Fail the job if there are uncommitted changes.

## Step 5: Open a draft PR (when ready)

When the integration is complete and local lint/generate pass:

1. Commit all buf-related changes (configs, protodep wrapper, docker-compose, CI, docs).
2. Push the branch and **open the PR as a draft** so reviewers can see the full diff and CI can run before marking it ready.
3. After CI passes and feedback is addressed, mark the PR ready for review.

Use GitHub’s “Create draft pull request” (or `gh pr create --draft`) so the PR starts in draft state.

## Step 6: Update README.md and proto/README.md

Document the proto workflow in both files so others can lint, generate, and update deps.

**README.md** (repo root) – add or update an "Updating Proto Files" (or similar) section that includes:

- Where repo protos live (e.g. `proto/jumpcloud/<service>/`).
- Breaking-change rules: don't reuse/change field numbers (use reserved if deleting); avoid renaming existing messages/RPCs; adding new elements is generally safe.
- That new proto imports may require updating deps via protodep, with a link to **proto/README.md**.
- Exact commands to lint and generate (e.g. `docker compose --file docker-compose.tools.yml run --rm protobuf lint` then `generate`), and `go mod tidy` after generate if applicable.

**proto/README.md** – add or update so it covers:

- How to modify proto dependencies: edit `protodep.toml` (update revision or add a new `[[dependencies]]`), then run `bin/protodep up -f`. Optionally document protodep install as a prerequisite.
- How to (re)generate code after changing `.proto` files: same lint + generate Docker commands as in the main README.

Adjust section titles and paths to match the repo (e.g. replace "jumpcloud/insights" with the actual proto path). Create **proto/README.md** if it does not exist.

## Checklist

- [ ] `buf.work.yaml` with correct `directories`
- [ ] `proto/buf.yaml` (and `.protodep/buf.yaml` if using protodep)
- [ ] `buf.gen.yaml` with correct `module` and desired plugins
- [ ] `protodep.toml` + `bin/protodep` if using external proto deps
- [ ] `docker-compose.tools.yml` protobuf service and env vars
- [ ] CI job runs lint → generate → git diff on generated paths
- [ ] **README.md** updated: proto location, breaking-change rules, link to proto/README, lint/generate commands (and `go mod tidy` if needed).
- [ ] **proto/README.md** updated or created: how to change protodep.toml and run `bin/protodep up -f`; how to run lint/generate.
- [ ] When everything looks good: open a **draft** PR; mark ready after CI passes and review is addressed.

## Additional resources

- File templates and example CI snippet: [reference.md](reference.md)
