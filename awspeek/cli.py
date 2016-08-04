import core
import click

@click.command()
@click.option('--profile', default='dev')
@click.option('--show', default='instance')
def cli(profile, show):
    print core.show(profile, show)

if __name__ == "__main__":
    cli()
