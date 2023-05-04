"""..."""
import click

@click.command()
@click.option('--name', prompt=True)
@click.option('--phone', prompt=True, type=int)
def add_phone(name, phone):
    click.echo(f'params {name}, {phone}!')

@click.command()
@click.option('--name', prompt=True)
@click.option('--phone', prompt=True, type=int)
@click.option('--old_phone', prompt=True, type=int)
def change_phone(name, phone, old_phone):
    click.echo(f'params {name}, {phone}, and {old_phone}!')

functions = {
    'c1': add_phone,
    'c2': change_phone,
}

@click.command()
@click.option('--command', prompt=True, type=click.Choice(functions.keys()))
def main(command):
    functions[command]()

if __name__ == '__main__':
    main()


# import click

# click.echo(click.style('Hello World!', fg='blue'))
# click.echo(click.style('Some more text', bg='blue', fg='white'))
# click.echo(click.style('ATTENTION', blink=True, bold=True))
