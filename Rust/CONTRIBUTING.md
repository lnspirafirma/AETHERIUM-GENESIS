Name Last commit message Last commit date
📁 .cargo config: update alias for conesis-atr 2 hours ago
📁 conesis-common refactor: migrate types to atr schema 4 hours ago
📁 conesis-core core: init genesis protocol yesterday
📁 conesis-protocol api: sync with firma v2.2 spec yesterday
📁 conesis-tui ui: apply inspira styling guidelines 5 hours ago
📄 Cargo.toml workspace: rename codex-rs to conesis-atr yesterday
📄 Justfile scripts: update test targets yesterday
📄 README.md docs: update architecture diagrams 2 days ago
📄 CONTRIBUTING.md rules: update env vars and prefixes today

Development Guidelines for conesis-atr
Crate Naming & Structure
Crate names are now prefixed with conesis-.
Example: The core folder's crate is named conesis-core.
Workspace root: conesis-atr.
Coding Standards
Format Macros: When using format! and variables can be inlined into {}, always do so.
Integer Types: Do not use unsigned integers even if the number cannot be negative (use i32/i64 unless interfacing with specific hardware/API requirements).
Tests: Prefer comparing the equality of entire objects over fields one by one.
Clippy:
Collapse if statements (collapsible_if).
Inline format args (uninlined_format_args).
Use method references over closures (redundant_closure_for_method_calls).
Sandbox Environment Variables
Network: You operate in a sandbox where CONESIS_SANDBOX_NETWORK_DISABLED=1 is set.
Do not modify code related to CONESIS_SANDBOX_NETWORK_DISABLED_ENV_VAR.
Seatbelt: When spawning processes via Seatbelt (/usr/bin/sandbox-exec), CONESIS_SANDBOX=seatbelt is set on the child process.
Workflow & Tooling
Prerequisites: Ensure just, rg, and cargo-insta are installed.
Formatting: Run just fmt automatically after changes.
Linting: Before finalizing, run just fix -p <project> (e.g., just fix -p conesis-tui).
Testing:
Run project-specific tests first: cargo test -p conesis-tui
If common, core, or protocol changed: cargo test --all-features
TUI Convention (conesis-tui)
Styling (Ratatui)
Use Stylize trait helpers: "text".cyan().bold() instead of manual Style.
Constructors:
Basic: "text".into()
Lines: vec!["A".into(), "B".red()].into()
Wrapping: Use textwrap::wrap for strings. Use conesis-tui/src/wrapping.rs helpers for Ratatui Lines.
Snapshot Tests:
Check pending: cargo insta pending-snapshots -p conesis-tui
Accept: cargo insta accept -p conesis-tui
Integration Tests (Core)
Use conesis_core_test_support::responses.
Mocking: Use mount_sse_once and hold the ResponseMock to assert outbound requests.
Assertions: Inspect ResponsesRequest using helpers like function_call_output, json_body.
จำลองสถานะ: เชื่อมต่อ Directory สำเร็จ - โครงสร้างถูกปรับปรุงเป็น conesis-atr แล้ว