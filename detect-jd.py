import os
import csv
from dotenv import load_dotenv
from openai import OpenAI

# 1) Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set OPENAI_API_KEY in your .env")

# 2) Initialize client
client = OpenAI(api_key=API_KEY)

# 3) Prompt template (forces parseable format) 
PROMPT = """
Company: {name}
Website: {website}

Question: Is this company or website a job board?
Please reply in exactly this format:

Answer: <Yes or No>
Reason: <brief reason, max 100 characters>
"""

def parse_response(text):
    """
    Given the full response text, extract the 'Yes/No' and reason.
    """
    answer = None
    reason = ""
    for line in text.splitlines():
        if line.lower().startswith("answer:"):
            answer = line.split(":",1)[1].strip().capitalize()
        elif line.lower().startswith("reason:"):
            reason = line.split(":",1)[1].strip()
    # Fallbacks
    if answer not in ("Yes","No"):
        answer = "No"
    return answer, reason[:100]

def classify_company(name, website):
    # build prompt
    prompt = PROMPT.format(name=name, website=website)
    resp = client.responses.create(
        model="gpt-4o",
        input=prompt,
        tools=[{"type": "web_search"}]
    )
    # pick the first message with .content
    msg = next((o for o in resp.output if hasattr(o, "content")), None)
    if not msg:
        return "No", "No response from model"
    text = msg.content[0].text
    return parse_response(text)

def main():
    with open("input.csv", newline="", encoding="utf-8") as fin, \
         open("output.csv", "w", newline="", encoding="utf-8") as fout:

        reader = csv.DictReader(fin, fieldnames=["name","website"])
        writer = csv.writer(fout)
        # header
        writer.writerow(["name","website","is_job_board","reason"])

        for row in reader:
            name = row["name"].strip()
            website = row["website"].strip()
            yes_no, reason = classify_company(name, website)
            writer.writerow([name, website, yes_no, reason])
            print(f"✓ {name}: {yes_no} — {reason}")

if __name__ == "__main__":
    main()
