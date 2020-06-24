import argparse
import sys

from pycondor.version import __version__

class PyCondor(object):

    def report(*args, **kwargs):
        print('Pepe')


def _parse_args():
    usage = "%(prog)s [options] PATH [PATH ...]"
    version = "pycondor {}".format(__version__)

    parser = argparse.ArgumentParser(prog="pycondor", usage=usage)
    parser.add_argument("--version", action="version", version=version)
    return parser.parse_args()


def init():
    _parse_args()
    pycondor = PyCondor()
    sys.exit(
        pycondor.report()
    )
