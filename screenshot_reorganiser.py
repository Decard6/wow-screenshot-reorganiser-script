#!/usr/bin/env python3

import argparse
import re
import os
import shutil


class InvalidFileNameException(Exception):
    def __init__(self, file_name):
        self.message = f'{file_name} is not valid'
        super().__init__(self.message)


class WowDateTime:
    def __init__(self, file_name):
        regex = re.compile(
            r'^WoWScrnShot_(\d{2})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2}).jpg$')
        result = regex.match(file_name)
        if result == None:
            raise InvalidFileNameException(file_name)

        self.month = result.group(1)
        self.day = result.group(2)
        self.year = result.group(3)
        self.hour = result.group(4)
        self.minute = result.group(5)
        self.second = result.group(6)

    def format_name(self):
        return f'{self.year}{self.month}{self.day}_{self.hour}{self.minute}{self.second}.jpg'


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Reorganises wow screenshots"
                                     "so they're in YYMMDD_HHmmSS format.")

    parser.add_argument(
        '-p', '--path', help='Path to wow directory.', required=True)
    args = parser.parse_args()

    screenshots_dir = os.path.join(args.path, 'Screenshots')

    for file in os.listdir(screenshots_dir):
        if file.endswith('.jpg'):
            try:
                new_name = WowDateTime(file).format_name()
            except InvalidFileNameException:
                continue

            src = os.path.join(screenshots_dir, file)
            dest = os.path.join(screenshots_dir, new_name)
            shutil.move(src, dest)
