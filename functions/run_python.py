import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        path = os.path.join(working_directory, file_path)
        working_directory_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(path)
        rel_path_for_uv = os.path.relpath(abs_file_path, working_directory_path)
        commands = ["uv", "run", rel_path_for_uv]

        if not abs_file_path.startswith(working_directory_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        
        try:
            result = subprocess.run(
                commands, 
                timeout=30, 
                capture_output=True, 
                cwd=working_directory_path,
                text=True
                )
            output_lines = []

            if result.stdout:
                output_lines.append(f"STDOUT:\n{result.stdout.strip()}")

            if result.stderr:
                output_lines.append(f"STDERR:\n{result.stderr.strip()}")

            if result.returncode:
                output_lines.append(f"Process exited with code {result.returncode}")
            
            if not output_lines:
                return "No output produced."
            
            return "\n".join(output_lines)
        
        except Exception as e:
            return f"Error: executinc Python file: {e}"
        
    
    except (OSError, IOError) as e:
        return f"Error: {str(e)}"