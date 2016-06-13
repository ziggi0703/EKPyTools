#!/usr/bin/env python


import click
from datetime import datetime
from ._transfer import parallel_rsync


@click.group()
def ekpy():
    pass


@ekpy.command()
@click.argument('sources', type=click.File(), nargs=1, help="File with all (ssh-)paths to the files to be copied: "
                                                            "'user@login.cc.kek.jp:/path/to/file.root' \n "
                                                            "Note: ssh forwarding must be enabled.")
@click.option('--dest', '-d', type=str, required=True, help='Target directory')
@click.option('--processes', '-p', default=10, help='Number of parallel processes.')
def par_sync(sources, dest, processes):
    """
    Parallel rsync to copy large amount of data
    """
    files = [source.strip() for source in sources.read().split('\n')]

    print('Copy {} files'.format(len(files)))

    start = datetime.now()
    parallel_rsync(files, dest, n=processes)
    end = datetime.now()

    duration = end - start

    print('Copied {} files in {}'.format(len(files), duration))

