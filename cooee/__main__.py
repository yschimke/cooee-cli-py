import click
import webbrowser

@click.command()
@click.option('--login', is_flag=True, help='Login to coo.ee')
@click.option('--local', '-l', is_flag=True, help='Use local services')
def cooee(login: bool = False, local: bool = False):
    """https://coo.ee command line."""
    if (login):
        webbrowser.open(web_path(local=local))


def web_path(path: str = "/", local: bool = False):
    return f"https://www.coo.ee{path}"


if __name__ == '__main__':
    cooee()
