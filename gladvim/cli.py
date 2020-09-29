import click
import colorama

from .GladVim import GladVim
from . import util

colorama.init()

gladvim = None


@click.group()
def cli():
    global gladvim
    gladvim = GladVim()


@cli.command(help='Fetch package with a given name.')
@click.argument('package', type=click.STRING)
def fetch(package):
    util.call_and_report(gladvim.fetch, package)


@cli.command(help='Remove package with a given name.')
@click.argument('package', type=click.STRING)
def remove(package):
    util.call_and_report(gladvim.remove, package)


@cli.command(help='Plug fetched package with a given name.')
@click.argument('package', type=click.STRING)
def plug(package):
    util.call_and_report(gladvim.plug, package)


@cli.command(help='Unplug package with a given name.')
@click.argument('package', type=click.STRING)
def unplug(package):
    util.call_and_report(gladvim.unplug, package)


@cli.command(help='Equivalent to fetch + plug.')
@click.argument('package', type=click.STRING)
def install(package):
    util.call_and_report(gladvim.fetch, package)
    util.call_and_report(gladvim.plug, package)


@cli.command(help='Equivalent to unplug + remove.')
@click.argument('package', type=click.STRING)
def uninstall(package):
    util.call_and_report(gladvim.unplug, package)
    util.call_and_report(gladvim.remove, package)
