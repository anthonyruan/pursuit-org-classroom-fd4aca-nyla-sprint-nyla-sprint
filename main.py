import argparse
import os
import sys
import time
import requests
import json

# === Settings ===
MODEL = "meta-llama/llama-4-maverick:free"
ENDPOINT = "https://openrouter.ai/v1/chat/completions"

# === Functions ===
def build_prompt(args):
    return f"Write five fundraising emails and four social captions for the {args.event} on {args.date} in a {args.tone} tone."

def chat_completion(prompt):
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        sys.exit("❌ Missing OPENROUTER_API_KEY environment variable.")

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    try:
        t0 = time.time()
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=60)
        dt = time.time() - t0
        print(f"✅ Request completed in {dt:.2f}s", file=sys.stderr)
    except requests.exceptions.RequestException as e:
        sys.exit(f"❌ Request failed: {e}")

    if response.status_code != 200:
        print(f"❌ HTTP {response.status_code} Error: {response.text}")
        sys.exit(1)

    try:
        return response.json()["choices"][0]["message"]["content"]
    except (KeyError, json.JSONDecodeError) as e:
        sys.exit(f"❌ Failed to parse response: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate fundraising emails and social captions.")
    parser.add_argument("--event", default="Community Gala", help="Name of the event")
    parser.add_argument("--date", default="TBD", help="Date of the event")
    parser.add_argument("--tone", default="upbeat", help="Tone of the writing")
    parser.add_argument("--dry-run", action="store_true", help="Only print the prompt without sending request")
    args = parser.parse_args()

    prompt = build_prompt(args)

    if args.dry_run:
        print(prompt)
        return

    output = chat_completion(prompt)

    os.makedirs("out", exist_ok=True)
    with open("out/campaign.md", "w") as f:
        f.write(output)

    print("✅ Content generated and saved to out/campaign.md")

if __name__ == "__main__":
    main()
