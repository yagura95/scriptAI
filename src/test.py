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
    file_path = Path("outputs/test.py")

    try:
        success, msg = execute_script(file_path)
    except Exception as e:
        print(e)
        try:
            assistant = ClaudeAssistant(api_key=os.getenv('ANTHROPIC_API_KEY')) 

            version = version + 1

            prompt = str(e)

            code_result = assistant.get_response_with_file(prompt, file_path, filename, file_type='code')

            print(code_result)
            
            assistant.save_response_to_file(content=str(code_result), filename=f"{filename}-prompt-v{version}.txt")
        except RuntimeError as e:
            print(e)

if __name__ == "__main__":
    main()
