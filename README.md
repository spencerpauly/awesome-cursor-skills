# Awesome Cursor Skills [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of awesome [skills](https://docs.cursor.com/agent/skills) for [Cursor](https://cursor.com), the AI code editor.

Cursor Skills are reusable `SKILL.md` instruction files that teach the AI agent how to perform specific tasks — from setting up analytics to scaffolding entire projects. They live in `.cursor/skills/` (personal) or project directories and are automatically discovered by the agent.

## Contents

- [Skills](#skills)
- [Plugins](#plugins)
- [Cursor Resources](#cursor-resources)
- [Contributing](#contributing)

---

## Skills

Ready-to-use `SKILL.md` files you can copy into your `.cursor/skills/` directory. Each one teaches the agent a specific engineering workflow.

### Cursor-Native

Skills that harness Cursor's unique agent capabilities — things only an AI inside Cursor can do.

- [`switching-projects`](resources/switching-projects/SKILL.md) - Switch the active workspace to a different project using the `cursor-app-control` MCP, without opening a new window.
- [`visual-qa-testing`](resources/visual-qa-testing/SKILL.md) - Open the app in Cursor's built-in browser, take screenshots, check console errors, and audit network requests after making changes.
- [`verifying-in-browser`](resources/verifying-in-browser/SKILL.md) - Start the dev server, open the app side-by-side with your code, and verify rendering, console, and network health.
- [`profiling-performance`](resources/profiling-performance/SKILL.md) - Profile CPU performance of a running app using Cursor's browser profiler to capture call stacks and identify slow functions.
- [`screenshotting-changelog`](resources/screenshotting-changelog/SKILL.md) - Generate visual before/after PR descriptions by screenshotting UI changes across branches.
- [`best-of-n-solving`](resources/best-of-n-solving/SKILL.md) - Try multiple approaches to a hard problem in parallel using isolated git worktrees, then pick the best solution.
- [`parallel-exploring`](resources/parallel-exploring/SKILL.md) - Explore a large codebase fast by launching multiple read-only subagents that investigate different areas simultaneously.
- [`grinding-until-pass`](resources/grinding-until-pass/SKILL.md) - Keep iterating autonomously — fix, run, check, repeat — until tests pass, the build succeeds, or linting is clean.
- [`babysitting-pr`](resources/babysitting-pr/SKILL.md) - Monitor an open PR for CI failures, review comments, and merge conflicts — then fix them automatically to keep the PR merge-ready.

### Analytics & Tracking

- [`adding-analytics`](resources/adding-analytics/SKILL.md) - Add PostHog event tracking, page views, feature flags, and session replay to any web app.
- [`adding-feature-flags`](resources/adding-feature-flags/SKILL.md) - Add feature flags for gradual rollouts and A/B testing using PostHog or a simple local implementation.
- [PostHog LLM Analytics](https://github.com/PostHog/skills/tree/main/skills/posthog/llm-analytics) - Instrument LLM calls with token usage, latency, cost tracking, and model comparison.
- [PostHog Migrations](https://github.com/PostHog/skills/tree/main/skills/posthog/migrations) - Migrate from other analytics providers (Amplitude, Mixpanel, GA) to PostHog.

### Error Tracking & Monitoring

- [`adding-error-tracking`](resources/adding-error-tracking/SKILL.md) - Add Sentry crash reporting, performance monitoring, and source maps.

### Authentication & Payments

- [`adding-auth`](resources/adding-auth/SKILL.md) - Add OAuth login, session management, and protected routes with Auth.js (NextAuth).
- [`adding-stripe`](resources/adding-stripe/SKILL.md) - Integrate Stripe checkout, subscriptions, webhooks, and customer portal.

### Testing

- [`adding-e2e-tests`](resources/adding-e2e-tests/SKILL.md) - Set up Playwright with config, example tests, page objects, and CI integration.
- [`writing-tests`](resources/writing-tests/SKILL.md) - Analyze existing code and write comprehensive unit and integration tests with proper mocking, edge cases, and assertions.
- [`python-tdd-with-uv`](resources/python-tdd-with-uv/SKILL.md) - Test-driven development in Python using uv — red-green-refactor cycle with vertical slicing and fast dependency management.
- [Matt Pocock TDD](https://github.com/mattpocock/skills/tree/main/tdd) - Vertical-slice TDD for AI agents — one test, one implementation, repeat. Prevents over-engineering and speculative tests.
- [Anthropic Webapp Testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) - Automated browser testing for web apps with screenshot verification and interaction flows.

### Infrastructure & DevOps

- [`adding-docker`](resources/adding-docker/SKILL.md) - Dockerize any app with a multi-stage Dockerfile, docker-compose, and .dockerignore.
- [`setting-up-ci`](resources/setting-up-ci/SKILL.md) - Set up a GitHub Actions CI/CD pipeline with linting, testing, type-checking, and deployment.
- [`setting-up-terraform`](resources/setting-up-terraform/SKILL.md) - Infrastructure-as-code with provider config, modules, remote state, and CI integration.
- [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) - Terraform and OpenTofu skill — testing, modules, CI/CD, and production patterns.

### Code Quality & Security

- [`reviewing-code`](resources/reviewing-code/SKILL.md) - Thorough code review focused on correctness, maintainability, performance, and best practices.
- [`auditing-security`](resources/auditing-security/SKILL.md) - Systematic security audit checking for OWASP Top 10 vulnerabilities, secrets exposure, and insecure patterns.
- [`auditing-performance`](resources/auditing-performance/SKILL.md) - Audit bundle size, rendering, database queries, and Core Web Vitals.
- [Sentry Code Simplifier](https://github.com/getsentry/skills/tree/main/plugins/sentry-skills/skills/code-simplifier) - Refactor for clarity, consistency, and maintainability — eliminates dead code, fixes naming, and reduces complexity.
- [Sentry Find Bugs](https://github.com/getsentry/skills/tree/main/plugins/sentry-skills/skills/find-bugs) - Scan local branch changes for bugs, security vulnerabilities, and code quality issues.
- [Sentry Code Review](https://github.com/getsentry/skills/tree/main/plugins/sentry-skills/skills/code-review) - Code review following Sentry's engineering practices.
- [Sentry Security Review](https://github.com/getsentry/skills/tree/main/plugins/sentry-skills/skills/security-review) - Security code review for injection, XSS, auth bypass, and IDOR vulnerabilities.
- [Sentry Django Perf Review](https://github.com/getsentry/skills/tree/main/plugins/sentry-skills/skills/django-perf-review) - Django-specific performance review — N+1 queries, select_related, caching, and serialization.
- [Sentry Skill Scanner](https://github.com/getsentry/skills/tree/main/plugins/sentry-skills/skills/skill-scanner) - Scan agent skills for security issues — prompt injection, exfiltration, and unsafe tool use.
- [`verifying-markdown-formatting`](resources/verifying-markdown-formatting/SKILL.md) - Verify headings, lists, links, code blocks, spacing, and style consistency in Markdown files.
- [`fixing-broken-links`](resources/fixing-broken-links/SKILL.md) - Crawl all URLs in a file, test each for HTTP 200, and fix or replace any broken links.

### Dependencies

- [`updating-npm-package`](resources/updating-npm-package/SKILL.md) - Safely update an npm package: check npmjs.com for the latest version, read release notes, auto-apply minor updates, and for major updates find the migration guide and produce a detailed validation report.

### Frontend & UI

- [`using-ui-stack`](resources/using-ui-stack/SKILL.md) - Enforce a design system (8px grid, color tokens, typography, dark mode, 5-state interactions) on every AI-generated component.
- [`converting-css-to-tailwind`](resources/converting-css-to-tailwind/SKILL.md) - Convert plain CSS stylesheets to Tailwind utility classes — selectors, media queries, pseudo-classes, animations, and arbitrary values.
- [`converting-css-modules-to-tailwind`](resources/converting-css-modules-to-tailwind/SKILL.md) - Migrate CSS Modules to Tailwind — handles `styles.xxx` removal, `composes`, conditional classNames, SCSS features, and cleanup.
- [Anthropic Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) - Generate polished, production-ready frontend UI with consistent styling and responsive layouts.
- [shadcn/ui Skill](https://ui.shadcn.com/docs/skills) - Managing shadcn components — adding, searching, debugging, styling, and composing UI.
- [Vercel React Best Practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices) - 40+ rules for React/Next.js performance including eliminating request waterfalls and bundle optimization.
- [Vercel Web Design Guidelines](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) - UI code auditing for accessibility, UX, and performance compliance.
- [Vercel React View Transitions](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-view-transitions) - Implement the View Transitions API in React/Next.js for smooth page and component animations.
- [Vercel Composition Patterns](https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns) - Component composition, code splitting, and server/client boundary patterns for Next.js.

### Planning & Architecture

- [Matt Pocock PRD to Issues](https://github.com/mattpocock/skills/tree/main/prd-to-issues) - Convert a product requirements doc into a set of well-scoped GitHub issues.
- [Matt Pocock Improve Architecture](https://github.com/mattpocock/skills/tree/main/improve-codebase-architecture) - Analyze a codebase and propose concrete architecture improvements.
- [Matt Pocock Grill Me](https://github.com/mattpocock/skills/tree/main/grill-me) - Challenge assumptions and push back on ideas before committing to an approach.
- [Anthropic MCP Builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) - Build Model Context Protocol servers from scratch with tool definitions and transport setup.

### Documentation

- [`adding-api-docs`](resources/adding-api-docs/SKILL.md) - Generate OpenAPI/Swagger documentation with interactive docs UI.
- [Anthropic Doc Coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) - Structured workflow for co-authoring technical documentation with an AI agent.

### Utilities

- [`exporting-to-png`](resources/exporting-to-png/SKILL.md) - Export code snippets, diagrams, terminal output, or UI components to PNG images via headless browser or CLI tools.

## Plugins

Official Cursor marketplace plugins with bundled skills. Install via **Cursor Settings > Plugins**.

- [Figma](https://cursor.com/cn/marketplace/figma) - (`generate-design`, `code-connect-components` + 5 more) Design-to-code and design system management.
- [Linear](https://cursor.com/cn/marketplace/linear) - Issues, projects, documents, and sprints via MCP.
- [Slack](https://cursor.com/cn/marketplace/slack) - Channel search, messaging, and Slack actions via MCP.
- [Datadog](https://cursor.com/cn/marketplace/datadog) - (`datadog-mcp-setup`) Query logs, metrics, traces, and dashboards.
- [Stripe](https://cursor.com/cn/marketplace/stripe) - (`stripe-best-practices`, `upgrade-stripe`) Payment integration and SDK migration.
- [Firebase](https://cursor.com/cn/marketplace/firebase) - (`firebase-ai-logic`, `firebase-auth-basics` + 9 more) Backend, auth, and AI infrastructure.
- [Shopify](https://cursor.com/cn/marketplace/shopify) - (`shopify-admin`, `shopify-custom-data` + 14 more) GraphQL, Liquid, and extensions.
- [dbt Labs](https://cursor.com/cn/marketplace/dbt-labs) - (`adding-dbt-unit-test`, `building-dbt-semantic-layer` + 7 more) Data modeling and analytics engineering.
- [Sentry](https://cursor.com/cn/marketplace/sentry) - (`sentry-code-review`, `sentry-browser-sdk` + 26 more) Error tracking and SDK integration.
- [Vercel](https://cursor.com/cn/marketplace/vercel) - (`ai-architect`, `deployment-expert`, `performance-optimizer` + 25 more) Deploy and optimize web apps.
- [Svelte](https://cursor.com/cn/marketplace/svelte) - (`svelte-file-editor`, `svelte-code-writer` + 2 more) Svelte 5 development and validation.
- [Elastic](https://cursor.com/cn/marketplace/elastic) - (`cloud-create-project`, `cloud-manage-project` + 31 more) Elasticsearch and Observability.
- [Postman](https://cursor.com/cn/marketplace/postman) - (`api-readiness-analyzer`, `postman-routing` + 11 more) API lifecycle management.
- [Sanity](https://cursor.com/cn/marketplace/sanity) - (`content-modeling-best-practices`, `seo-aeo-best-practices` + 6 more) CMS and content workflows.
- [Langfuse](https://cursor.com/cn/marketplace/langfuse) - (`langfuse`) LLM tracing, prompt management, and evaluation.
- [CockroachDB](https://cursor.com/cn/marketplace/cockroachdb) - (`cockroachdb-sql-patterns`, `cockroachdb-app-patterns` + 2 more) Distributed DB management.
- [Encore](https://cursor.com/cn/marketplace/encore) - (`add-infrastructure`, `create-service` + 20 more) TypeScript/Go backends with auto infrastructure.
- [AWS Amplify](https://cursor.com/cn/marketplace/aws-amplify) - (`amplify-workflow`) Full-stack apps with auth, data, and storage.
- [AWS Serverless](https://cursor.com/cn/marketplace/aws-serverless) - (`aws-lambda`, `api-gateway` + 2 more) Serverless application lifecycle.
- [Pendo](https://cursor.com/cn/marketplace/pendo) - (`account-health`, `feature-adoption` + 2 more) Product analytics and session replays.
- [GitLab](https://cursor.com/cn/marketplace/gitlab) - (`gitlab-ci-author`, `backlog-health` + 7 more) Issues, MRs, and CI/CD pipelines.
- [Sourcegraph](https://cursor.com/cn/marketplace/sourcegraph) - (`searching-sourcegraph`, `sourcegraph-deepsearch`) Code search across repos.
- [Miro](https://cursor.com/cn/marketplace/miro) - (`miro-mcp`, `diagram` + 4 more) Board context, diagrams, and code generation.
- [Cloudinary](https://cursor.com/cn/marketplace/cloudinary) - (`cloudinary-docs`, `cloudinary-transformations`) Media management and optimization.
- [Appwrite](https://cursor.com/cn/marketplace/appwrite) - (`appwrite-cli`, `appwrite-web` + 8 more) BaaS with database, auth, and storage.
- [ClickUp](https://cursor.com/cn/marketplace/clickup) - Task management, time tracking, and collaboration via MCP.
- [Box](https://cursor.com/cn/marketplace/box) - (`box`) Content management, AI Q&A, and extraction.
- [Chargebee](https://cursor.com/cn/marketplace/chargebee) - (`chargebee-integration`) Billing operations and webhook handling.
- [Circle](https://cursor.com/cn/marketplace/circle) - (`bridge-stablecoin`, `use-circle-wallets` + 7 more) Stablecoin payments and smart contracts.
- [Runlayer](https://cursor.com/cn/marketplace/runlayer) - (`mcp-builder`, `mcp-security-audit`, `plugin-builder`) MCP security and governance.
- [Superpowers](https://cursor.com/cn/marketplace/superpowers) - (`code-reviewer`, `brainstorming` + 13 more) TDD, debugging, and collaboration.
- [Omni](https://cursor.com/cn/marketplace/omni) - (`omni-content-builder`, `omni-ai-optimizer` + 9 more) Analytics and dashboard creation.
- [Braintrust](https://cursor.com/cn/marketplace/braintrust) - AI evaluation, experiments, and evaluation logs via MCP.
- [Parallel](https://cursor.com/cn/marketplace/parallel) - (`parallel-web-search`, `parallel-deep-research` + 2 more) Web search and data enrichment.
- [Tavily](https://cursor.com/cn/marketplace/tavily) - (`tavily-cli`, `tavily-extract` + 4 more) Web search, crawling, and deep research.
- [Astronomer](https://cursor.com/cn/marketplace/astronomer) - (`airflow`, `airflow-plugins` + 19 more) Data engineering and Airflow integration.
- [Meta Reality Labs](https://cursor.com/cn/marketplace/meta-reality-labs) - (`hz-immersive-designer`, `hz-new-project-creation` + 11 more) Quest and Horizon OS development.
- [Plain](https://cursor.com/cn/marketplace/plain) - Support threads, customer management, and help center articles.
- [Turbopuffer](https://cursor.com/cn/marketplace/turbopuffer) - Vector and full-text search database integration.

## Cursor Resources

### Cursor Rules

Cursor Rules (`.cursorrules` / `.cursor/rules/`) are complementary to skills — rules are always-on conventions, skills are on-demand workflows.

- [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) - The most comprehensive collection of `.cursorrules` files, categorized by framework and language.
- [sanjeed5/awesome-cursor-rules-mdc](https://github.com/sanjeed5/awesome-cursor-rules-mdc) - Curated `.mdc` format rules with a generator tool.
- [tugkanboz/awesome-cursorrules](https://github.com/tugkanboz/awesome-cursorrules) - Showcases modern Cursor Rules system with MDC format.

### Learning

- [Cursor Skills Documentation](https://docs.cursor.com/agent/skills) - Official docs on creating and using skills.
- [Cursor Marketplace](https://cursor.com/marketplace) - Browse and install official plugins with bundled skills.
- [Agent Skills Specification](https://agentskills.io) - The open standard for defining agent capabilities.
- [Deep Dive SKILL.md](https://abvijaykumar.medium.com/deep-dive-skill-md-part-1-2-09fc9a536996) - In-depth walkthrough of the SKILL.md format.

### Directories

- [cursor-skills GitHub Topic](https://github.com/topics/cursor-skills) - Browse community repos tagged with cursor-skills.
- [skills.sh](https://skills.sh/) - Leaderboard and directory for popular skill repositories.
- [AgentDepot.dev](https://agentdepot.dev/) - Open-source explorer for agents, skills, and rules.
- [CursorDirectory](https://cursor.directory/) - Community directory for Cursor rules and configurations.

### Tools

- [npx skills](https://github.com/vercel-labs/skills) - CLI to search, install, and manage skills.
- [PostHog/context-mill](https://github.com/PostHog/context-mill) - Assemble context for AI agents into Agent Skills-compliant packages.
- [Anthropic Skill Creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) - Official skill for drafting, testing, and optimizing custom SKILL.md files.

---

## Contributing

Contributions welcome! Please read the [contribution guidelines](CONTRIBUTING.md) first.

If you know of a great Cursor skill that isn't listed here, please open a PR. Include:
- A link to the skill or repository
- A brief description of what it does
- Which category it belongs to
