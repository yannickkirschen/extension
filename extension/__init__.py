# Copyright 2019 Yannick Kirschen. All rights reserved.
# Use of this source code is governed by the GNU-GPL
# license that can be found in the LICENSE file.

# Date created: July 21, 2019


import json
import os
import platform
import random
import shutil
import time
import _thread
import threading
from os.path import abspath, dirname, isfile, join

import flask
import markdown

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern


__all__ = [
    'Cache',
    'CsvReader',
    'CsvWriter',
    'Logger',
    'Singleton',

    'clear',
    'cur_dir',
    'get_json',
    'parse_csv',
    'ran_num',
    'read_file',
    'render_markdown',
    'render_markdown_from_file',
    'render_markdown_for_flask',
    'render_markdown_from_file_for_flask',
    'timestamp',
    'save_json',
    'write_csv',
    'write_file'
]


EMOJI_RE = r'(:)(.*?):'


def read_file(file):
    """
    Reads a file.

    Parameters:
        file: Path to the file.

    Returns:
        The content of the file.
    """
    with open(file, 'r') as f:
        return f.read()


def write_file(file, data):
    """
    Writes data to a file at once.

    Parameters:
        file: Path to the file.
        data: Data to write.
    """
    with open(file, 'w') as f:
        f.write(data)


def clear():
    """
    Clears the console platform-specific.
    """
    p = platform.system()
    if p == 'Windows':
        os.system('cls')
    elif p in ['Linux', 'Darwin']:
        os.system('clear')


def cur_dir(file):
    """
    Gets the current directory of a file.

    Arguments:
        file: File to get the directory from.

    Returns:
        The directory.
    """
    return dirname(os.path.realpath(file))


def ran_num(length=1):
    """
    Random string number generator.

    This function generates a string with a custom length
    that contains random digits and characters from a-f.

    Parameters:
        length: Number of places the number should have.

    Returns:
        A string with random digits and characters.
    """
    number = ''
    for z in range(length):
        r = random.randint(0, 15)
        if 0 <= r <= 9:
            number += str(r)
        elif r == 10:
            number += 'a'
        elif r == 11:
            number += 'b'
        elif r == 12:
            number += 'c'
        elif r == 13:
            number += 'd'
        elif random == 14:
            number += 'e'
        elif r == 15:
            number += 'f'
    return number


def timestamp():
    """
    Creates the local time as a string of the format <YYYY-MM-DD:HH-mm-SS>.

    Returns:
        The local time as a string.
    """
    t = time.localtime()
    return '{}-{}-{}:{}-{}-{}'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)


def get_json(file, path=''):
    """
    Reads and parses a JSON file.

    Parameters:
        file: The name of the JSON file to read.
        path: The path to the JSON file, if it is not in the working directory.

    Returns:
        A dict containing the JSON file's content.
    """
    with open(os.path.join(path, file), 'r', encoding='UTF-8') as j:
        return json.load(j)


def save_json(file, data, path=''):
    """
    Writes data to a JSON file.

    Parameters:
        file: The name of the JSON file to write to.
        data: The object to write.
        path: The path to the JSON file, if it is not in the working directory.
    """
    if not os.path.exists(path):
        os.mkdir(path)

    with open(os.path.join(path, file), 'w', encoding='UTF-8') as j:
        json.dump(data, j, indent=4)


