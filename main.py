import os
from anthropic import Anthropic

def main():
    client = Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    
    print("Shell Command Generator initialized.")

if __name__ == "__main__":
    main()
