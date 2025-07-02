import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    args = sys.argv[1:]
    verbose = False

    if not args:
        print("A prompt need to be entered.")
        sys.exit(1)
    
    user_prompt = " ".join(args)

    if "--verbose" in user_prompt:
        verbose = True
        user_prompt = user_prompt.replace("--verbose", "")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print(response.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        


if __name__ == "__main__":
    main()
