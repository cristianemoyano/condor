import argparse
import sys

__version__ = "0.0.1"


class PyCondor(object):

    def report(*args, **kwargs):
        print('PRINT')


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
