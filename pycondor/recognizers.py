import ast

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

    def get_feature_flag_object(self):
        def is_ff(obj):
            return func == self.FEATURE_FLAG_MODULE

        values = self.node.test.values if hasattr(self.node.test, 'values') else None
        if values:
            for value in values:
                if isinstance(value, ast.Call):
                    func = value.func.value.id
                    if is_ff(func):
                        return {
                            'method': value.func.attr,
                            'args': value.args,
                            'func': func,
                            'complex': 1,
                        }

        func = self.node.test.func.value.id if hasattr(self.node.test, 'func') else None
        if is_ff(func):
            return {
                'method': self.node.test.func.attr,
                'args': self.node.test.args,
                'func': func,
                'complex': 0,
            }

    def generate_report(self):
        ff_object = self.get_feature_flag_object()
        if ff_object:
            if ff_object['func'] == self.FEATURE_FLAG_MODULE and ff_object['method'] == self.FEATURE_FLAG_METHOD:
                start_key_lineno = ff_object['args'][0].lineno
                key = ff_object['args'][0].attr
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
                    'complex_lines': [start_key_lineno] if ff_object['complex'] else [],
                    'dead_lines': [] if ff_object['complex'] else dead_lines,
                    'live_lines': [i for i in range(start_key_lineno + 1, else_start_lineno)],
                }
        return self.report

    @classmethod
    def get_live_lines(cls, report, key=None):
        live_lines = {}
        for ff in report[cls.STATS_KEY]:
            if live_lines.get(ff['key']) and ff['key'] == key and not ff['complex_lines']:
                live_lines[ff['key']] += ff['live_lines']
            elif key == ff['key'] and not ff['complex_lines']:
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

    @classmethod
    def get_complex_lines(cls, report, key=None):
        complex_lines = {}
        for ff in report[cls.STATS_KEY]:
            if complex_lines.get(ff['key']) and ff['key'] == key:
                complex_lines[ff['key']] += ff['complex_lines']
            elif key == ff['key']:
                complex_lines[ff['key']] = ff['complex_lines']
        return complex_lines


def get_recognizer(recognizer_name):
    recognizers = {
        FEATURE_FLAG_RECOGNIZER: FeatureFlagRecognizer,
    }

    return recognizers[recognizer_name]
