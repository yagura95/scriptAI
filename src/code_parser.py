class CodeParser:
    def extract_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """
        Extract code blocks from markdown-style text where each block 
        starts with ```language and ends with ```
        """
        # Pattern matches everything between ```language and ```
        pattern = r'```(\w*)\n(.*?)```'
        blocks = []
        
        # Find all matches in the text
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for match in matches:
            language = match.group(1).lower() or 'text'  # If no language specified, use 'text'
            code = match.group(2).strip()  # Remove leading/trailing whitespace
            blocks.append({
                'language': language,
                'code': code
            })
        
        return blocks
