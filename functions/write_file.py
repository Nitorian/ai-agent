import os

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