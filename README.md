# Description 
Generate scripts with AI that execute and autocorrect. For security reasons, this is done inside a docker container.  
Currently tuned to Python scripts.

# Settings
- Model: Claude 3.5 Sonnet 
-  

# Classes
- ModelAssistent: chosen model to help generate code.
- Executer: tests script correct execution

# Artifacts 
There is 2 folders that are exported outside the container:
- logs: script generation monitoring 
- output: files generated by prompts 

# Links
