#!/usr/bin/env python


import click
from datetime import datetime
from ._transfer import parallel_rsync


@click.group()
def ekpy():
    pass


@ekpy.command()
@click.argument('sources', type=click.File(), nargs=1)
@click.option('--dest', '-d', required=True, help='destination')
@click.option('--processes', '-p', default=10)
def par_sync(sources, dest, processes):
    """
    Parallel rsync to copy large amount of data
    """
    files = [source.strip() for source in sources.read().split('\n')]

    print 'Copy {} files'.format(len(files))

    start = datetime.now()
    parallel_rsync(files, dest, n=processes)
    end = datetime.now()

    duration = end - start

    print 'Copied {} files in {}'.format(len(files), duration)

