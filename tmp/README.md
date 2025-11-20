# Temporary Files Directory

This directory contains runtime artifacts generated during workflow execution.

## Files

- `agno_sessions.db` - SQLite database storing AgentOS workflow session state
  - Created automatically by the AgentOS runtime
  - Contains workflow execution history and session data
  - Used for audit trails and report generation
  - This file is gitignored (see `.gitignore`)

## Usage

This directory is automatically created when the AgentOS runtime executes workflows.
The database file persists session state between runs for debugging and reporting purposes.

## Cleanup

To reset session state, delete `agno_sessions.db`. It will be recreated on the next workflow execution.

