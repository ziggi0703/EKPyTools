#!/usr/bin/env python
import subprocess
from multiprocessing import Pool
from functools import partial


def _start_rsync(source, dest):
    subprocess.call(['rsync', source, dest])

def parallel_rsync(sources, dest, n=10):
    """
    Start n rsync process to copy sources to dest
    :param source:
    :type source:
    :param dest:
    :type dest:
    :param processes:
    :type processes:
    :return:
    :rtype:
    """
    if len(sources) < n:
        n = len(sources)

    pool = Pool(n)

    start_rsync_partial = partial(_start_rsync, dest=dest)

    pool.map(start_rsync_partial, sources)



