import argparse, json
from pathlib import Path
from .checks import analyze_manifest, CHECKLIST
from .reporting import save_report

def main():
    parser = argparse.ArgumentParser(description="Mobile application security review helper")
    sub = parser.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("manifest"); m.add_argument("xml"); m.add_argument("--out", default="reports/generated/manifest")
    c = sub.add_parser("checklist"); c.add_argument("--out", default="reports/generated/checklist")
    args = parser.parse_args()
    if args.cmd == "manifest":
        data = analyze_manifest(Path(args.xml).read_text(encoding="utf-8"))
        prefix = args.out
    else:
        data = {"checklist":[{"area":a,"checks":b,"status":"not assessed"} for a,b in CHECKLIST],
                "notes":["Complete checklist items using authorised test accounts and lab builds.",
                         "Checklist status is intentionally not pre-filled with pass/fail claims."]}
        prefix = args.out
    jp, mp = save_report(data, prefix)
    print(json.dumps(data, indent=2))
    print(f"Reports written: {jp} and {mp}")

if __name__ == "__main__":
    main()
