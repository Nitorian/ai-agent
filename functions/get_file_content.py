import os

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000

    try:
        path = os.path.join(working_directory, file_path)
        working_directory_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(path)

        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        if not abs_file_path.startswith(working_directory_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS]
                return f'{file_content_string} [...File "{file_path}" truncated at {MAX_CHARS} characters]'
            else:
                return file_content_string
        
    
    except (OSError, IOError) as e:
        return f"Error: {str(e)}"