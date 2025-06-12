# Style Guide for testlens Project

# Important
When chatting with the user, use Vietnamese language to explain to the user.

# Introduction
This document outlines the programming rules and code conventions for the testlens project. testlens is a modern testing framework developed to replace traditional BDD frameworks, using browser-use cloud API for browser automation.

# Key Principles
* **Readability:** Code must be easy to read and understand for all team members.
* **Maintainability:** Code must be easy to modify and extend when necessary.
* **Consistency:** Adherence to a consistent style improves team efficiency and reduces errors.
* **Performance:** Performance is also important, especially for testing frameworks.
* **Cloud-First:** Design always prioritizes using cloud APIs rather than local browsers.

# Coding Conventions

## Indentation and Formatting
* **Use 4 spaces for each level of indentation.**
* **Maximum 120 characters per line.**
* **Blank lines:** Use 2 blank lines between classes, 1 blank line between methods.

## Python Rules
* **Docstrings:** All modules, classes, and functions must have docstrings following the Google Python Style.
* **Type Hints:** Always use type hints for parameters and return types.
* **Imports:** Arrange in order: standard library, third-party packages, local imports.
* **Async/Await:** Use async/await consistently, don't mix with non-async methods.

## testlens Architecture
* **Browser Management:** Always use browser-use cloud API, don't use Playwright directly.
* **Configuration:** Use `.env` for configuration, don't hardcode API keys or sensitive information.
* **Tests:** Use the new TestRunner API (no longer using browsers and profiles parameters).
* **Error Handling:** Ensure detailed error handling and fallback mechanisms.

## Logging
* **Log Levels:** Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
* **Context:** Logs must have sufficient context for debugging when needed.
* **Structure:** Consistent log format: time, level, module, message.

## Documentation
* **README:** Update the README when API or usage changes occur.
* **Examples:** Each new feature must have examples in the examples/ directory.
* **CHANGELOG:** Update the CHANGELOG for each new version.

## Git Workflow
* **Commit Messages:** Prefix with change type: feat:, fix:, docs:, test:, refactor:
* **Branch Naming:** feature/{feature-name}, bugfix/{issue-number}
* **Pull Requests:** Fully describe changes, attach screenshots if related to UI
* **Code Reviews:** Each PR must be reviewed by at least 1 other team member
* **CI/CD:** All tests must pass on CI before merging

## Standard Libraries and Dependencies
* **Browser-use:** Use browser-use cloud API as the core for automation
* **Python-dotenv:** Manage environment variables and API keys
* **Conda:** Use Conda to manage development environments
* **pytest:** Main testing framework for the project

## Special Rules
* **Don't use Playwright directly:** All browser interactions must go through the browser-use cloud API
* **Always fallback gracefully:** Provide mock functionality when no API key is available
* **Always check version** when releasing a new version
* **Consistent API:** Don't use browsers and profiles parameters for run_tests() function
* **Secure API keys:** Never commit real API keys to the repository
