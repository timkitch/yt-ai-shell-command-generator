import os
import click
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

def select_shell():
    shells = ['cmd', 'powershell', 'bash']
    for i, shell in enumerate(shells, 1):
        click.echo(f"{i}. {shell}")
    while True:
        choice = click.prompt("Select your preferred shell environment", type=int)
        if 1 <= choice <= len(shells):
            return shells[choice - 1]
        click.echo("Invalid choice. Please try again.")

def generate_command(client, shell, query):
    prompt = f"{HUMAN_PROMPT}Generate a {shell} command for the following query: {query}\n{AI_PROMPT}"
    response = client.completion(
        prompt=prompt,
        max_tokens_to_sample=300,
        model="claude-v1",
        stop_sequences=[HUMAN_PROMPT]
    )
    return response.completion.strip()

@click.command()
def main():
    shell = select_shell()
    client = Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    
    click.echo(f"Shell Command Generator initialized for {shell}.")
    
    while True:
        query = click.prompt("Enter your command query (or 'exit' to quit)")
        if query.lower() == 'exit':
            break
        command = generate_command(client, shell, query)
        click.echo(f"Generated command for {shell}:")
        click.echo(command)

    click.echo("Exiting Shell Command Generator.")

if __name__ == "__main__":
    main()
