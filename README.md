# BDD Testing Suite for [itsvrushabh.github.io](https://itsvrushabh.github.io)

Comprehensive Behavior-Driven Development (BDD) test automation project built using **Python**, **uv**, **Behave (Gherkin)**, and **Playwright**.

Designed to validate core functionalities, responsive navigation, theme persistence, interactive TUI terminal simulation, hero components, and SEO endpoint health on [itsvrushabh.github.io](https://itsvrushabh.github.io).

---

## 🏗️ Architecture & Design Pattern

This project implements the **Page Object Model (POM)** pattern alongside Gherkin BDD specifications:

```
testing_itsvrushabh.github.io/
├── features/
│   ├── environment.py              # Lifecycle hooks (before_all, scenario setup, screenshot on failure)
│   ├── navigation.feature          # Menubar workspaces & navigation routes
│   ├── theme_switcher.feature      # Omarchy theme toggling & localStorage persistence
│   ├── interactive_terminal.feature# Interactive TUI terminal emulator simulation
│   ├── hero_and_assets.feature     # Hero copy, snippet switcher, CTA buttons
│   ├── seo_and_performance.feature # HTTP 200 health checks & SEO meta tags
│   └── steps/
│       ├── common_steps.py         # Navigation, page loading, menubar actions
│       ├── terminal_steps.py       # TUI command execution & output assertions
│       ├── theme_steps.py          # Theme cycle & localStorage validation
│       ├── hero_steps.py           # Hero copy & snippet tabs
│       └── seo_steps.py            # Status code & Open Graph metadata validation
├── pages/                          # Page Object Model (POM) abstractions
│   ├── __init__.py
│   ├── base_page.py                # Reusable Playwright wrappers & actions
│   ├── home_page.py                # Homepage, menubar, theme, & hero selectors
│   └── terminal_page.py            # TUI terminal emulator selectors & actions
├── reports/                        # HTML test execution reports (auto-generated)
├── screenshots/                    # Failure capture screenshots (auto-saved on failure)
├── behave.ini                      # Behave runner configuration & defaults
├── pyproject.toml                  # UV project dependencies & build metadata
├── Makefile                        # Convenient shortcuts for running test suites
└── README.md
```

---

## 🎯 BDD Feature Coverage

| Feature File | Tags | Scenarios Covered |
| :--- | :--- | :--- |
| [`navigation.feature`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/features/navigation.feature) | `@ui`, `@navigation` | Homepage branding, 5 topbar numbered workspaces (Plugins & Code, Dispatches, Manual, Contact, Resume), GitHub external profile link with `target="_blank"`, terminal calendar toggle. |
| [`theme_switcher.feature`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/features/theme_switcher.feature) | `@ui`, `@theme` | Default theme validation (`tokyo-night`), cycling through color themes on `<html>[data-theme]`, and theme persistence in `localStorage("omarchy-site-theme")` across reloads. |
| [`interactive_terminal.feature`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/features/interactive_terminal.feature) | `@ui`, `@terminal` | Foot/Alacritty TUI simulation, window titlebar controls, quick command buttons (`fastfetch`, `about`, `skills`, `shortcuts`), keyboard typing & execution, clearing terminal. |
| [`hero_and_assets.feature`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/features/hero_and_assets.feature) | `@ui`, `@hero` | Header title & tagline validation, interactive installation snippet tabs (`cargo`, `curl`, `cli`), and CTA anchors. |
| [`keyboard_shortcuts.feature`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/features/keyboard_shortcuts.feature) | `@ui`, `@shortcuts` | Global hotkeys: `t` (theme cycle), `?` (toggle shortcuts modal cheatsheet), `Ctrl+K` (command palette), `Esc` (dismiss), and `` ` `` (jump to & focus TUI terminal prompt). |
| [`responsive_design.feature`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/features/responsive_design.feature) | `@ui`, `@responsive` | Responsive layout stability across Mobile (375x812), Tablet (768x1024), Desktop HD (1280x720), and Desktop Large (1440x900). |
| [`broken_links.feature`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/features/broken_links.feature) | `@api`, `@crawler` | Internal link crawler detecting broken 404/500 routes across all discovered internal navigation links and technical blog articles. |
| [`performance_assets.feature`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/features/performance_assets.feature) | `@api`, `@performance` | Critical hero 3D WebP assets and CSS stylesheet integrity, content-type headers, size budget compliance, and DOMContentLoaded load timing. |
| [`seo_and_performance.feature`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/features/seo_and_performance.feature) | `@api`, `@seo` | HTTP 200 GET requests for all core subpages (`/`, `/projects/`, `/blog/`, `/about/`, `/contact/`, `/resume/`), canonical links, author, and Open Graph metadata. |

---

## 🚀 Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) (fast Python package and project manager)
- System browser (Chromium, Google Chrome, or Playwright Chromium)

### 1. Install Dependencies

Using `uv`:

```bash
uv sync
```

Or install Playwright browser binaries if using a fresh machine without system Chromium:

```bash
uv run playwright install chromium
```

---

## 🧪 Running Tests

### Run All Tests

```bash
uv run behave
# or
make test
```

### Generate HTML Test Report

```bash
uv run behave -f behave_html_formatter:HTMLFormatter -o reports/report.html -f pretty
# or
make report
```
The report will be generated at `reports/report.html`.

### Run Specific Test Categories by Tag

```bash
# Run only UI tests
uv run behave --tags=@ui
# or: make test-ui

# Run interactive terminal tests
uv run behave --tags=@terminal
# or: make test-terminal

# Run theme switcher tests
uv run behave --tags=@theme
# or: make test-theme

# Run navigation tests
uv run behave --tags=@navigation
# or: make test-nav

# Run global keyboard shortcuts tests
uv run behave --tags=@shortcuts
# or: make test-shortcuts

# Run responsive design viewport tests
uv run behave --tags=@responsive
# or: make test-responsive

# Run broken links crawler tests
uv run behave --tags=@crawler
# or: make test-crawler

# Run critical assets & performance tests
uv run behave --tags=@performance
# or: make test-perf

# Run SEO & API endpoint health tests
uv run behave --tags=@seo
# or: make test-seo
```

### Run in Headed Mode (Watch Browser Live)

```bash
uv run behave -D headless=false
# or
make headed
```

### Run Against Custom Environment / URL

```bash
uv run behave -D base_url=https://itsvrushabh.github.io
```

---

## 📸 Failure Handling & Screenshots

The test runner is configured with an automated failure hook in [`features/environment.py`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/features/environment.py).

Whenever a scenario fails, a full-page screenshot is automatically captured and saved to `screenshots/FAIL_<scenario_name>.png` for immediate debugging.

---

## 🤖 GitHub Actions CI/CD & Automated Issue Reporting

Workflow file: [`.github/workflows/test.yml`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/.github/workflows/test.yml)

### Workflow Overview:
1. **Triggers:**
   - On `push` or `pull_request` to `master`/`main`
   - On a daily schedule cron (`0 6 * * *`) for automated health monitoring
   - Manually via `workflow_dispatch`
2. **Basic Tasks:**
   - Validates Python syntax for all modules (`py_compile`)
   - Validates Gherkin `.feature` files structure
3. **Execution & Reporting:**
   - Runs full BDD test suite with `uv run behave`
   - Automatically uploads HTML reports and screenshots as workflow run artifacts
4. **Automated Issue Creation on Failure:**
   - If any test fails, [`scripts/create_issue.py`](file:///home/cachyos/Work/testing_itsvrushabh.github.io/scripts/create_issue.py) automatically reports the issue directly to [**itsvrushabh/itsvrushabh.github.io/issues**](https://github.com/itsvrushabh/itsvrushabh.github.io/issues).
   - If an open test failure issue already exists, it appends a comment with the latest failure details instead of creating duplicate issues.
   - **Authentication:** Uses repository secret `GH_PAT` (Personal Access Token with `repo` or `issues:write` scope) for cross-repository issue creation, or defaults to `GITHUB_TOKEN`.

