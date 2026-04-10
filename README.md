# Awesome Cursor Skills [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of awesome [skills](https://docs.cursor.com/agent/skills) for [Cursor](https://cursor.com), the AI code editor.

Cursor Skills are reusable `SKILL.md` instruction files that teach the AI agent how to perform specific tasks — from setting up analytics to scaffolding entire projects. They live in `.cursor/skills/` (personal) or project directories and are automatically discovered by the agent.

## Contents

- [Featured](#featured)
- [Skills](#skills)
- [Plugins](#plugins)
- [Community Skills](#community-skills)
- [Cursor Rules (Related)](#cursor-rules-related)
- [Resources](#resources)
- [Contributing](#contributing)

---

## Featured

Standout skills and collections that are especially useful across many projects.

- [PostHog Skills](https://github.com/PostHog/skills) - Official PostHog skills for adding analytics, feature flags, and event tracking to any project.
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) - Official Vercel skills including React best practices, web design guidelines, and deploy workflows.
- [Anthropic Skills](https://github.com/anthropics/skills) - Official Anthropic skills including skill-creator, frontend-design, webapp-testing, and MCP builder.
- [Sentry Skills](https://github.com/getsentry/skills) - Official Sentry skills for security review, code review, and development workflows.

## Skills

Ready-to-use `SKILL.md` files you can copy into your `.cursor/skills/` directory. Each one teaches the agent a specific engineering workflow.

### Analytics & Tracking

- [Add Analytics (PostHog)](resources/add-analytics/SKILL.md) - Add event tracking, page views, feature flags, and session replay to any web app.
- [Add Feature Flags](resources/add-feature-flags/SKILL.md) - Add feature flags for gradual rollouts and A/B testing using PostHog or a simple local implementation.

### Error Tracking & Monitoring

- [Add Error Tracking (Sentry)](resources/add-error-tracking/SKILL.md) - Add crash reporting, performance monitoring, and source maps.

### Authentication & Payments

- [Add Authentication (Auth.js)](resources/add-auth/SKILL.md) - Add OAuth login, session management, and protected routes with NextAuth.js.
- [Add Stripe Payments](resources/add-stripe/SKILL.md) - Integrate Stripe checkout, subscriptions, webhooks, and customer portal.

### Testing

- [Add E2E Tests (Playwright)](resources/add-e2e-tests/SKILL.md) - Set up Playwright with config, example tests, page objects, and CI integration.

### Infrastructure & DevOps

- [Add Docker](resources/add-docker/SKILL.md) - Dockerize any app with a multi-stage Dockerfile, docker-compose, and .dockerignore.
- [Setup CI (GitHub Actions)](resources/setup-ci/SKILL.md) - Set up a CI/CD pipeline with linting, testing, type-checking, and deployment.
- [Setup Terraform](resources/setup-terraform/SKILL.md) - Infrastructure-as-code with provider config, modules, remote state, and CI integration.

### Code Quality & Security

- [Code Review](resources/code-review/SKILL.md) - Thorough code review focused on correctness, maintainability, performance, and best practices.
- [Security Audit](resources/security-audit/SKILL.md) - Systematic security audit checking for OWASP Top 10 vulnerabilities, secrets exposure, and insecure patterns.
- [Performance Audit](resources/performance-audit/SKILL.md) - Audit bundle size, rendering, database queries, and Core Web Vitals.

### Documentation

- [Add API Docs (OpenAPI)](resources/add-api-docs/SKILL.md) - Generate OpenAPI/Swagger documentation with interactive docs UI.

## Plugins

Official Cursor marketplace plugins with bundled skills. Install via **Cursor Settings > Plugins**.

- [Figma](https://cursor.com/cn/marketplace/figma) - (Generate Design from Code, Code Connect Components, Generate Design System Library + 4 more) Skills for translating Figma designs into production code and managing design systems.
- [Linear](https://cursor.com/cn/marketplace/linear) - Skills for managing issues, projects, documents, and sprints via MCP.
- [Slack](https://cursor.com/cn/marketplace/slack) - Skills for searching channels, sending messages, and performing Slack actions via MCP.
- [Datadog](https://cursor.com/cn/marketplace/datadog) - (Datadog MCP Setup) Skills for querying logs, metrics, traces, and dashboards through natural conversation.
- [Stripe](https://cursor.com/cn/marketplace/stripe) - (Stripe Best Practices, Upgrade Stripe API/SDK) Skills for payment integration patterns and SDK migration guidance.
- [Firebase](https://cursor.com/cn/marketplace/firebase) - (Firebase AI Logic, Firebase Auth Basics, App Hosting Basics + 8 more) Skills for building apps with Firebase backend and AI infrastructure.
- [Shopify](https://cursor.com/cn/marketplace/shopify) - (Admin GraphQL API, Admin Execution, Custom Data Metafields + 13 more) Skills for Shopify development across GraphQL, Liquid, and extensions.
- [dbt Labs](https://cursor.com/cn/marketplace/dbt-labs) - (Adding Unit Tests, Answering Natural Language Questions, Building Semantic Layer + 6 more) Skills for data modeling, analytics engineering, and dbt Cloud workflows.
- [Sentry](https://cursor.com/cn/marketplace/sentry) - (Code Review, Browser SDK Setup, Cloudflare SDK Setup + 25 more) Skills for error tracking, performance monitoring, and SDK integration across platforms.
- [Vercel](https://cursor.com/cn/marketplace/vercel) - (AI Architect, Deployment Expert, Performance Optimizer + 25 more) Skills for building, deploying, and optimizing web apps and AI agents.
- [Svelte](https://cursor.com/cn/marketplace/svelte) - (Svelte File Editor, Svelte Code Writer, Core Best Practices + 1 more) Skills for Svelte 5 development with documentation lookup and code validation.
- [Elastic](https://cursor.com/cn/marketplace/elastic) - (Cloud Create Project, Cloud Manage Project, Cloud Access Management + 30 more) Skills for Elasticsearch, Kibana, Observability, and ES|QL workflows.
- [Postman](https://cursor.com/cn/marketplace/postman) - (API Readiness Analyzer, Client Code Generation, Mock Server Creation + 10 more) Skills for full API lifecycle management and security auditing.
- [Sanity](https://cursor.com/cn/marketplace/sanity) - (Content Experimentation & A/B Testing, Content Modeling Best Practices, SEO & AEO Best Practices + 5 more) Skills for CMS integration, schema design, and content workflows.
- [Langfuse](https://cursor.com/cn/marketplace/langfuse) - (Langfuse CLI & Docs) Skills for LLM tracing, prompt management, and evaluation.
- [CockroachDB](https://cursor.com/cn/marketplace/cockroachdb) - (SQL Patterns, App Patterns, Operator Patterns + 1 more) Skills for schema exploration, query optimization, and distributed DB management.
- [Encore](https://cursor.com/cn/marketplace/encore) - (Add Infrastructure, Create Service, Code Review + 19 more) Skills for building backend services in TypeScript/Go with automatic infrastructure.
- [AWS Amplify](https://cursor.com/cn/marketplace/aws-amplify) - (Amplify Workflow) Skills for building full-stack apps with authentication, data models, and storage.
- [AWS Serverless](https://cursor.com/cn/marketplace/aws-serverless) - (AWS Lambda, API Gateway, Lambda Durable Functions + 1 more) Skills for designing, building, and deploying serverless applications.
- [Pendo](https://cursor.com/cn/marketplace/pendo) - (Account Health, Feature Adoption, Feedback Analysis + 1 more) Skills for product analytics, session replays, and customer insights.
- [GitLab](https://cursor.com/cn/marketplace/gitlab) - (CI/CD Author, Backlog Health, Pipeline Status + 6 more) Skills for managing issues, merge requests, and CI/CD pipelines.
- [Sourcegraph](https://cursor.com/cn/marketplace/sourcegraph) - (Searching Sourcegraph, Deep Search) Skills for code search and navigation across repositories.
- [Miro](https://cursor.com/cn/marketplace/miro) - (Miro MCP, Create Diagram, Summarize Board + 3 more) Skills for reading board context, creating diagrams, and generating code from whiteboards.
- [Cloudinary](https://cursor.com/cn/marketplace/cloudinary) - (Cloudinary Docs, Cloudinary Transformations) Skills for media asset management, transformations, and optimization.
- [Appwrite](https://cursor.com/cn/marketplace/appwrite) - (Appwrite CLI, Appwrite Web SDK, Appwrite Dart SDK + 7 more) Skills for backend-as-a-service with database, auth, and storage across platforms.
- [ClickUp](https://cursor.com/cn/marketplace/clickup) - Skills for task management, time tracking, and collaboration via MCP.
- [Box](https://cursor.com/cn/marketplace/box) - (Box MCP Workflows) Skills for content management, AI Q&A, summarization, and extraction.
- [Chargebee](https://cursor.com/cn/marketplace/chargebee) - (Chargebee Integration) Skills for billing operations, API integration, and webhook handling.
- [Circle](https://cursor.com/cn/marketplace/circle) - (Bridge Stablecoin CCTP, Circle Wallets, Gateway + 6 more) Skills for stablecoin payments, cross-chain transfers, and smart contracts.
- [Runlayer](https://cursor.com/cn/marketplace/runlayer) - (MCP Builder, MCP Security Audit, Plugin Builder) Skills for security policies, secret protection, and audit trails for MCPs.
- [Superpowers](https://cursor.com/cn/marketplace/superpowers) - (Code Reviewer, Brainstorming, Dispatching Parallel Agents + 12 more) Skills for TDD, debugging, and collaboration patterns.
- [Omni](https://cursor.com/cn/marketplace/omni) - (Content Builder, AI Optimizer, Content Explorer + 8 more) Skills for analytics exploration, querying, model building, and dashboard creation.
- [Braintrust](https://cursor.com/cn/marketplace/braintrust) - Skills for AI evaluation, experiments, and evaluation logs via MCP.
- [Parallel](https://cursor.com/cn/marketplace/parallel) - (Web Search, Deep Research, Data Enrichment + 1 more) Skills for web search, content extraction, and deep research.
- [Tavily](https://cursor.com/cn/marketplace/tavily) - (Web Search CLI, Extract Content, Crawl Sites + 3 more) Skills for web search, crawling, deep research, and URL discovery.
- [Astronomer](https://cursor.com/cn/marketplace/astronomer) - (Airflow DAG Management, Airflow Plugins, Analyzing Data + 18 more) Skills for data engineering, warehouse exploration, and Airflow integration.
- [Meta Reality Labs](https://cursor.com/cn/marketplace/meta-reality-labs) - (Immersive Designer, New Project Creation, WebXR IWSDK + 10 more) Skills for Meta Quest and Horizon OS development.
- [Plain](https://cursor.com/cn/marketplace/plain) - Skills for support threads, customer management, and help center articles.
- [Turbopuffer](https://cursor.com/cn/marketplace/turbopuffer) - Skills for vector and full-text search database integration.

## Community Skills

Open-source skill repositories from the community and official dev teams.

### Analytics & Monitoring

- [PostHog/skills](https://github.com/PostHog/skills) - Official PostHog skills for analytics, feature flags, session replay, and LLM analytics.
- [PostHog/ai-plugin](https://github.com/PostHog/ai-plugin) - PostHog AI plugin for Cursor and other coding agents.

### Infrastructure & Deployment

- [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) - Claude Agent Skill for Terraform and OpenTofu — testing, modules, CI/CD, and production patterns.

### Frontend & UI

- [shadcn/ui Skill](https://github.com/hzm0321/real-time-fund/blob/main/.cursor/skills/shadcn/SKILL.md) - Managing shadcn components — adding, searching, debugging, styling, and composing UI.
- [Vercel React Best Practices](https://github.com/vercel-labs/agent-skills) - 40+ rules for React/Next.js performance, including eliminating request waterfalls and bundle optimization.
- [Vercel Web Design Guidelines](https://github.com/vercel-labs/agent-skills) - UI code auditing for accessibility, UX, and performance compliance.

### Code Quality

- [Anthropic Simplify](https://github.com/anthropics/skills) - Reviews code for reuse, efficiency, and quality, fixing dead code and naming issues.
- [Sentry Code Review](https://github.com/getsentry/skills) - Code review following Sentry's engineering practices.
- [Sentry Security Review](https://github.com/getsentry/skills) - Systematic security code review for injection, XSS, and authentication vulnerabilities.

## Cursor Rules (Related)

Cursor Rules (`.cursorrules` / `.cursor/rules/`) are complementary to skills — rules are always-on conventions, skills are on-demand workflows.

- [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) - The most comprehensive collection of `.cursorrules` files, categorized by framework and language.
- [sanjeed5/awesome-cursor-rules-mdc](https://github.com/sanjeed5/awesome-cursor-rules-mdc) - Curated `.mdc` format rules with a generator tool.
- [tugkanboz/awesome-cursorrules](https://github.com/tugkanboz/awesome-cursorrules) - Showcases modern Cursor Rules system with MDC format.

## Resources

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
- [Anthropic Skill Creator](https://github.com/anthropics/skills) - Official skill for drafting, testing, and optimizing custom SKILL.md files.

---

## Contributing

Contributions welcome! Please read the [contribution guidelines](CONTRIBUTING.md) first.

If you know of a great Cursor skill that isn't listed here, please open a PR. Include:
- A link to the skill or repository
- A brief description of what it does
- Which category it belongs to
