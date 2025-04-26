import os
import argparse
import openai

def generate_copy(event, date):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenRouter API Key!")

    prompt = f"""You are a nonprofit marketing expert.
Generate a 5-email drip sequence plus 4 social media captions for an event called '{event}' happening on {date}.
Emails should build excitement and encourage donations.
Captions should be short, energetic, and suitable for Instagram and Facebook."""

    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    response = client.chat.completions.create(
        model="meta-llama/llama-3-70b-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Generate Nyla fundraiser copy")
    parser.add_argument("--event", required=True, help="Name of the event")
    parser.add_argument("--date", required=True, help="Date of the event")

    args = parser.parse_args()

    try:
        copy = generate_copy(args.event, args.date)
        print("\n🎯 Generated Copy:\n")
        print(copy)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

