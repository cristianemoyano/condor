import os

class ApplicationProcess(object):

    def __init__(self, filename):
        self.original_file = filename if filename else "dead_code.py"
        self.backup_file = self.original_file + '.bak'

    def apply(self):
        os.rename(self.backup_file, self.original_file)


if __name__ == "__main__":
    ApplicationProcess().apply()
