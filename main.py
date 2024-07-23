import os
import click
import pyperclip
from dotenv import load_dotenv
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from click import style
from anthropic.types import Completion

load_dotenv()  # Load environment variables from .env file

def select_shell():
    shells = ['cmd', 'powershell', 'bash']
    for i, shell in enumerate(shells, 1):
        click.echo(f"{i}. {shell}")
    while True:
        choice = click.prompt("Select your preferred shell environment", type=int)
        if 1 <= choice <= len(shells):
            return shells[choice - 1]
        click.echo("Invalid choice. Please try again.")

def generate_command(client, shell, query) -> tuple[str, int]:
    prompt = f"{HUMAN_PROMPT}Generate a valid {shell} command for the following query: {query}. Ensure the command is complete and executable.\n{AI_PROMPT}"
    response: Completion = client.completions.create(
        prompt=prompt,
        max_tokens_to_sample=300,
        model="claude-v1",
        stop_sequences=[HUMAN_PROMPT]
    )
    # Extract only the command from the response
    command = response.completion.strip().split('\n')[0]
    # Ensure the command is not empty
    if not command:
        command = f"echo 'Unable to generate a valid command for: {query}'"
    # The token count is not directly available, so we'll estimate it
    # This is a rough estimate and may not be entirely accurate
    estimated_tokens = len(command.split()) + len(prompt.split())
    return command, estimated_tokens

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
    
    total_tokens = 0
    while True:
        query = click.prompt(style("Enter your command query (or 'exit' to quit)", fg="cyan"))
        if query.lower() == 'exit':
            break
        command, tokens = generate_command(client, shell, query)
        total_tokens += tokens
        click.echo(style(f"\nGenerated command for {shell}:", fg="yellow", bold=True))
        click.echo(command)  # Print the command without any styling
        click.echo(style(f"Tokens used: {tokens}", fg="blue"))
        click.echo(style(f"Total tokens used this session: {total_tokens}", fg="magenta"))
        
        if click.confirm("Do you want to copy this command to clipboard?"):
            copy_to_clipboard(command)
        
        click.echo(style("\nCommand (for easy copy-paste):", fg="cyan"))
        click.echo(command)  # Print the command again for easy copy-paste
        
        click.echo()  # Add an empty line for better readability

    click.echo(style("Exiting Shell Command Generator.", fg="red", bold=True))
    click.echo(style(f"Total tokens used this session: {total_tokens}", fg="magenta", bold=True))

if __name__ == "__main__":
    main()
