#!/usr/bin/env python3
import argparse
import json
from typing import Any, Dict, List

from app.analysis.pipeline import analyze_url, analyze_email
from app.storage.json_storage import append_scan, get_recent_scans

# command: scan-url
def cmd_scan_url(args: argparse.Namespace) -> int:
    url = args.url
    log = bool(args.log)

    result = analyze_url(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if log:
        append_scan(result)

    return 0

# command: scan-email
def cmd_scan_email(args: argparse.Namespace) -> int:
    subject = args.subject or ""
    body = args.body or ""
    sender = args.sender or ""
    log = bool(args.log)

    result = analyze_email(subject, body, sender)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if log:
        append_scan(result)

    return 0

# command: history
def cmd_history(args: argparse.Namespace) -> int:
    limit = args.limit
    items: List[Dict[str, Any]] = get_recent_scans(limit=limit)

    print(f"Last {len(items)} scans:")
    for i, rec in enumerate(items, start=1):
        t = rec.get("timestamp", "?")
        rtype = rec.get("type", "?")
        verdict = rec.get("verdict", "?")
        inp = rec.get("input", "")
        if isinstance(inp, dict):
            short_input = inp.get("subject", "") or str(inp)
        else:
            short_input = str(inp)
        print(f"{i:3d}. [{t}] [{rtype}] [{verdict}] {short_input}")

    return 0

# build argument parser
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PhishSense CLI - scan URLs and emails for phishing indicators"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # scan-url
    url_cmd = subparsers.add_parser(
        "scan-url",
        help="Scan a single URL",
    )
    url_cmd.add_argument(
        "url",
        help="URL to scan (e.g. http://example.com/login)",
    )
    url_cmd.add_argument(
        "--log",
        action="store_true",
        help="Append this scan to data/scans.jsonl",
    )
    url_cmd.set_defaults(func=cmd_scan_url)

    # scan-email
    email_cmd = subparsers.add_parser(
        "scan-email",
        help="Scan an email (subject + body + sender)",
    )
    email_cmd.add_argument(
        "--subject",
        default="",
        help="Email subject",
    )
    email_cmd.add_argument(
        "--body",
        default="",
        help="Email body text",
    )
    email_cmd.add_argument(
        "--sender",
        default="",
        help="Email sender address (e.g. support@bank.com)",
    )
    email_cmd.add_argument(
        "--log",
        action="store_true",
        help="Append this scan to data/scans.jsonl",
    )
    email_cmd.set_defaults(func=cmd_scan_email)

    # history
    hist_cmd = subparsers.add_parser(
        "history",
        help="Show recent scans from data/scans.jsonl",
    )
    hist_cmd.add_argument(
        "--limit",
        type=int,
        default=20,
        help="How many recent scans to show (default: 20)",
    )
    hist_cmd.set_defaults(func=cmd_history)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 1

    return func(args)


if __name__ == "__main__":
    raise SystemExit(main())
