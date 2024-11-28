from claude import ClaudeAssistant
from executer import execute_script
from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()

def main():
    version = 0

    try:
        assistant = ClaudeAssistant(api_key=os.getenv('ANTHROPIC_API_KEY')) 
        
        # Example of streaming response
        code_prompt = "Write a Python function that opens a white window"
        code_result = assistant.get_response_and_save(
            code_prompt,
            f"scheduler-v{version}.py",
            file_type='code'
        ) 
        
        assistant.save_response_to_file(content=str(code_result["response"]), filename=f"window-full-prompt-v{version}.txt")
        version = version + 1

        success, msg = execute_script(code_result["filepath"])

        if not success:
            # TODO: should try to fix it
            print(msg)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
