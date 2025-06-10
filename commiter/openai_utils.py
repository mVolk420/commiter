from openai import OpenAI

client = OpenAI()


def generate_commit_message(diff: str) -> str:
    prompt = (
        "Write a concise and clear git commit message summarizing the following diff:\n"
        f"{diff}\n"
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who writes concise git commit messages."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()
