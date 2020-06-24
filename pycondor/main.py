import ast
import argparse
import sys

from pycondor.version import __version__
from pycondor.analyzer import Analyzer
from pycondor.cleaner import Cleaner
from pycondor.replace import ApplicationProcess

class PyCondor(object):

    def __init__(self, filename):
        self.filename = filename

    def analyze(self):
        with open(self.filename, "r") as source:
            tree = ast.parse(source.read())
        analyzer = Analyzer()
        analyzer.visit(tree)
        analyzer.report()

    def clean(self):
        Cleaner(filename=self.filename).clean()

    def apply(self):
        ApplicationProcess(filename=self.filename).apply()

    def process(self):
        self.analyze()
        self.cleaner()
        self.apply()


def parse_args():
    usage = "%(prog)s [options] PATH [PATH ...]"
    version = "pycondor {}".format(__version__)

    parser = argparse.ArgumentParser(prog="pycondor", usage=usage)
    parser.add_argument("--version", action="version", version=version)
    parser.add_argument("-f", required=True, type=str, help="File with dead code.")
    return parser.parse_args()


def init():
    args = parse_args()
    pycondor = PyCondor(filename=args.f)
    sys.exit(
        pycondor.process()
    )
