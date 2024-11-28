import sys
import traceback
from typing import Optional, Tuple, Union
from pathlib import Path
import logging

def execute_script(script_path: Union[str, Path], args: Optional[list] = None) -> Tuple[bool, str]:
    """
    Execute a Python script with comprehensive error handling.
    
    Args:
        script_path: Path to the Python script to execute
        args: Optional list of arguments to pass to the script
        
    Returns:
        Tuple of (success_status: bool, message: str)
    """
    script_path = Path(script_path)
    if not script_path.exists():
        return False, f"Script not found: {script_path}"
    
    # Save original sys.argv
    original_argv = sys.argv.copy()
    
    try:
        # Prepare script arguments
        if args:
            sys.argv = [str(script_path)] + args
        else:
            sys.argv = [str(script_path)]
            
        logging.info(f"Executing script: {script_path}")
        
        # Read and execute the script
        with open(script_path, 'r') as file:
            script_contents = file.read()
            
        # Create a new namespace for the script
        namespace = {}
        exec(script_contents, namespace)
        
        return True, "Script executed successfully"
    except RuntimeError as e:
        return False, e 

