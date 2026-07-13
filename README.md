# Codex Model Routing Team

[中文说明](README.zh-CN.md)

Route complex Codex work to background workers with explicit models and reasoning effort, while keeping one lead agent in control.

## Why this exists

Codex's native MultiAgentV2 surface does not expose per-worker model or reasoning controls. Native subagents therefore inherit the session model, which can make parallel work unexpectedly expensive.

This skill uses Codex App background tasks instead. The lead agent plans, assigns file ownership, integrates results, runs verification, and decides what to keep. Background workers can use different available models and reasoning levels for the work they are best suited to handle.

## What it does

- Routes only complex, genuinely parallel work such as multi-source research, multi-section content, large Skills or decks, and independent engineering workstreams.
- Assigns explicit models and reasoning effort to background workers, with Sol and Luna as the default routes and Ultra disabled.
- Limits fan-out to three new workers per wave, six concurrent workers, and eight workers per root task.
- Verifies that each task materialized before continuing, prevents workers from spawning descendants, and archives only completed tasks whose results were adopted.
- Keeps publishing, payments, deletion, account changes, and production mutations in the lead task.

## Requirements

- Codex App with background task tools for project discovery, task creation, task reading, follow-up messages, and archiving.
- Access to the models and reasoning levels selected by the lead agent.
- A healthy Codex tool environment. The skill stops delegation when background task creation cannot be verified.

## Install

```bash
npx skills add zjp1997720/codex-model-routing-team -g -a codex --skill codex-model-routing-team -y
```

## Use

Ask Codex directly:

```text
Use $codex-model-routing-team to research these six independent topics in parallel, then verify and synthesize the findings.
```

```text
Use $codex-model-routing-team to implement, test, and review three independent modules without overlapping file ownership.
```

```text
Use $codex-model-routing-team to prepare a training deck with separate research, writing, and review workers.
```

The skill can also activate implicitly when the user's Codex instructions contain standing authorization for background model routing.

## Routing behavior

1. The lead agent decides whether parallelism will beat coordination cost.
2. The first real worker acts as a health probe and must be readable before more tasks are created.
3. Later workers are created in bounded waves with explicit model, reasoning, scope, ownership, and acceptance criteria.
4. The lead agent verifies facts and outputs, handles conflicts, and integrates the final deliverable.
5. Adopted idle or completed tasks are archived one at a time.

The full policy lives in [SKILL.md](SKILL.md). Supporting rules are in [references](references/).

## Repository layout

```text
.
├── SKILL.md
├── agents/
│   ├── interface.yaml
│   └── openai.yaml
└── references/
    ├── durable-mode.md
    ├── routing-policy.md
    ├── task-packet.md
    ├── thread-lifecycle.md
    └── validation-cases.md
```

## Validation

The workflow has been tested locally with both projectless research workers and project-bound workspace workers, including model/reasoning verification, result collection, and serial archival.

## License

[MIT](LICENSE)
