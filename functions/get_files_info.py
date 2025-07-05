import os

def get_files_info(working_directory, directory=None):
    try:
        path = os.path.join(working_directory, directory)
        working_directory_path = os.path.abspath(working_directory)
        directory_path = os.path.abspath(path)
        file_info = []

        if not os.path.isdir(directory_path):
            return f'Error: "{directory}" is not a directory'

        if not directory_path.startswith(working_directory_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            item_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            file_info.append(f"- {item}: file_size={item_size} bytes, is_dir={is_dir}")

        return "\n".join(file_info)
    
    except (OSError, IOError) as e:
        return f"Error: {str(e)}"
