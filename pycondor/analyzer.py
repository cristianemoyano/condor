import ast

from recognizers import get_recognizer, FEATURE_FLAG_RECOGNIZER
from logger import getLogger

class AnalyzerMixin(object):

    def _collect_stats(self, report):
        # print(ast.dump(node))  # Debug
        if report:
            self.stats[self.recognizer.NAME][self.recognizer.STATS_KEY].append(report)


class Analyzer(ast.NodeVisitor, AnalyzerMixin):
    def __init__(self):
        self.recognizer = get_recognizer(FEATURE_FLAG_RECOGNIZER)
        self.stats = {
            self.recognizer.NAME: {
                self.recognizer.STATS_KEY: [],
            }
        }
        self.logger = getLogger('analyzer')

    def visit_If(self, node):
        self._collect_stats(self.recognizer(node).generate_report())
        self.generic_visit(node)

    def report(self):
        self.logger.info(self.stats)


if __name__ == "__main__":
    with open("dead_code.py", "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()
