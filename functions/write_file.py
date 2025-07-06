import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is to be written to the specified file path",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        path = os.path.join(working_directory, file_path)
        working_directory_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(path)

        if not abs_file_path.startswith(working_directory_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(os.path.dirname(abs_file_path)):
            os.makedirs(os.path.dirname(abs_file_path))
        
        with open(abs_file_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    
    except (OSError, IOError) as e:
        return f"Error: {str(e)}"