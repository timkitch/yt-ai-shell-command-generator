import os
import click
from anthropic import Anthropic

def select_shell():
    shells = ['cmd', 'powershell', 'bash']
    for i, shell in enumerate(shells, 1):
        click.echo(f"{i}. {shell}")
    while True:
        choice = click.prompt("Select your preferred shell environment", type=int)
        if 1 <= choice <= len(shells):
            return shells[choice - 1]
        click.echo("Invalid choice. Please try again.")

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
        click.echo(f"Your query for {shell}: {query}")
        # TODO: Process the query and generate the command

    click.echo("Exiting Shell Command Generator.")

if __name__ == "__main__":
    main()