class EmojiExtension(Extension):
    """
    Original version can be found here: https://github.com/bytefish/MarkdownEmojiExtension.
    """
    def __init__(self, **kwargs):
        self.config = {
            'emojis': [[], 'List of Emojis.']
        }
        self.as_dictionary = lambda emojis: dict((emoji['key'], emoji['value']) for emoji in emojis)
        super(EmojiExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        emojis = self.as_dictionary(self.getConfig('emojis'))
        pattern = EmojiInlinePattern(EMOJI_RE, emojis)
        md.inlinePatterns.add('emoji', pattern, '<not_strong')

    @staticmethod
    def create_from_json():
        return EmojiExtension(emojis=get_json('emojis.json', path=abspath(__file__).replace('__init__.py', '')))


class EmojiInlinePattern(Pattern):
    def __init__(self, pattern, emojis):
        super(EmojiInlinePattern, self).__init__(pattern)
        self.emojis = emojis

    def handleMatch(self, m):
        emoji_key = m.group(3)
        return self.emojis.get(emoji_key, '')


def render_markdown(markdown_string=''):
    """
    Renders a string containing markdown to an HTML string.

    Parameters:
        markdown_string: A string containing markdown.

    Returns:
        The rendered HTML.
    """
    return markdown.markdown(markdown_string, extensions=[EmojiExtension.create_from_json()])


def render_markdown_for_flask(markdown_string=''):
    """
    Renders a string containing markdown to an HTML string and formats it for Flask.

    Parameters:
        markdown_string: A string containing markdown.

    Returns:
        The rendered HTML for Flask.
    """
    return flask.Markup(render_markdown(markdown_string))


def render_markdown_from_file(file):
    """
    Renders a file containing markdown to an HTML string and formats it for Flask.

    Parameters:
        file: A file containing markdown.

    Returns:
        The rendered HTML for Flask.
    """
    with open(file, 'r', encoding='UTF-8') as f:
        return render_markdown_for_flask(f.read())


def render_markdown_from_file_for_flask(file):
    """
    Renders a file containing markdown to an HTML string.

    Parameters:
        file: A file containing markdown.

    Returns:
        The rendered HTML.
    """
    with open(file, 'r', encoding='UTF-8') as f:
        return render_markdown(f.read())


def parse_csv(input_file, separator=','):
    """
    Parses a CSV-File and stores it at once in a list.

    Parameters:
        input_file: CSV-File to read from.
        separator: Separator of each element; Default: ','.
    """
    r = CsvReader(input_file, separator)
    data = []

    while r.has_next():
        data.append(r.pull())

    return data


def write_csv(output_file, data, separator=','):
    """
    Writes a CSV-File from a list.

    Parameters:
        output_file: CSV-File to write to.
        data: The list of lines to write.
        separator: Separator of each element; Default: ','
    """
    w = CsvWriter(output_file, separator)
    for line in data:
        w.push(line)


class CsvReader:
    """
    Dynamic CSV-Reader. File is read line by line.
    """
    def __init__(self, input_file, separator=','):
        """
        Initialize a new CsvReader.

        Parameters:
            input_file: CSV-File to read from.
            separator: Separator of each element; Default: ','.
        """
        self.file = open(input_file, 'r')
        self.separator = separator

        self._line = ''
        self._input_file = input_file

    def __del__(self):
        """
        Make sure the file is closed.
        """
        self.file.close()

    def __str__(self):
        return '<CSV-File: {}>'.format(self._input_file)

    def __repr__(self):
        return '<CSV-File: {}>'.format(self._input_file)

    def has_next(self):
        """
        Checks if there is a next line in the file.

        Returns:
            True, if there is a next line, otherwise False.
        """
        self._line = self.file.readline().strip()
        return not self._line == ''

    def pull(self):
        """
        Reads the next line.

        Returns:
            A list with all elements from that line.
        """
        line_list = []
        line_string = ''
        in_quote = False
        index = 1

        for char in self._line:
            if char == self.separator and not in_quote:
                line_list.append(line_string.strip())
                line_string = ''
            elif char == '"':
                in_quote = not in_quote
            else:
                line_string += char

            index += 1
        line_list.append(line_string.strip())
        return line_list


class CsvWriter:
    """
    Dynamic CSV-Writer. File is written line by line.
    """
    def __init__(self, output_file, separator=','):
        """
        Initialize a new CsvWriter.

        Parameters:
            output_file: CSV-File to write to.
            separator: Separator of each element; Default: ','.
        """
        self.file = open(output_file, 'w')
        self.separator = separator

        self._line = ''
        self._output_file = output_file

    def __del__(self):
        """
        Make sure the file is closed.
        """
        self.file.close()

    def __str__(self):
        return '<CSV-File: {}>'.format(self._output_file)

    def __repr__(self):
        return '<CSV-File: {}>'.format(self._output_file)

    def push(self, line):
        string = ''
        for s in line:
            string += '"' + s + '"' + self.separator
        self.file.write(string[:len(string) - 1] + '\n')


class TangoIcon:
    """
    Represents an icon from the Icon-Set Tango.

    """
    def __init__(self, image, static=''):
        """
        Initializes an icon.

        Arguments:
            image: The name of the image to display.
            static: If set to <True>, the image gets copied to <static_path>.
            static: If <static> is set to <True>, the image gets copied
            to this path.
        """
        self._image = image

        if not static == '':
            self.make_static(static)

    def make_static(self, path):
        """
        Copies the image to a certain destination. Some applications need
        static files in a special directory (e.g. Flask).

        Arguments:
            path: The absolute path, the image should be copied to.
        """
        img = join(path, self.image)
        if not isfile(img):
            shutil.copyfile(self.path, img)

    @property
    def image(self):
        """
        Returns:
            The name of the image.
        """
        return self._image

    @property
    def path(self):
        """
        Returns:
            The absolute path to the requested icon.
        """
        return os.path.join(abspath(__file__).replace('__init__.py', ''), 'resources/{}'.format(self.image))


class Singleton(type):
    """
    When this class is the metaclass of another class, this would be a singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Cache(metaclass=Singleton):
    """
    Implements a simple, thread-safe cache by using a dict.
    """
    def __init__(self, ttl=0):
        self.__data = {}
        self.__lock = threading.Lock()
        _log.info('Initialized cache with ttl {}.'.format(ttl))
        _thread.start_new_thread(_ttl_master, (ttl,))

    def __del__(self):
        with self.__lock:
            self.__data = {}

    def __setitem__(self, key, value):
        with self.__lock:
            self.__data[key] = value

    def __getitem__(self, item):
        with self.__lock:
            return self.__data[item]

    def __contains__(self, item):
        with self.__lock:
            return item in self.__data

    def pop(self, key, default=None):
        try:
            with self.__lock:
                item = self.__data[key]
                del self.__data[key]
                return item
        except KeyError:
            return default

    def get(self, key, default=None):
        try:
            with self.__lock:
                return self.__data[key]
        except KeyError:
            return default

    def keys(self):
        with self.__lock:
            return [key for key in self.__data]

    def values(self):
        with self.__lock:
            return [self.__data[key] for key in self.__data]

    def clear(self):
        self.__del__()

    def __str__(self):
        return str(self.__data)

    def __repr__(self):
        return str(self.__data)

    def __hash__(self):
        return hash(self.__data)

    def __eq__(self, other):
        return self.__data == other


def _ttl_master(ttl):
    if ttl == 0:
        return

    time.sleep(ttl)
    c = Cache()
    c.clear()
    _log.info('Deleted cache.')


class Logger:
    """
    Implements a simple logger that can print to the terminal or write into a file.
    """
    def __init__(self, source_file, output='terminal', scope='info'):
        self.source_file = source_file
        self.output = output
        self.file = None
        self.scope = scope

        self.message_format = ' * {} - ({}) - {} - {}'

        if not self.output == 'terminal':
            self.file = open(self.output, 'a')

    def __del__(self):
        if self.file:
            self.file.close()

    def __str__(self):
        return '<Logger: {}>'.format(self.source_file)

    def _print(self, msg):
        """
        Either prints the log to the console or writes it into a file.
        """
        if not self.file:
            print(msg)
        else:
            self.file.write(msg + '\n')

    def _log(self, message, level):
        """
        Logs the message.
        """
        msg = self.message_format.format(level, timestamp(), abspath(self.source_file), message)

        if self.scope == 'error' and 'error' in level:
            self._print(msg)
        elif self.scope == 'warning':
            if 'error' in level or 'warning' in level:
                self._print(msg)
        elif self.scope == 'info':
            if 'error' in level or 'warning' in level or 'info' in level:
                self._print(msg)
        elif self.scope == 'debug':
            self._print(msg)

    def error(self, message):
        """
        Prints an error.
        """
        self._log(message, 'error  ')

    def warning(self, message):
        """
        Prints a warning.
        """
        self._log(message, 'warning')

    def info(self, message):
        """
        Prints an info.
        """
        self._log(message, 'info   ')

    def debug(self, message):
        """
        Prints a debug message.
        """
        self._log(message, 'debug  ')


_log = Logger(__file__)
