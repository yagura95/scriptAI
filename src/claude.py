import anthropic
import os
from typing import Optional, Dict
from pathlib import Path
import mimetypes
import base64

class ClaudeAssistant:
    def __init__(self, 
                 api_key: Optional[str] = None,
                 model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')

        if not self.api_key:
            raise ValueError("API key must be provided or set in ANTHROPIC_API_KEY environment variable")
        
        self.client = anthropic.Client(api_key=self.api_key)
        self.model = model
        self.output_dir = Path("outputs")
    
    def stream_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """Stream a response from Claude."""
        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            yield e

    def get_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """Get a complete response from Claude."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        except Exception as e:
            return e

    def process_code_output(self, response: str, filename: str) -> str:
        """
        Process and save code output from Claude.
        Returns the path to the saved file.
        """
        # Extract code between triple backticks if present
        if "```" in response:
            code_blocks = []
            lines = response.split('\n')
            in_code_block = False
            current_block = []
            
            for line in lines:
                if line.startswith('```'):
                    if in_code_block:
                        code_blocks.append('\n'.join(current_block))
                        current_block = []
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    current_block.append(line)
            
            if code_blocks:
                code = '\n\n'.join(code_blocks)
            else:
                code = response
        else:
            code = response
        
        return self.save_response_to_file(code, filename)

    def save_response_to_file(self, content: str, filename: str, mode: str = 'w') -> str:
        """
        Save Claude's response to a file.
        
        Args:
            content: Content to save
            filename: Name of the file
            mode: File opening mode ('w' for text, 'wb' for binary)
            
        Returns:
            Path to saved file
        """
        filepath = self.output_dir / filename
        with open(filepath, mode) as f:
            f.write(content)
        return str(filepath)

    def get_response_and_save(self, 
                            prompt: str,
                            output_filename: str,
                            file_type: str = 'text',
                            max_tokens: int = 1000) -> Dict:
        """
        Get response from Claude and save to appropriate file format.
        
        Args:
            prompt: Input prompt
            output_filename: Name for the output file
            file_type: Type of file ('text', 'code', 'json')
            max_tokens: Maximum tokens in response
            
        Returns:
            Dict containing response info and file path
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            filepath = "" 
            
            if file_type == 'code':
                filepath = self.process_code_output(content, output_filename)
            
            return {
                'response': response,
                'status': 'success',
                'filepath': filepath,
                'content': content
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def read_file_content(self, file_path: str) -> str:
        """
        Read file content and return it as text
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def get_response_with_file(self, 
                             prompt: str, 
                             file_path: str,
                             output_filename: str,
                             file_type: str = "text",
                             max_tokens: int = 1000) -> str:
        """
        Send a prompt along with file contents to Claude and get a response
        """
        try:
            # Read the file content
            file_content = self.read_file_content(file_path)
            
            # Combine prompt with file content
            combined_prompt = f"{prompt}\n\nHere's the file content:\n\n{file_content}"
            
            # Create the message
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": combined_prompt
                        }
                    ]
                }]
            )
            
            content = response.content[0].text

            filepath = ""

            if file_type == 'code':
                filepath = self.process_code_output(content, output_filename)
            
            return {
                'response': response,
                'status': 'success',
                'filepath': filepath,
                'content': content
            }
            
        except Exception as e:
            return f"Error processing request: {str(e)}"

