import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    # Load API key from .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Set OPENAI_API_KEY in .env")

    client = OpenAI(api_key=api_key)

    print("🖥️  OpenAI Responses CLI (type 'exit' to quit)")
    previous_id = None

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ("exit", "quit"):
            break

        # Build the request payload
        params = {
            "model": "gpt-4o",                   # or "gpt-4o-mini"
            "input": user_input,
            "tools": [{"type": "web_search"}],  # enable live web search
        }
        if previous_id:
            params["previous_response_id"] = previous_id

        # Send the request
        response = client.responses.create(**params)
        
        message_obj = next(
            (item for item in response.output if hasattr(item, "content")),
            None
        )

        if not message_obj:
            print("⚠️  No generated message found in response.output.")
        else:
            ai_text = message_obj.content[0].text
            print(f"\nAI: {ai_text}")

        # Save for follow-up context
        previous_id = response.id

if __name__ == "__main__":
    main()
