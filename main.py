import argparse, os, sys, time, requests, json
MODEL="meta-llama/llama-4-maverick:free"
ENDPOINT="https://openrouter.ai/v1/chat/completions"
def build_prompt(args):
    return f"Write five fundraising emails and four social captions for the {args.event} on {args.date} in a {args.tone} tone."
def chat_completion(prompt):
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        sys.exit("❌ Missing OPENROUTER_API_KEY environment variable.")

    payload = {
        "model": MODEL,
        "router_query": { "forced_model": MODEL },  # 新加这一行强制指定模型
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    print(f"🚀 Sending payload:\n{json.dumps(payload, indent=2)}")  # 打印发送内容

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
    p=argparse.ArgumentParser()
    p.add_argument("--event",default="Community Gala"); p.add_argument("--date",default="TBD"); p.add_argument("--tone",default="upbeat"); p.add_argument("--dry-run",action="store_true")
    a=p.parse_args()
    prompt=build_prompt(a)
    if a.dry_run:
        print(prompt); return
    out=chat_completion(prompt)
    os.makedirs("out",exist_ok=True)
    with open("out/campaign.md","w") as f: f.write(out)
    print(out)
if __name__=="__main__":
    main()
