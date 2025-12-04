<!--
  This file is managed by the /sp.constitution command. Do not edit directly.
-->
# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.13+
**Primary Dependencies**: UV (Universal Python Package Manager); rich/typer (optional for CLI UX)
**Storage**: In-Memory (Global List or Dictionary)
**Testing**: pytest (if testing is requested)
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: Python Console Application (Single project)
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   **Language & Package Manager**: Verify adherence to Python 3.13+ and UV.
*   **User Interface**: Confirm CLI implementation and simple rich/typer usage.
*   **Storage**: Ensure only in-memory storage (Global List/Dictionary) is used, no file I/O or databases.
*   **Testing**: If testing is in scope, confirm `pytest` usage.
*   **Typing**: Verify strict type hinting throughout the codebase.
*   **Code Structure**: Validate modular architecture (Model vs. Service vs. UI).
*   **Coding Standards**: Confirm Google/NumPy style docstrings, graceful error handling, and PEP 8 formatting.
*   **Workflow Rules**: Ensure no code writing before plan approval, `sp.history` reading, and organized `/src` directory.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
├── models/
├── services/
├── cli/
└── lib/ # Optional: for shared utilities if needed

tests/
├── unit/
├── integration/
└── contract/ # Optional: if external contracts are introduced
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
