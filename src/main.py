from claude import ClaudeAssistant
from executer import execute_script
from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()

def main():
    version = 0
    error = None
    code_result = None
    filename = "test"

    try:
        assistant = ClaudeAssistant(api_key=os.getenv('ANTHROPIC_API_KEY')) 
        
        # Example of streaming response
        code_prompt = "Write code in Python "
        code_result = assistant.get_response_and_save(
            code_prompt,
            f"{filename}-v{version}.py",
            file_type='code'
        ) 
        
        assistant.save_response_to_file(content=str(code_result["response"]), filename=f"{filename}-prompt-v{version}.txt")


        while version < 5:
            success, msg = execute_script(code_result["filepath"])

            if success: 
                break

            version = version + 1

            code_prompt = msg 
            code_result = assistant.get_response_and_save(
                code_prompt,
                f"{filename}-v{version}.py",
                file_type='code'
            ) 
            
            assistant.save_response_to_file(content=str(code_result["response"]), filename=f"{filename}-prompt-v{version}.txt")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
