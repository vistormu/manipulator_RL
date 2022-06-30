import csv


class Save:

    def __init__(self, filename, fieldnames) -> None:
        self.filename = filename
        self.fieldnames = fieldnames
        self._write_header()

    def _write_header(self):
        with open(self.filename, 'a', encoding='UTF8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

    def row(self, data):
        with open(self.filename, 'a', encoding='UTF8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(data)
