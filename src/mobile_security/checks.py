from defusedxml import ElementTree as ET

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

def attr(element, name, default=None):
    return element.attrib.get(ANDROID_NS + name, default)

def analyze_manifest(xml_text: str) -> dict:
    root = ET.fromstring(xml_text)
    package = root.attrib.get("package", "unknown")
    app = root.find("application")
    findings = []
    if app is not None:
        debuggable = (attr(app, "debuggable", "false") or "false").lower() == "true"
        allow_backup = (attr(app, "allowBackup", "true") or "true").lower() == "true"
        cleartext = (attr(app, "usesCleartextTraffic", "false") or "false").lower() == "true"
        if debuggable:
            findings.append({"title":"Debuggable application flag enabled","severity":"high",
                "category":"Platform usage","evidence":'android:debuggable="true"',
                "remediation":"Disable debugging in release builds and verify build variants."})
        if allow_backup:
            findings.append({"title":"Application backup is enabled or unspecified","severity":"low",
                "category":"Data storage","evidence":f'android:allowBackup="{attr(app, "allowBackup", "unspecified")}"',
                "remediation":"Review backup rules and exclude sensitive data where appropriate."})
        if cleartext:
            findings.append({"title":"Cleartext traffic explicitly permitted","severity":"medium",
                "category":"Communication","evidence":'android:usesCleartextTraffic="true"',
                "remediation":"Prefer HTTPS and restrict cleartext exceptions to documented cases."})
        for tag in ("activity", "service", "receiver", "provider"):
            for node in app.findall(tag):
                exported = attr(node, "exported")
                name = attr(node, "name", "unnamed")
                has_filter = node.find("intent-filter") is not None
                if exported == "true" or (exported is None and has_filter):
                    findings.append({"title":f"Review exported {tag}: {name}","severity":"medium",
                        "category":"Platform usage",
                        "evidence":f"component={name}; exported={exported}; intent_filter={has_filter}",
                        "remediation":"Confirm external exposure is required, enforce permissions, and validate caller access."})
    return {
        "package": package,
        "application_present": app is not None,
        "findings": findings,
        "notes": [
            "Manifest checks are static indicators and may require target-SDK-aware interpretation.",
            "A clean manifest does not prove the app is secure.",
            "Inspect storage, cryptography, network behaviour, and backend APIs separately."
        ]
    }

def normalise_mobsf_json(data: dict) -> list[dict]:
    results = []
    for item in data.get("findings", []):
        results.append({
            "title": item.get("title") or item.get("issue") or "Untitled finding",
            "severity": (item.get("severity") or "info").lower(),
            "category": item.get("category") or "Imported MobSF finding",
            "evidence": item.get("description") or item.get("files") or "No evidence supplied",
            "remediation": item.get("recommendation") or "Review the source finding and validate manually."
        })
    return results

CHECKLIST = [
    ("Platform usage", "Review exported components, permissions, intent handling and release build flags."),
    ("Data storage", "Inspect preferences, databases, files, logs, backups and key material."),
    ("Communication", "Verify HTTPS, certificate validation and any certificate-pinning design."),
    ("Authentication", "Review login/session lifecycle, token expiry, logout and re-authentication."),
    ("Authorisation", "Test access controls on backend objects and functions using separate test accounts."),
    ("Cryptography", "Review algorithms, key generation, storage and use of platform crypto APIs."),
    ("Code quality", "Check debug code, hardcoded secrets, sensitive logs and unsafe dependencies."),
    ("Tampering / reverse engineering", "Review integrity assumptions and ensure server-side controls remain authoritative."),
]
