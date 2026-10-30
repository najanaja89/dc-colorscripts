# Repository Guidelines

## Project Structure & Module Organization

This repository is currently an initial scaffold: no source code, tests, assets, or build configuration have been committed. Establish a clear layout as implementation begins, and update this guide when directories are introduced.

Keep executable scripts, supporting assets, and tests in separate, clearly named directories. Document each directory’s purpose in a root `README.md`. Treat `.agents/`, `.codex/`, and `.aws/` as environment configuration; avoid changing them as part of ordinary feature work.

## Build, Test, and Development Commands

No build, test, or local execution commands are configured yet. Do not assume a particular language, package manager, or build system.

When adding tooling, document exact setup and execution commands in `README.md`, including required dependencies. Prefer a small set of reproducible commands that contributors can run from the repository root.

Useful review commands:

- `git status --short`: inspect pending changes.
- `git diff --check`: detect whitespace errors in tracked changes.
- `git diff`: review the patch before committing.

## Coding Style & Naming Conventions

Follow the conventions of the language selected for implementation. Use consistent indentation within each file, descriptive names, and small, focused modules. Prefer lowercase, hyphen-separated filenames for documentation and standalone scripts where language conventions permit.

No formatter or linter is configured. If one is introduced, commit its configuration and document its invocation.

## Testing Guidelines

No testing framework or coverage threshold exists yet. Add automated checks alongside new behavior, covering expected results and meaningful failure cases. Give tests descriptive names and document how to run them. For visual output, include a reproducible preview command and representative screenshots when useful.

## Commit & Pull Request Guidelines

There is no commit history establishing a message convention. Use concise, imperative subjects, such as `Add initial script runner`, and keep commits focused.

Pull requests should explain the purpose, summarize changes, list validation performed, and link related issues when available. Explicitly identify checks that could not be run and why.
