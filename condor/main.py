import argparse
import sys

__version__ = "0.0"


class Condor(object):

    def __init__(
        self, verbose=False, ignore_names=None, ignore_decorators=None
    ):
        self.verbose = verbose
        self.ignore_names = ignore_names or []
        self.ignore_decorators = ignore_decorators or []

        self.filename = ""
        self.code = []
        self.found_dead_code_or_error = False

    def report(*args, **kwargs):
        print('PRINT')


def _parse_args():
    def csv(exclude):
        return exclude.split(",")

    usage = "%(prog)s [options] PATH [PATH ...]"
    version = "vulture {}".format(__version__)
    glob_help = "Patterns may contain glob wildcards (*, ?, [abc], [!abc])."
    parser = argparse.ArgumentParser(prog="vulture", usage=usage)
    parser.add_argument(
        "paths",
        nargs="+",
        metavar="PATH",
        help="Paths may be Python files or directories. For each directory"
        " Vulture analyzes all contained *.py files.",
    )
    parser.add_argument(
        "--exclude",
        metavar="PATTERNS",
        type=csv,
        help="Comma-separated list of paths to ignore (e.g.,"
        ' "*settings.py,docs/*.py"). {glob_help} A PATTERN without glob'
        " wildcards is treated as *PATTERN*.".format(**locals()),
    )
    parser.add_argument(
        "--ignore-decorators",
        metavar="PATTERNS",
        type=csv,
        help="Comma-separated list of decorators. Functions and classes using"
        ' these decorators are ignored (e.g., "@app.route,@require_*").'
        " {glob_help}".format(**locals()),
    )
    parser.add_argument(
        "--ignore-names",
        metavar="PATTERNS",
        type=csv,
        default=None,
        help='Comma-separated list of names to ignore (e.g., "visit_*,do_*").'
        " {glob_help}".format(**locals()),
    )
    parser.add_argument(
        "--make-whitelist",
        action="store_true",
        help="Report unused code in a format that can be added to a"
        " whitelist module.",
    )
    parser.add_argument(
        "--min-confidence",
        type=int,
        default=0,
        help="Minimum confidence (between 0 and 100) for code to be"
        " reported as unused.",
    )
    parser.add_argument(
        "--sort-by-size",
        action="store_true",
        help="Sort unused functions and classes by their lines of code.",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--version", action="version", version=version)
    return parser.parse_args()


def init():
    args = _parse_args()
    condor = Condor(
        verbose=args.verbose,
        ignore_names=args.ignore_names,
        ignore_decorators=args.ignore_decorators,
    )
    sys.exit(
        condor.report(
            min_confidence=args.min_confidence,
            sort_by_size=args.sort_by_size,
            make_whitelist=args.make_whitelist,
        )
    )
