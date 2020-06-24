import json
import itertools

from recognizers import get_recognizer, FEATURE_FLAG_RECOGNIZER
from logger import getLogger


class Cleaner(object):

    TAB_4 = '    '

    def __init__(self, filename=None):
        self.logger = getLogger('cleaner')
        self.recognizer = get_recognizer(FEATURE_FLAG_RECOGNIZER)
        self.separator = self.TAB_4
        self.ANALYZER_LOG = "analyzer.txt"
        self.DIRTY_FILE = filename if filename else "dead_code.py"
        self.DUMMY_FILE = self.DIRTY_FILE + '.bak'
        self.dead_lines = []
        self.live_lines = []
        self.complex_lines = []
        self.target_key = 'FEATURE_1'

    @staticmethod
    def parse_line_to_dict(string_dict):
        """Parse a string(dict) to dict"""
        string = string_dict.replace("\'", "\"")
        return json.loads(string)

    @staticmethod
    def get_item_depth(list_of_dict):
        """
        given a list returns how many times the item is repeated
        """
        new_list_of_dict = []
        for dic in list_of_dict:
            new_list_of_dict.append(
                {k: {i: items.count(i) for i in items} for k, items in dic.items()}
            )
        return new_list_of_dict

    @staticmethod
    def flat_list(list_of_dict):
        """Flat a list of dict"""
        full_list = []
        for dic in list_of_dict:
            full_list.append(list(itertools.chain.from_iterable(dic.values())))
        return set(itertools.chain.from_iterable(full_list))

    def _parse_live_and_dead_lines(self):
        """Parse the live and dead lines from the analyzer log"""
        with open(self.ANALYZER_LOG, 'r') as log:
            for line in log:
                parsed_line = Cleaner.parse_line_to_dict(line)
                self.live_lines.append(self.recognizer.get_live_lines(
                    parsed_line[self.recognizer.NAME],
                    self.target_key,
                ))
                self.dead_lines.append(self.recognizer.get_dead_lines(
                    parsed_line[self.recognizer.NAME],
                    self.target_key,
                ))
                self.complex_lines.append(self.recognizer.get_complex_lines(
                    parsed_line[self.recognizer.NAME],
                    self.target_key,
                ))

    def _remove_tab(self, line, total=1):
        """Remove one tab given a code line"""
        # Obtain the statement from the line
        statement = [tab for tab in line.split(self.separator) if tab != '']
        # Total tabs
        tabs = sum(tab == '' for tab in line.split(self.separator))
        # Add first the total tabs - 1
        new_line_splitted = []
        for _ in range(0, tabs - total):
            new_line_splitted.append(self.separator)
        # Insert again the statement
        new_line_splitted += statement
        # Join everything in a single string
        return ''.join(new_line_splitted)

    def _remove_feature_flag_statement(self, line):
        stament_splitted = line.split(' ')
        indexes_to_remove = []
        ff_index = None
        for index, st in enumerate(stament_splitted):
            if self.target_key in st:
                ff_index = index
                indexes_to_remove.append(ff_index)
        if stament_splitted[ff_index - 1] in ['and', 'or']:
            indexes_to_remove.append(ff_index - 1)
        elif stament_splitted[ff_index + 1] in ['and', 'or']:
            indexes_to_remove.append(ff_index + 1)

        new_list = []
        for index, st in enumerate(stament_splitted):
            if index not in indexes_to_remove:
                new_list.append(st)
        return ' '.join(new_list)

    def _regenerate_file(self):
        # Flat the lines. This is because the dead_lines and live_lines are list of dict: list[dict]
        dead_lines_flatten = Cleaner.flat_list(self.dead_lines)
        complex_lines_flatten = Cleaner.flat_list(self.complex_lines)
        # Complex lines has another treatment
        dead_lines_flatten -= complex_lines_flatten
        live_lines_flatten = Cleaner.flat_list(Cleaner.get_item_depth(self.live_lines))
        live_lines_flatten = {li for li in live_lines_flatten if li not in dead_lines_flatten}
        live_lines_flatten -= complex_lines_flatten
        live_lines_with_depth = Cleaner.get_item_depth(self.live_lines)

        target_live_lines = None
        for live_lines in live_lines_with_depth:
            target_live_lines = live_lines.get(self.target_key)

        special_lines = list(itertools.chain(live_lines_flatten, complex_lines_flatten, dead_lines_flatten))

        # Open the dirty file in read mode and the dummy file in write mode
        with open(self.DIRTY_FILE, 'r') as dirty, open(self.DUMMY_FILE, 'w') as dummy:
            # Iterate line by line from the dirty file
            for index, line in enumerate(dirty, 1):
                # Remove tabs from live lines
                if index in live_lines_flatten:
                    new_line = self._remove_tab(line, target_live_lines.get(index, 1))
                    dummy.write(new_line)
                    self.logger.info('line MOV {index}: {line}'.format(line=str(line).rstrip(), index=index))
                elif index in complex_lines_flatten:
                    new_line = self._remove_feature_flag_statement(line)
                    dummy.write(new_line)
                    self.logger.info('line UPT {index}: {line}'.format(line=str(new_line).rstrip(), index=index))
                # Copy the rest of the lines and skip the dead lines into the dummy file.
                elif index not in special_lines:
                    dummy.write(line)
                # Log only affected lines.
                else:
                    self.logger.info('line REM {index}: {line}'.format(line=str(line).rstrip(), index=index))

    def clean(self):
        self._parse_live_and_dead_lines()
        self._regenerate_file()


if __name__ == "__main__":
    Cleaner().clean()
