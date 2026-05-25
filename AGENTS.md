# NightmareNet Agent Configuration

## Instructions

Read and follow `CLAUDE.md` in this repository for project-specific conventions.

## Skills

The following skills are available and SHOULD be used when relevant:

### Superpowers (via ~/.agents/skills/superpowers/)

- **test-driven-development** — Use when writing any new feature or fixing bugs
- **systematic-debugging** — Use when investigating test failures or runtime errors
- **verification-before-completion** — Use before claiming ANY task is done
- **writing-plans** — Use when the task requires 3+ steps of implementation
- **executing-plans** — Use when executing a previously written plan

### Project Skills (via .claude/skills/)

- **ui-ux-pro-max** (`.claude/skills/ui-ux-pro-max/`) — Use for any frontend/UI work on the Next.js frontend
- **elite-execution-philosophy** (`.claude/skills/elite-execution-philosophy/`) — Core execution philosophy; applies to ALL tasks. Sets staff-engineer quality bar.
- **workflow-orchestration** (`.claude/skills/workflow-orchestration/`) — Plan-mode-first execution, task management via `tasks/todo.md`, self-improvement loop via `tasks/lessons.md`
- **verification-and-elegance** (`.claude/skills/verification-and-elegance/`) — Never mark work complete without proof. Demands elegant solutions over hacky/brittle code.
- **subagent-strategy** (`.claude/skills/subagent-strategy/`) — Aggressive subagent delegation for research, debugging, architecture, security, and verification.
- **research-first-execution** (`.claude/skills/research-first-execution/`) — Research competitors, benchmark patterns, analyze architecture before implementation.
- **ai-native-product-thinking** (`.claude/skills/ai-native-product-thinking/`) — AI-native product design, modern UX expectations, Linear/Vercel/Stripe-tier polish.
- **performance-security-devops** (`.claude/skills/performance-security-devops/`) — Performance engineering, security, RBAC, CI/CD, observability, deployment automation.

## Commands

Available slash commands in `.claude/commands/`:

- `/check` — Run full quality pipeline (lint + tests + frontend build)
- `/tdd <feature>` — Implement a feature with strict TDD
- `/commit` — Create a conventional commit with pre-flight checks
- `/debug <problem>` — Systematic debugging workflow
- `/prime` — Load project context for a new session

## Hooks

Configured in `.claude/settings.json`:

- **PostToolUse**: Python syntax check on `.py` file edits
- **Stop**: Ruff lint check before session ends

## Learned User Preferences

- Research-first execution: deep competitive landscape, market sizing, academic lit, GTM, personas, and architecture patterns before implementing; leverage Browser Use API for live web research/automation where applicable.
- Use subagents aggressively for parallel research, exploration, debugging, security review, and verification; one focused responsibility per subagent.
- Linear/Vercel/Stripe-tier UI polish; feature-dense, information-heavy panels inspired by Linear/Vercel/DarkLead, Arc, Notion, Raycast — not minimal or sparse.
- Plan-mode-first for any non-trivial task (3+ steps or architectural decisions); generate full PRD/TRD/architecture/UX flows/API contracts/sprint plans as part of planning, not just task lists; re-plan if anything goes sideways.
- Track work via `tasks/todo.md` (checkable items) and corrections via `tasks/lessons.md` (self-improvement loop, append after every user correction).
- Verification before completion: tests, lint, type-check, UX validation, architecture integrity — never claim done without staff-engineer-level proof.
- Demand elegance: pause and ask "Is there a more elegant solution?" before non-trivial implementations; reject hacky, repetitive, brittle, or tightly-coupled code.
- Autonomous bug fixing: investigate, trace root cause, fix, validate — no hand-holding required.
- AI-native thinking: every feature considers AI copilots, semantic search, intelligent automation, conversational workflows; integrate Azure OpenAI, OpenAI APIs, Anthropic Claude, RAG pipelines, and vector databases as needed.
- Performance-first: sub-100ms UI, sub-500ms API, CUDA acceleration, mixed precision, quantization for ML; code splitting and lazy loading on the frontend.
- Security + DevOps: RBAC, secrets in vaults, rate limiting, audit logs, least-privilege, compliance readiness; CI/CD via GitHub Actions, Docker, Vercel/Railway, PostgreSQL/Redis, observability, rollback strategies, cost optimization.
- Spec-driven + repository intelligence: GitHub Spec Kit structured specs/ADRs/validation pipelines; use GitNexus for impact analysis before editing any symbol, and complement with `graphify` and `code-review-graph` for architecture and PR-review intelligence.

## Learned Workspace Facts

- Next.js client uses same-origin `/api`; `frontend/next.config.ts` rewrites to `NEXT_API_REWRITE_URL` (backend base, no trailing slash). If `NEXT_PUBLIC_API_URL` is set, the browser calls that origin directly and rewrites are not used (configure API CORS for split-host).
- Health (`/api/v1/health`): `NIGHTMARENET_HEALTH_TEST_COUNT` optionally runs a subprocess `pytest --collect-only` check; leave unset/off in production.
- Pipeline runner registry: `NIGHTMARENET_MAX_PIPELINE_RUNNERS` caps in-memory runners (default 64); when over cap, completed runs are evicted first.
- `docs/solutions/nightmarenet-research-synthesis.md` is the research synthesis artifact; full deep-research workflows expect **parallel-cli** (or equivalent) available.
- Strategic execution plan lives at `.cursor/plans/nightmarenet_strategic_research_synthesis_9589248a.plan.md`; when executing it, do not edit the plan file itself.
- Dev GPU: RTX 3050 Ti (4 GB VRAM). DistilBERT/DistilGPT-2 fit without issues; GPT-2 (124M) needs gradient checkpointing + FP16, batch size 4-8 max.
- `C:\Users\aditj\New Projects\TR-104-DarkLead-main` is the design inspiration reference for feature-dense 20+ panel dashboards.
- Strategic direction: hybrid open-source core (Apache 2.0) + hosted platform (paid). OSS = distortion engines, training loop, CLI. Paid = orchestration, compliance, multi-GPU, team features.
- Pricing model: Community $0 (full OSS, single-GPU, self-hosted) / Pro $49/seat/mo + compute (cloud orchestration, multi-GPU, teams, ~1000 cycles/mo) / Enterprise $50K-$100K/yr (SSO, audit, compliance, on-prem, SLA, custom engines).
- Cyberpunk-neural design system: Void Black (#020617) backgrounds, Indigo Dream (#818CF8), Red Nightmare (#EF4444), Cyan Neural (#06B6D4), Amber Compress (#F59E0B); Inter (UI) + JetBrains Mono (code/metrics); Framer Motion spring-based 60fps motion.
- Academic positioning: closest prior art is PAD (Deperrois 2022, eLife) for sleep-inspired training; NightmareNet differentiates by targeting adversarial robustness (not representation learning) with integrated compression phase.
- Target market timing: EU AI Act Article 15 (robustness mandate) fully applicable August 2, 2026.
- Continual-learning state lives at the cross-workspace canonical index `C:\Users\aditj\New Projects\AtomicPulse\.cursor\hooks\state\continual-learning-index.json` (reused by NightmareNet rather than maintaining a per-repo index).

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **NightmareNet** (2280 symbols, 4080 relationships, 78 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/NightmareNet/context` | Codebase overview, check index freshness |
| `gitnexus://repo/NightmareNet/clusters` | All functional areas |
| `gitnexus://repo/NightmareNet/processes` | All execution flows |
| `gitnexus://repo/NightmareNet/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
