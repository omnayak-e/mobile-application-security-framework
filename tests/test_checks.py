from pathlib import Path
from mobile_security.checks import analyze_manifest, normalise_mobsf_json

def test_manifest_flags_detected():
    xml = Path("examples/AndroidManifest.xml").read_text()
    result = analyze_manifest(xml)
    titles = [f["title"] for f in result["findings"]]
    assert any("Debuggable" in t for t in titles)
    assert any("Cleartext" in t for t in titles)

def test_mobsf_normalisation():
    findings = normalise_mobsf_json({"findings":[{"issue":"Sample","severity":"high","recommendation":"Fix it"}]})
    assert findings[0]["title"] == "Sample"
    assert findings[0]["remediation"] == "Fix it"
