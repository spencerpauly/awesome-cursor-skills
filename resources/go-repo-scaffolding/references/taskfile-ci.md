# Taskfile CI Patterns

Taskfile and Docker setup for Taskfile CI. Read only when CI = Taskfile.

Source: [jumpcloud-public-workflows](https://github.com/TheJumpCloud/jumpcloud-public-workflows)

## Table of Contents

- [Files to fetch from repo](#files-to-fetch-from-repo)
- [Taskfile.yml template](#taskfileyml-template)
- [Dockerfile.TaskFile reference](#dockerfiletaskfile-reference)
- [Verification](#verification)

## Files to fetch from repo

Fetch these directly via `gh api` — do not hardcode:

```bash
# GitHub Actions workflows
mkdir -p .github/workflows
gh api repos/TheJumpCloud/jumpcloud-public-workflows/contents/.github/workflows/new-ci.yml \
  --jq '.content' | base64 -d > .github/workflows/new-ci.yml
gh api repos/TheJumpCloud/jumpcloud-public-workflows/contents/.github/workflows/publish-ecr-images.yml \
  --jq '.content' | base64 -d > .github/workflows/publish-ecr-images.yml

# Dockerfile.TaskFile
gh api repos/TheJumpCloud/jumpcloud-public-workflows/contents/Dockerfile.TaskFile \
  --jq '.content' | base64 -d > Dockerfile.TaskFile

# golangci-lint config (required for go:lint to work)
gh api repos/TheJumpCloud/jumpcloud-public-workflows/contents/.golangci.yml \
  --jq '.content' | base64 -d > .golangci.yml
```

### Patch new-ci.yml after fetching

The upstream `new-ci.yml` is written for the `jumpcloud-public-workflows` repo. After fetching, apply **all** of these changes to `.github/workflows/new-ci.yml`:

**1. Rename `jumpcloud-public-workflows` to `jumpcloud-{app_name}`** throughout the file. The checkout `path:`, `uses:`, `version_file:`, and `working-directory:` all reference the repo name — replace every occurrence:

- `jumpcloud-public-workflows` → `jumpcloud-{app_name}`

**2. Handle missing tests** — no tests exist in a freshly scaffolded repo:

- Comment out the "Run unit tests" step (the one calling `task test:unit-report`), the "Publish Unit Tests Report" step, the "Run functional tests" step, and the "Publish Functional Tests Report" step entirely
- The `test:unit-report` task is also commented out in the Taskfile — both must be uncommented together when unit tests are added
- Without tests, `go-junit-report` produces an empty report that fails the publisher action's `require_passed_tests` check

Teams should uncomment these workflow steps AND the `test:unit-report` Taskfile task when they add tests.

## Taskfile.yml template

Replace `{app}` with app name. Remove `internal-api` from SERVICES if gRPC = No.Keep only the minimum that is required.

```yaml
version: 3

vars:
  SERVICES:
    - cli
    - internal-api

env:
  BUILD_DATE:
    sh: date

tasks:
  origin:generate:
    cmds:
      - bin/origin generate

  clean:artifacts:
    desc: Clean up artifacts
    cmds:
      - rm -rf bins/ logs/
      - mkdir -p bins/ logs/

  deps:install:
    desc: Install required dependencies
    cmds:
      - curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v2.3.0
      - go install github.com/jstemmer/go-junit-report/v2@latest
      - go install -tags nosqlite3,nomysql,nomymysql github.com/pressly/goose/v3/cmd/goose
      - mkdir -p bins/
    status:
      - golangci-lint --version | grep 2.3.0
      - go-junit-report --version | grep v2
      - goose

  go:lint:
    desc: Run lint
    cmd: golangci-lint run

  go:lint:fix:
    desc: Run lint fix
    cmd: golangci-lint run --fix ./...

  go:fmt:
    desc: Run fmt
    cmd: golangci-lint fmt ./...

  go:update-deps:
    desc: Update deps
    cmd: go get -u all

  services:compile:
    desc: Compile all services
    cmds:
      - mkdir -p bins
      - for: { var: SERVICES }
        cmd: |
          LDFLAGS=${LDFLAGS:-""}
          REVISION=${REVISION:-"development"}
          VERSION=${VERSION:-"development"}
          REPO_NAME="jumpcloud-{app}"
          LDFLAGS+=" -X \"github.com/TheJumpCloud/${REPO_NAME}/config.BuildDate='${BUILD_DATE}'\""
          LDFLAGS+=" -X \"github.com/TheJumpCloud/${REPO_NAME}/config.Revision=${REVISION}\""
          LDFLAGS+=" -X \"github.com/TheJumpCloud/${REPO_NAME}/config.Version=${VERSION}\""
          time go build -ldflags "${LDFLAGS}" -o bins/jumpcloud-{app}-{{.ITEM}} cmd/{{.ITEM}}/main.go

  service:start:
    desc: Run a service
    dotenv:
      - env/{{ .SERVICE }}.env
      - env/common.env
    cmds:
      - mkdir -p logs/
      - bash -c "bins/jumpcloud-{app}-{{ .SERVICE }} > logs/{{ .SERVICE }}.log 2>&1 & echo \$! > logs/{{ .SERVICE }}.pid"

  service:kill:
    desc: Kill a service
    ignore_error: true
    cmds:
      - kill $(cat logs/{{ .SERVICE }}.pid)

  services:start-all:
    desc: Run all services
    cmds:
      - for: { var: SERVICES }
        if: '{{.ITEM}} != "cli"'
        task: service:start
        vars:
          SERVICE: '{{.ITEM}}'

  services:kill-all:
    desc: Kill all services
    cmds:
      - for: { var: SERVICES }
        if: '{{.ITEM}} != "cli"'
        task: service:kill
        vars:
          SERVICE: '{{.ITEM}}'

  test:unit:
    desc: Run unit tests
    cmd: go test $(go list ./... | grep -v /test/)
    dotenv:
      - env/common.env

  # Uncomment test:unit-report when unit tests are added.
  # Without tests, go-junit-report produces an empty report that fails
  # the CI "Publish Unit Tests Report" step (require_passed_tests).
  # test:unit-report:
  #   cmd: go test -json $(go list ./... | grep -v /test/) | go-junit-report -iocopy -parser gojson -set-exit-code -out report-unit.xml
  #   dotenv:
  #     - env/common.env

  # If gRPC = Yes:
  service:run:local:
    desc: Run a service locally
    cmd: go run cmd/internal-api/main.go
    dotenv:
      - env/internal-api.env
      - env/common.env
  # If gRPC = No, replace with:
  # service:run:local:
  #   desc: Run CLI locally
  #   cmd: go run cmd/cli/main.go
  #   dotenv:
  #     - env/cli.env
  #     - env/common.env

  docker:build:
    desc: Build the docker images
    cmds:
      - for: { var: SERVICES }
        if: '{{.ITEM}} != "cli"'
        cmd: |
          docker build --target=internal-api --build-arg BINARY_NAME=jumpcloud-{app}-{{.ITEM}} -t jumpcloud/{app}-{{.ITEM}}:${REVISION:-development} . -f Dockerfile.TaskFile
      - cmd: cp ~/go/bin/goose bins/goose
      - docker build --target=cli -t jumpcloud/{app}-cli:${REVISION:-development} . -f Dockerfile.TaskFile

  ci:ecr:push:
    desc: Push all images to ECR (CI only)
    cmds:
      - bin/ecr push {{join " " .SERVICES}}

  ci:ecr:tag:
    desc: Tag images (CI only)
    cmds:
      - bin/ecr tag {{join " " .SERVICES}}
```

## Dockerfile.TaskFile reference

Fetched from [jumpcloud-public-workflows/Dockerfile.TaskFile](https://github.com/TheJumpCloud/jumpcloud-public-workflows/blob/master/Dockerfile.TaskFile). Key structure:

```dockerfile
FROM public.ecr.aws/docker/library/alpine:3.20 AS base
LABEL org.opencontainers.image.source="https://github.com/TheJumpCloud/jumpcloud-{app}"
RUN apk add --no-cache gcompat libc6-compat curl

FROM base AS internal-api
ARG BINARY_NAME
ADD bins/${BINARY_NAME} /internal-api
ENV INTERFACE="[::]"
EXPOSE 8080
ENTRYPOINT ["/internal-api"]
HEALTHCHECK CMD curl --fail --silent http://localhost:8080/healthcheck

FROM base AS cli
RUN apk --no-cache add postgresql-client bash gcompat libc6-compat jq
COPY db/migrations/ db/migrations
COPY db/dbconf.yml db/dbconf.yml
COPY db/create db/create
COPY db/wait db/wait
COPY db/drop db/drop
COPY bin/entrypoint.cli.sh /entrypoint.sh
COPY bins/goose /usr/local/bin/goose
COPY bins/jumpcloud-{app}-cli /jumpcloud-{app}-cli
ENTRYPOINT ["/entrypoint.sh"]
```

Build flow: `task services:compile` → `task docker:build` → `task ci:ecr:push`

## Verification

**This step is mandatory.** After Taskfile setup, run every task command except `ci:ecr:push` and `ci:ecr:tag`. All must pass. Fix any lint or test failures before proceeding.

```bash
task deps:install
task services:compile
task go:lint
task test:unit
task docker:build
```

If `go:lint` fails, check that `.golangci.yml` was fetched and fix the reported issues. If `test:unit` fails, fix the failing tests. Do not skip this step.
