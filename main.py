import os
import click
from anthropic import Anthropic

@click.command()
@click.option('--shell', type=click.Choice(['cmd', 'powershell', 'bash']), prompt='Select your preferred shell environment', help='The shell environment to generate commands for.')
def main(shell):
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
