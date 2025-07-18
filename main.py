import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


def main():
    load_dotenv()

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    def call_function(function_call_part,verbose=False):
        function_name = function_call_part.name
        
        if verbose:
            print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(f" - Calling function: {function_call_part.name}")

        function_call_part.args["working_directory"] = "./calculator"
        args = function_call_part.args

        func_dict = {"get_files_info": get_files_info,
                     "get_file_content": get_file_content,
                     "run_python_file": run_python_file,
                     "write_file": write_file,
        }

        

        if function_name in func_dict:
            function_result = func_dict[function_name](**args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result}
                    )
                ]
            )
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"}
                    )
                ]
            )

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

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    
    for i in range(0, 20):

        
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt
            )
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        function_call = response.function_calls
        
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        if function_call:
            result = call_function(function_call[0], verbose)
            messages.append(result)
            if verbose == True:
                print(f"-> {result.parts[0].function_response.response}")
        else:
            print(response.text)
            break
    
        


if __name__ == "__main__":
    main()
