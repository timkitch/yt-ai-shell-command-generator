import os
import click
import pyperclip
from dotenv import load_dotenv
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from click import style
from anthropic.types import Completion

load_dotenv()  # Load environment variables from .env file

def select_shell(shells=['cmd', 'powershell', 'bash'], input_func=click.prompt):
    """
    Prompts the user to select their preferred shell environment from a list of options.
    
    Args:
        shells (list): List of available shells.
        input_func (function): Function to use for user input (for testing purposes).
    
    Returns:
        str: The selected shell environment.
    """
    for i, shell in enumerate(shells, 1):
        click.echo(f"{i}. {shell}")
    while True:
        choice = input_func("Select your preferred shell environment")
        try:
            choice = int(choice)
            if 1 <= choice <= len(shells):
                return shells[choice - 1]
        except ValueError:
            pass
        click.echo("Invalid choice. Please try again.")

def generate_command(client, shell, query) -> str:
    """
    Generate a shell command based on a user's query using the Anthropic API.
    
    Args:
        client (Anthropic): An Anthropic API client instance.
        shell (str): The user's preferred shell environment.
        query (str): The user's command query.
    
    Returns:
        str: The generated shell command.
    """
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"Generate a valid {shell} command for the following query: {query}. Return ONLY the command, without any explanation."
            }
        ]
    )
    # Extract the command from the response
    command = response.content[0].text.strip()
    # Ensure the command is not empty and doesn't start with explanatory text
    if not command or not command[0].isalnum():
        command = f"echo 'Unable to generate a valid command for: {query}'"
    return command

def copy_to_clipboard(text):
    pyperclip.copy(text)
    click.echo(style("Command copied to clipboard!", fg="green"))

@click.command()
def main():
    shell = select_shell()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    client = Anthropic(api_key=api_key)
    
    click.echo(style(f"Shell Command Generator initialized for {shell}.", fg="green", bold=True))
    
    while True:
        query = click.prompt(style("Enter your command query (or 'exit' to quit)", fg="cyan"))
        if query.lower() == 'exit':
            break
        command = generate_command(client, shell, query)
        click.echo(style(f"\nGenerated command for {shell}:", fg="yellow", bold=True))
        click.echo(style(command, fg="green"))  # Print the command with green styling
        
        if click.confirm(style("Do you want to copy this command to clipboard?", fg="cyan")):
            copy_to_clipboard(command)
            click.echo(style("Command copied to clipboard!", fg="green"))
        
        click.echo(style("\nCommand (for easy copy-paste):", fg="cyan"))
        click.echo(command)  # Print the command again without styling for easy copy-paste
        
        click.echo()  # Add an empty line for better readability

    click.echo(style("Exiting Shell Command Generator.", fg="red", bold=True))

if __name__ == "__main__":
    main()
