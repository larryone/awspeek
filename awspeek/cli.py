import core
import click

@click.command()
@click.option('--profile', default='dev')
@click.option(
    '--show',
    default='instance',
    help='possible options: {}'.format(core.targets.keys())
)
def cli(profile, show):
    print core.show(profile, show)

if __name__ == "__main__":
    cli()
