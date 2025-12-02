import argparse
import sys
from app.model import load_model
from app.analysis.pipeline import analyze_url, analyze_email, analyze_qr_image
from app.ml.model_loader import get_model


# -------------------------
# Main CLI logic
# -------------------------
def main():
    parser = argparse.ArgumentParser(
        description="PhishSense CLI - Analyze text, URLs, emails, or QR codes"
    )

    parser.add_argument(
        "command",
        choices=["scan-text", "scan-url", "scan-email", "scan-qr"],
        help="Type of scan to perform",
    )

    parser.add_argument(
        "value",
        help="Text / URL / path to file (depending on command)",
    )

    parser.add_argument(
        "--model", default="model.pkl",
        help="Path to trained ML model (.pkl)"
    )

    parser.add_argument(
        "--vectorizer", default="vectorizer.pkl",
        help="Path to trained vectorizer (.pkl)"
    )

    args = parser.parse_args()

    # --- Load ML model ---
    load_model(args.model, args.vectorizer)

    # --- Handle each command ---
    try:
        if args.command == "scan-text":
            text = args.value.strip()
            result = analyze_email(text)  # treat text as email/message
            print(result)

        elif args.command == "scan-url":
            url = args.value.strip()
            result = analyze_url(url)
            print(result)

        elif args.command == "scan-email":
            with open(args.value, "r", encoding="utf-8") as f:
                content = f.read()
            result = analyze_email(content)
            print(result)

        elif args.command == "scan-qr":
            with open(args.value, "rb") as f:
                result = analyze_qr_image(f)
            print(result)

    except Exception as e:
        print("[!] Error during scanning:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
