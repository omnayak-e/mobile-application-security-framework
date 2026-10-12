# Mobile Application Security Testing Framework

> **Portfolio project by Om Nayak** · M.Sc. Cyber Security · Amity University Rajasthan  
> **Focus:** Android configuration review, OWASP-aligned test planning, evidence management, and backend API security.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Android](https://img.shields.io/badge/Platform-Android-3DDC84?logo=android&logoColor=white)
![Testing](https://img.shields.io/badge/testing-pytest-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 1. Project overview

The Mobile Application Security Testing Framework is a small, modular Python project that supports a structured first-pass review of Android application security. It checks an extracted `AndroidManifest.xml` for selected configuration flags and exported components, offers a checklist for manual testing, and can normalise a simplified MobSF-style JSON findings file.

The framework is designed around a central principle: **static configuration checks are only one part of mobile application security**. Runtime behaviour, data storage, network communications, authentication, authorisation, cryptography, and backend APIs require separate validation.

This project does not decompile APKs, instrument apps, bypass certificate pinning, or attack production APIs. It is a reporting and review aid that complements authorised use of tools such as MobSF, Android Studio Emulator, Frida, Burp Suite, and Postman.

## 2. Problem statement

Mobile app security findings are often spread across static-analysis reports, runtime observations, API tests, and manual checklists. Without a consistent approach, teams can overlook important areas or struggle to communicate evidence and remediation.

This project demonstrates how to:
- check selected Android manifest settings;
- use a consistent finding format;
- keep checklist items in an explicit `not assessed` state until evidence exists;
- prepare a repeatable API test plan; and
- generate JSON and Markdown outputs for later review.

## 3. Objectives

### Technical objectives
- Parse Android manifest XML safely.
- Review debuggable, backup, and cleartext-traffic settings.
- Identify components that appear exported or have intent filters for manual review.
- Normalise a simplified JSON representation of MobSF findings.
- Generate an assessment checklist and report.

### Learning objectives
- Translate mobile security topics into concrete test cases.
- Understand the difference between static indicators and confirmed vulnerabilities.
- Consider the device, application, network, and backend as connected attack surfaces.
- Practise evidence-led reporting and remediation planning.

## 4. Scope and limitations

### Included
- Extracted Android manifest XML review.
- Selected application-level configuration checks.
- Exported component review candidates.
- Simplified MobSF JSON finding normalisation.
- A mobile security checklist and API test plan.
- JSON and Markdown report generation.

### Not included
- APK decompilation or automated reverse engineering.
- Runtime instrumentation or Frida script execution.
- Certificate-pinning bypass.
- Automatic API crawling, authentication attacks, or object enumeration.
- A claim of full OWASP MASVS compliance.
- Automatic severity validation or proof that a finding is exploitable.

A manifest flag is a review signal. For example, an exported component may be intended and safely permission-protected. Target SDK, Android version, app architecture, and runtime controls all affect interpretation.

## 5. Architecture

```text
Input
  +--> AndroidManifest.xml
  |        |
  |        v
  |   Safe XML parser + configuration rules
  |
  +--> Simplified MobSF JSON
  |        |
  |        v
  |   Finding normalisation
  |
  +--> Manual checklist
           |
           v
    Consistent assessment data
           |
           v
     JSON + Markdown reports
```

### Main modules

| Module | Responsibility |
|---|---|
| `checks.py` | Manifest rules, checklist, and MobSF finding normalisation |
| `reporting.py` | JSON and Markdown output |
| `cli.py` | CLI entry points |

## 6. Methodology

### Phase 1 — Define authorisation and build scope
Use an application you own or are explicitly authorised to assess. Record the package name, build variant, Android version, test account roles, backend environment, and approved testing activities.

### Phase 2 — Static manifest review
Obtain an extracted manifest from an approved APK or build pipeline. The parser reviews selected settings:
- `android:debuggable`;
- `android:allowBackup`;
- `android:usesCleartextTraffic`; and
- activities, services, receivers, and providers that may be externally accessible.

The tool creates findings with an evidence snippet and recommended review action. These are not automatically confirmed vulnerabilities.

### Phase 3 — Expand into a manual checklist
The checklist covers platform usage, data storage, communication, authentication, authorisation, cryptography, code quality, and tampering/reverse-engineering assumptions. Items are deliberately marked `not assessed`; an analyst should change status only after recording evidence.

### Phase 4 — Static/dynamic correlation
Use a dedicated test build and an emulator to observe runtime behaviour. Compare static indicators with what the app actually does. For example, a manifest setting may be overridden or constrained by other configuration, while runtime observations can reveal data flows not obvious from the manifest.

The Python framework does not perform this dynamic analysis itself; it organises the resulting review and reporting.

### Phase 5 — Backend API validation
Use approved test accounts and a test backend. Review authentication, object-level authorisation, token lifecycle, rate limiting, error disclosure, and data minimisation. Avoid destructive operations and redact tokens from evidence.

### Phase 6 — Report findings and remediation
Each finding should include:
- the affected package/component or API endpoint;
- the exact evidence and build/environment context;
- a risk rationale;
- business and user impact;
- a practical remediation recommendation; and
- retest criteria.

Do not describe the application as secure merely because the selected checks did not report a finding.

## 7. Technology stack

- **Python 3.10+** — CLI and rule logic.
- **defusedxml** — safer XML parsing.
- **pytest** — automated tests.
- **GitHub Actions** — CI.
- **MobSF, Android Studio Emulator, Frida, Burp Suite, Postman** — complementary tools for authorised manual or lab workflows; they are not all automatically invoked by this codebase.

## 8. Installation

```bash
git clone https://github.com/YOUR-USERNAME/mobile-application-security-framework.git
cd mobile-application-security-framework

python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
pip install -e .
```

## 9. Usage

### Review the included training manifest

```bash
mobile-security manifest examples/AndroidManifest.xml --out reports/generated/manifest-review
```

The sample intentionally includes configuration settings that trigger review findings. It is a training example, not a real application.

### Generate a checklist report

```bash
mobile-security checklist --out reports/generated/mobile-checklist
```

The report keeps each item as `not assessed` so the user does not accidentally imply that checks were performed.

### Run as a Python module

```bash
python -m mobile_security.cli manifest examples/AndroidManifest.xml
```

## 10. Understanding results

Each finding includes:
- `title` — the observation or review item;
- `severity` — a preliminary label for prioritisation;
- `category` — the security topic;
- `evidence` — the manifest setting or imported detail; and
- `remediation` — a suggested review or fix.

The report intentionally includes limitations and context. Do not treat severity labels as formal CVSS scores, and do not assume a missing finding proves the absence of a weakness.

## 11. Testing

```bash
pytest -q
```

The tests verify that selected manifest flags are detected and that simplified MobSF findings are normalised. The CI workflow runs the suite on pushes and pull requests.

## 12. Safe API test planning

The included [`docs/API_TEST_PLAN.md`](docs/API_TEST_PLAN.md) outlines non-destructive validation of authentication, object-level authorisation, token lifecycle, rate limiting, error disclosure, and response data minimisation.

Perform these checks only against a backend and test accounts approved for the assessment. Redact tokens and personal data before saving evidence.

## 13. Future improvements

- Add import support for additional MobSF report schemas with versioned fixtures.
- Add explicit finding status, owner, confidence, and retest fields.
- Add a checklist export to CSV or HTML.
- Add Android SDK / target SDK context to manifest checks.
- Add safe integration tests against a deliberately vulnerable local API.
- Add a dashboard after the report format is stable.

## 14. Author

**Om Nayak** · M.Sc. Cyber Security · Amity Institute of Information Technology, Amity University Rajasthan

This is a portfolio-oriented review helper, not a complete mobile penetration-testing product or a certification of app security.
