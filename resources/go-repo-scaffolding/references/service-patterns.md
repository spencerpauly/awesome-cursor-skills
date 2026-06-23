# Service Patterns

JumpCloud-specific Go service patterns. Read when gRPC Service = Yes.

Source: [jumpcloud-notifications](https://github.com/TheJumpCloud/jumpcloud-notifications)

## Table of Contents

- [Directory structure](#directory-structure)
- [cmd/connect.go](#cmdconnectgo)
- [cmd/internal-api/main.go](#cmdinternalapimaingomaingo)
- [services/](#services)
- [config/source.go](#configsourcego)
- [config/build.go](#configbuildgo)
- [config/common.go](#configcommongo)
- [config/internal_api.go](#configinternal_apigo)
- [tools.go](#toolsgo)

## Directory structure

```
jumpcloud-{app}/
├── cmd/
│   ├── cli/main.go
│   ├── internal-api/main.go
│   └── connect.go            # NOT services.go
├── config/
│   ├── source.go
│   ├── build.go
│   ├── common.go
│   └── internal_api.go
├── services/
│   └── {name}_service.go
└── tools.go
```

## cmd/connect.go

**Convention**: Named `connect.go`, not `services.go`.

```go
package cmd

import (
	"fmt"
	"io"

	jcconcurrency "github.com/TheJumpCloud/jumpcloud-common-go/v5/concurrency"
	jcinstrumentation "github.com/TheJumpCloud/jumpcloud-common-go/v5/instrumentation"
	"google.golang.org/grpc"
	"google.golang.org/grpc/health"
	"google.golang.org/grpc/health/grpc_health_v1"

	"github.com/TheJumpCloud/jumpcloud-{app}/config"
	"github.com/TheJumpCloud/jumpcloud-{app}/services"
)

type Closers []func() error

type InternalAPIService struct {
	*health.Server
	cfg    *config.InternalAPI
	bundle *jcinstrumentation.Bundle
}

func CreateInternalAPIServices(cfg *config.InternalAPI, bundle *jcinstrumentation.Bundle) (*InternalAPIService, io.Closer, error) {
	var closers Closers
	var err error

	s := &InternalAPIService{
		Server: health.NewServer(),
		cfg:    cfg,
		bundle: bundle,
	}

	defer func() {
		if err != nil {
			jcconcurrency.Parallel(closers...)
		}
	}()

	// Initialize services here

	s.SetServingStatus("", grpc_health_v1.HealthCheckResponse_SERVING)
	return s, &serviceCloser{closers: closers}, nil
}

func (s *InternalAPIService) BindInternalServices(server *grpc.Server) {
	grpc_health_v1.RegisterHealthServer(server, s)
}

func (s *InternalAPIService) Start() error {
	s.bundle.Logger().Info("internal API services started")
	return nil
}

func (s *InternalAPIService) Stop() error {
	s.bundle.Logger().Info("internal API services stopped")
	return nil
}

type serviceCloser struct{ closers Closers }

func (c *serviceCloser) Close() error {
	if len(c.closers) == 0 {
		return nil
	}
	errs := jcconcurrency.Parallel(c.closers...)
	if len(errs) > 0 {
		return fmt.Errorf("error closing services: %v", errs)
	}
	return nil
}
```

## cmd/internal-api/main.go

```go
package main

import (
	"fmt"

	jccmd "github.com/TheJumpCloud/jumpcloud-common-go/v5/cmd"
	jcgrpc "github.com/TheJumpCloud/jumpcloud-common-go/v5/grpc"
	jcinstrumentation "github.com/TheJumpCloud/jumpcloud-common-go/v5/instrumentation"

	"github.com/TheJumpCloud/jumpcloud-{app}/cmd"
	"github.com/TheJumpCloud/jumpcloud-{app}/config"
)

func main() {
	cfg, err := config.NewInternalAPI()
	if err != nil {
		panic(fmt.Sprintf("failed to load configuration: %s", err))
	}

	bundle, errInst := jcinstrumentation.NewAPI(cfg.API)
	if errInst != nil {
		panic(fmt.Sprintf("failed to load instrumentation: %s", errInst))
	}
	logger := bundle.Logger()
	defer bundle.Close()

	logger.WithFields(cfg.BannerFields()).Info("starting")

	svcs, closer, err := cmd.CreateInternalAPIServices(cfg, bundle)
	if err != nil {
		logger.WithError(err).Fatal("failed to create services")
	}
	defer closer.Close()

	server := jcgrpc.NewServer(cfg.API, bundle)
	svcs.BindInternalServices(server)

	jccmd.Start(bundle, svcs,
		jcgrpc.ListenAndServeTask(cfg.API, bundle, server))
}
```

## services/

Business logic lives here, separate from cmd/.

```go
package services

import jclog "github.com/TheJumpCloud/jumpcloud-common-go/v5/log"

type ExampleService struct {
	logger jclog.Logger
}

func NewExampleService(logger jclog.Logger) *ExampleService {
	return &ExampleService{logger: logger}
}
```

Initialize in `cmd/connect.go` via `services.NewExampleService(bundle.Logger())`.

## config/source.go

```go
package config

import jcconfig "github.com/TheJumpCloud/jumpcloud-common-go/v5/config"

func NewSource(defaults map[string]interface{}) jcconfig.Source {
	return jcconfig.NewEnvironmentSource(defaults)
}
```

## config/build.go

```go
package config

import jcconfig "github.com/TheJumpCloud/jumpcloud-common-go/v5/config"

var (
	BuildDate string
	Revision  string
	Version   string
)

func newBuildInfo() *jcconfig.BuildInfo {
	return &jcconfig.BuildInfo{Date: BuildDate, Revision: Revision, Version: Version}
}
```

## config/common.go

```go
package config

import (
	"fmt"
	jcconfig "github.com/TheJumpCloud/jumpcloud-common-go/v5/config"
)

const KeyEvents = "events"

var commonDefaults = map[string]interface{}{
	KeyEvents: map[string]interface{}{
		jcconfig.KeyEventType:    jcconfig.FileEventType,
		jcconfig.KeyEventLogPath: "/var/log/jumpcloud-events/{app}-events.log",
	},
}

type Common struct {
	clientTLS *jcconfig.ClientTLSConfig
	events    *jcconfig.Events
}

func newCommon(source jcconfig.Source) (cfg *Common, err error) {
	source.SetDefaults(commonDefaults)
	cfg = new(Common)
	if cfg.clientTLS, err = jcconfig.NewClientTLSConfig(source.Sub("client")); err != nil {
		return nil, fmt.Errorf("failed to load common TLS client configuration: %w", err)
	}
	if cfg.events, err = jcconfig.NewEvents(source.Sub(KeyEvents)); err != nil {
		return nil, fmt.Errorf("failed to load events configuration: %w", err)
	}
	return cfg, nil
}

func (c *Common) ClientTLS() *jcconfig.ClientTLSConfig { return c.clientTLS }
func (c *Common) Events() *jcconfig.Events              { return c.events }
```

## config/internal_api.go

```go
package config

import (
	"fmt"
	"strings"
	jcconfig "github.com/TheJumpCloud/jumpcloud-common-go/v5/config"
)

const internalAPIServiceName = "jumpcloud-{app}-internal-api"

var InternalAPIDefaults = map[string]interface{}{}

type InternalAPI struct {
	host string
	*jcconfig.API
	*Common
}

func NewInternalAPI() (cfg *InternalAPI, err error) {
	source := jcconfig.NewSource(InternalAPIDefaults)
	cfg = new(InternalAPI)
	cfg.API, err = jcconfig.NewAPI(source, internalAPIServiceName, newBuildInfo())
	if err != nil {
		return nil, fmt.Errorf("failed to load internal API service configuration: %w", err)
	}
	cfg.Common, err = newCommon(source)
	if err != nil {
		return nil, fmt.Errorf("failed to load common internal-api configuration: %w", err)
	}
	cfg.host = strings.Trim(source.GetString(jcconfig.KeyInterface), "[]")
	return cfg, nil
}

func (cfg *InternalAPI) Host() string { return cfg.host }
```

## tools.go

Place at repo root. Required for `bin/lint go` and `bin/configure` to work. 

```go
//go:build tools
// +build tools

package tools

import (
	_ "github.com/onsi/ginkgo/v2/ginkgo"
	_ "github.com/pressly/goose/v3/cmd/goose"
	_ "github.com/polyfloyd/go-errorlint"
	_ "golang.org/x/lint/golint"
	_ "golang.org/x/tools/go/analysis/passes/shadow/cmd/shadow"
)
```
Do not Skip any of the above tools while using Origin CI.
After creating tools.go, run `go mod tidy`.
