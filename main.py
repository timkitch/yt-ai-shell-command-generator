import os
import click
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
    prompt = f"{HUMAN_PROMPT}Generate a {shell} command for the following query: {query}\n{AI_PROMPT}"
    response: Completion = client.completions.create(
        prompt=prompt,
        max_tokens_to_sample=300,
        model="claude-v1",
        stop_sequences=[HUMAN_PROMPT]
    )
    return response.completion.strip(), response.usage.completion_tokens

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
        click.echo(style(command, fg="green"))
        click.echo(style(f"Tokens used: {tokens}", fg="blue"))
        click.echo(style(f"Total tokens used this session: {total_tokens}", fg="magenta"))
        click.echo()  # Add an empty line for better readability

    click.echo(style("Exiting Shell Command Generator.", fg="red", bold=True))
    click.echo(style(f"Total tokens used this session: {total_tokens}", fg="magenta", bold=True))

if __name__ == "__main__":
    main()
