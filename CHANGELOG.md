# Changelog

All notable changes to this project will be documented in this file.

## [v0.9.0] - 2026-05-25
### Added
- **Swarm Intelligence & A2A Mentions**:
  - Direct `@AgentName` mentions between all agents (not only routed through GeneralAG).
  - Background task dispatches when an agent addresses another agent, allowing chained agent-to-agent discussions.
  - Expiring rate-limit loops (15 seconds) to prevent infinite agent communication ping-pong.
- **Swarm Coordination**:
  - Parallel worker dispatching when a job is assigned.
  - Multi-agent coordination that monitors worker active jobs and automatically triggers GeneralAG to compile and synthesize final artifacts using `[WRITE: ...]` block actions.
- **Frontend Dashboard Visualization**:
  - Pulsing Swarm Status Banner in the dashboard showing the active team-workflows.
  - Real-time display of which agents are currently talking to each other.

### Changed
- Refactored `agent_repo.py`, `chat_commands_handlers.py`, and `chat_helpers.py` to support parallel task tracking, job clearing (`@free`), and prefixed commands.
- Optimized all backend files in `src/gnom_hub/` to remain strictly under the 40-line limit per file.

## [v0.8.0] - 2026-05-25
### Added
- Full system integration (Phases 1-7: Preset isolation, double-pass Gatekeeper validation, database sandbox checks, browser automation, and SoulAG memory retrieval).
- Automated test scripts for end-to-end flow validation.

## [v0.7.0] - 2026-05-25
### Added
- Multi-agent collaboration with job assignments.
- Real-time work status indicator on the frontend.
