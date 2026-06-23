# Origin CI Patterns

Docker and docker-compose patterns for Origin CI. Read only when CI = Origin.

Source: [jumpcloud-notifications](https://github.com/TheJumpCloud/jumpcloud-notifications)

## Table of Contents

- [Dockerfile](#dockerfile)
- [docker-compose.common.yml](#docker-composecommonyml)
- [docker-compose.yml](#docker-composeyml)
- [docker-compose.ci.yml](#docker-composeciyml)
- [Verification](#verification)

## Dockerfile

Multi-stage build. Replace `{app}` with app name. **If gRPC = No**, remove the `internal-api-builder` and `internal-api` stages entirely — only keep `base`, `builder`, `golang-builder`, `cli-builder`, and `cli`.

```dockerfile
# syntax=docker/dockerfile:1.2.1

FROM public.ecr.aws/docker/library/golang:1.26 as base
ENV GO111MODULE=on
ENV GOPRIVATE=github.com/TheJumpCloud
ENV GOFLAGS=-mod=readonly
RUN apt update && apt install --yes --quiet git openssh-client
RUN mkdir ~/.ssh \
  && ssh-keyscan github.com >> ~/.ssh/known_hosts \
  && git config --global url."git@github.com:".insteadOf "https://github.com/"
RUN git config --global --add safe.directory /go/src/github.com/TheJumpCloud/jumpcloud-{app}
ENV PROJECT jumpcloud-{app}
WORKDIR $GOPATH/src/github.com/TheJumpCloud/$PROJECT
COPY go.mod .
COPY go.sum .
RUN --mount=type=cache,target=/root/.cache/go-build \
  --mount=type=ssh \
  go mod download

FROM base as builder
RUN apt-get update && apt-get install --yes --quiet netcat-traditional unzip \
  && rm -rf /var/lib/apt/lists/*
COPY tools.go ./tools.go
COPY bin/configure bin/configure
RUN bin/configure

FROM base as golang-builder
ARG BUILD_DATE
ARG REVISION
ARG VERSION
COPY . .

FROM golang-builder as internal-api-builder
RUN --mount=type=cache,target=/root/.cache/go-build bin/build internal-api

FROM golang-builder as cli-builder
RUN --mount=type=cache,target=/root/.cache/go-build bin/build cli

FROM public.ecr.aws/docker/library/alpine:3.17 as internal-api
COPY --from=internal-api-builder /go/src/github.com/TheJumpCloud/jumpcloud-{app}/dist/jumpcloud-{app}-internal-api /jumpcloud-{app}-internal-api
ENV INTERFACE="[::]"
EXPOSE 8080
EXPOSE 9080
CMD ["/jumpcloud-{app}-internal-api"]

FROM debian:11 as cli
COPY --from=cli-builder /go/src/github.com/TheJumpCloud/jumpcloud-{app}/dist/jumpcloud-{app}-cli /
COPY bin/entrypoint.cli.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

## docker-compose.common.yml

Builder MUST mount SSH agent socket for private Go modules. **If gRPC = No**, remove the `internal-api` service block from all docker-compose files below.

```yaml
version: '2.3'
services:
  builder:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder
      ssh:
        - default
    image: jumpcloud/{app}-builder:${REVISION:-development}
    tty: true
    volumes:
      - .:/go/src/github.com/TheJumpCloud/jumpcloud-{app}
      - ${DOCKER_SSH_AUTH_SOCK:-/tmp/ssh_auth_sock}:/ssh-auth-sock
    environment:
      - SSH_AUTH_SOCK=/ssh-auth-sock

  internal-api:
    build:
      secrets:
        - aws-codeartifact-token
      context: .
      dockerfile: Dockerfile
      target: internal-api
      ssh:
        - default
      args:
        - REVISION=${REVISION:-development}
        - VERSION=${VERSION:-development}
    image: jumpcloud/{app}-internal-api:${REVISION:-development}
    tty: true

  cli:
    build:
      context: .
      dockerfile: Dockerfile
      target: cli
      ssh:
        - default
    image: jumpcloud/{app}-cli:${REVISION:-development}
    tty: true
    volumes:
      - .:/go/src/github.com/TheJumpCloud/jumpcloud-{app}
```

## docker-compose.yml

Local dev. Each service uses only TWO env files: `env/{service}.env` and `env/common.env`.

```yaml
version: '2.3'
services:
  internal-api:
    container_name: {app}-internal-api
    extends:
      file: docker-compose.common.yml
      service: internal-api
    env_file:
      - env/internal-api.env
      - env/common.env
    networks:
      - backend
    ports:
      - 9083:8080

  cli:
    extends:
      file: docker-compose.common.yml
      service: cli
    env_file:
      - env/cli.env
      - env/common.env
    working_dir: /go/src/github.com/TheJumpCloud/jumpcloud-{app}
    volumes:
      - .:/go/src/github.com/TheJumpCloud/jumpcloud-{app}
    networks:
      - backend

networks:
  backend:
    external: true
```

## docker-compose.ci.yml

Must include `secrets` section for AWS CodeArtifact.

```yaml
version: '2.3'
services:
  builder:
    extends:
      file: docker-compose.common.yml
      service: builder
    env_file:
      - env/common.env

  cli:
    extends:
      file: docker-compose.common.yml
      service: cli
    env_file:
      - env/cli.env
      - env/common.env
    volumes:
      - .:/go/src/github.com/TheJumpCloud/jumpcloud-{app}

  internal-api:
    extends:
      file: docker-compose.common.yml
      service: internal-api
    env_file:
      - env/internal-api.env
      - env/common.env
    ports:
      - 8010:8080

secrets:
  aws-codeartifact-token:
    file: ${JUMPCLOUD_WORKSPACE}/jumpcloud-workstation/.aws-codeartifact-token
```

## Verification

**This step is mandatory. Run every command below in order. Each must pass. Fix failures before moving to the next command. Do not skip any.**

```bash
# 1. Ensure SSH keys loaded (required for Docker builds with private Go modules)
ssh-add -l || ssh-add

# 2. Validate docker-compose syntax
docker compose --file docker-compose.ci.yml config --quiet

# 3. Build all images — run each, do not stop after builder
docker compose --file docker-compose.ci.yml build builder
docker compose --file docker-compose.ci.yml build cli
# Only if gRPC = Yes:
docker compose --file docker-compose.ci.yml build internal-api

# 4. Run lint — fix any lint errors before proceeding
docker compose --file docker-compose.ci.yml run --rm builder bin/lint go

# 5. Run tests — fix any test failures before proceeding
docker compose --file docker-compose.ci.yml run --rm builder bin/test go
```

If any command fails:
- **SSH errors**: Run `ssh-add` and retry.
- **Build fails**: Check Dockerfile, go.mod, or tools.go. Fix and rebuild.
- **Lint fails**: Fix the reported lint issues in source code, then rerun.
- **Test fails**: Fix the failing tests, then rerun.

Verification is complete only when all 5 steps above pass.
