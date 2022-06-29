import dataclasses


@dataclasses.dataclass
class Codes:
    end = "\x1b[0m"
    bold = "\x1b[1m"
    dim = "\x1b[2m"
    italic = "\x1b[2m"
    underscore = "\x1b[4m"
    blink = "\x1b[5m"
    highlight = "\x1b[7m"
    hidden = "\x1b[8m"
    strikethrough = "\x1b[9m"
    double_underscore = "\x1b[21m"

    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    magenta = "\x1b[35m"
    cyan = "\x1b[36m"
    white = "\x1b[37m"

    black__bg = "\x1b[40m"
    red_bg = "\x1b[41m"
    green_bg = "\x1b[42m"
    yellow_bg = "\x1b[43m"
    blue_bg = "\x1b[44m"
    magenta_bg = "\x1b[45m"
    cyan_bg = "\x1b[46m"
    white_bg = "\x1b[47m"

    secondary_black = "\x1b[90m"
    secondary_red = "\x1b[91m"
    secondary_green = "\x1b[92m"
    secondary_yellow = "\x1b[93m"
    secondary_blue = "\x1b[94m"
    secondary_magenta = "\x1b[95m"
    secondary_cyan = "\x1b[96m"
    secondary_white = "\x1b[97m"

    secondary_black_bg = "\x1b[40m"
    secondary_red_bg = "\x1b[41m"
    secondary_green_bg = "\x1b[42m"
    secondary_yellow_bg = "\x1b[43m"
    secondary_blue_bg = "\x1b[44m"
    secondary_magenta_bg = "\x1b[45m"
    secondary_cyan_bg = "\x1b[46m"
    secondary_white_bg = "\x1b[47m"

    line_up = "\x1b[1A"
    line_clear = "\x1b[2K"


class Formatter:
    @staticmethod
    def bold(message: str) -> str:
        return Codes.bold + message + Codes.end

    @staticmethod
    def green(message: str) -> str:
        return Codes.secondary_green + message + Codes.end

    @staticmethod
    def blue(message: str) -> str:
        return Codes.secondary_blue + message + Codes.end

    @staticmethod
    def yellow(message: str) -> str:
        return Codes.yellow + message + Codes.end

    @staticmethod
    def red(message: str) -> str:
        return Codes.red + message + Codes.end


def output(function):

    def wrapper(*args, **kwargs):
        return_value = function(*args, **kwargs)

        print(return_value)
        if kwargs.get('flush'):
            print(Codes.line_up, end=Codes.line_clear)

    return wrapper


class Logger:

    def __init__(self, name: str) -> None:
        self.__mute_info = False
        self.__mute_debug = False
        self.__mute_warning = False
        self.__mute_error = False

        self.__info_prefix = self._create_prefix(name, 'info')
        self.__debug_prefix = self._create_prefix(name, 'debug')
        self.__warning_prefix = self._create_prefix(name, 'warning')
        self.__error_prefix = self._create_prefix(name, 'error')

    @staticmethod
    def _create_prefix(name, level):
        prefix = Formatter.bold("[" + name + "]")

        if level == 'info':
            return Formatter.green(prefix) + Formatter.green("[INFO] ")
        elif level == 'debug':
            return Formatter.blue(prefix) + Formatter.blue("[DEBUG] ")
        elif level == 'warning':
            return Formatter.yellow(prefix) + Formatter.yellow("[WARNING] ")
        elif level == 'error':
            return Formatter.red(prefix) + Formatter.red("[ERROR] ")

    @ output
    def info(self, *message, flush=False) -> None:
        if self.__mute_info:
            return

        return self.__info_prefix + Formatter.green(''.join(map(str, message)))

    @ output
    def debug(self, *message, flush=False) -> None:
        if self.__mute_debug:
            return

        return self.__debug_prefix + Formatter.blue(''.join(map(str, message)))

    @ output
    def warning(self, *message, flush=False) -> None:
        if self.__mute_warning:
            return

        return self.__warning_prefix + Formatter.yellow(''.join(map(str, message)))

    @ output
    def error(self, *message, flush=False) -> None:
        if self.__mute_error:
            return

        return self.__error_prefix + Formatter.red(''.join(map(str, message)))

    def mute(self, *level) -> None:
        if ("info" in level) or ("all" in level):
            self.__mute_info = True
        if ("debug" in level) or ("all" in level):
            self.__mute_debug = True
        if ("warning" in level) or ("all" in level):
            self.__mute_warning = True
        if ("error" in level) or ("all" in level):
            self.__mute_error = True
