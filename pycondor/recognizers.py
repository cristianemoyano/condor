FEATURE_FLAG_RECOGNIZER = 'feature_flag_recognizer'


class FeatureFlagRecognizer(object):

    # REQUIRED
    STATS_KEY = 'feature_flags'
    NAME = FEATURE_FLAG_RECOGNIZER

    # EXTRAS
    FEATURE_FLAG_MODULE = 'feature_flag'
    FEATURE_FLAG_METHOD = 'is_active'

    def __init__(self, node):
        self.node = node
        self.report = {}

    def generate_report(self):
        func = self.node.test.func.value.id if hasattr(self.node.test, 'func') else None
        if func:
            attr = self.node.test.func.attr if hasattr(self.node.test.func, 'attr') else None
            if func == self.FEATURE_FLAG_MODULE and attr == self.FEATURE_FLAG_METHOD:
                start_key_lineno = self.node.test.args[0].lineno
                key = self.node.test.args[0].attr
                dead_lines = [start_key_lineno]
                else_body = self.node.orelse
                else_start_lineno = 0
                if else_body:
                    else_start_lineno = else_body[0].lineno - 1
                    dead_lines.append(else_start_lineno)
                    for statement in else_body:
                        dead_lines.append(statement.lineno)

                self.report = {
                    'key': key,
                    'dead_lines': dead_lines,
                    'live_lines': [i for i in range(start_key_lineno + 1, else_start_lineno)],
                }
        return self.report

    @classmethod
    def get_live_lines(cls, report, key=None):
        live_lines = {}
        for ff in report[cls.STATS_KEY]:
            if live_lines.get(ff['key']) and ff['key'] == key:
                live_lines[ff['key']] += ff['live_lines']
            elif key == ff['key']:
                live_lines[ff['key']] = ff['live_lines']
        return live_lines

    @classmethod
    def get_dead_lines(cls, report, key=None):
        dead_lines = {}
        for ff in report[cls.STATS_KEY]:
            if dead_lines.get(ff['key']) and ff['key'] == key:
                dead_lines[ff['key']] += ff['dead_lines']
            elif key == ff['key']:
                dead_lines[ff['key']] = ff['dead_lines']
        return dead_lines


def get_recognizer(recognizer_name):
    recognizers = {
        FEATURE_FLAG_RECOGNIZER: FeatureFlagRecognizer,
    }

    return recognizers[recognizer_name]
