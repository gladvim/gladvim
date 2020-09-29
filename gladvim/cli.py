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
@click.argument('packages', type=click.STRING, nargs=-1)
def fetch(packages):
    for package in packages:
        util.call_and_report(gladvim.fetch, package)


@cli.command(help='Remove package with a given name.')
@click.argument('packages', type=click.STRING, nargs=-1)
def remove(packages):
    for package in packages:
        util.call_and_report(gladvim.remove, package)


@cli.command(help='Plug fetched package with a given name.')
@click.argument('packages', type=click.STRING, nargs=-1)
def plug(packages):
    for package in packages:
        util.call_and_report(gladvim.plug, package)


@cli.command(help='Unplug package with a given name.')
@click.argument('packages', type=click.STRING, nargs=-1)
def unplug(packages):
    for package in packages:
        util.call_and_report(gladvim.unplug, package)


@cli.command(help='Equivalent to fetch + plug.')
@click.argument('packages', type=click.STRING, nargs=-1)
def install(packages):
    for package in packages:
        util.call_and_report(gladvim.fetch, package)
        util.call_and_report(gladvim.plug, package)


@cli.command(help='Equivalent to unplug + remove.')
@click.argument('packages', type=click.STRING, nargs=-1)
def uninstall(packages):
    for package in packages:
        util.call_and_report(gladvim.unplug, package)
        util.call_and_report(gladvim.remove, package)


@cli.command(help='Wipes out GladVim\'s local history.')
@click.option('-r', '--remove-packages', 'rm', is_flag=True,
              help='Uninstall all GladVim plugins.')
def selfdestruct(rm):
    gladvim.selfdestruct(rm)
