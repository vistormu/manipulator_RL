class _Formatter:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'

    @classmethod
    def bold(cls, message: str) -> str:
        return cls.BOLD + message + cls.END

    @classmethod
    def green(cls, message: str) -> str:
        return cls.GREEN + message + cls.END

    @classmethod
    def blue(cls, message: str) -> str:
        return cls.BLUE + message + cls.END

    @classmethod
    def yellow(cls, message: str) -> str:
        return cls.YELLOW + message + cls.END

    @classmethod
    def red(cls, message: str) -> str:
        return cls.RED + message + cls.END


def output(function):

    def wrapper(*args, **kwargs):
        return_value = function(*args, **kwargs)
        if kwargs.get('flush'):
            # print('\r' + return_value, end='\r', **kwargs)
            print(return_value)
            print(_Formatter.LINE_UP, end=_Formatter.LINE_CLEAR)
        else:
            print(return_value, **kwargs)

    return wrapper


class Logger(_Formatter):

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__mute_info = False
        self.__mute_debug = False
        self.__mute_warning = False
        self.__mute_error = False

    @ output
    def info(self, *message, flush=False, **kwargs) -> None:
        if self.__mute_info:
            return

        name = super().bold('[' + self.__name + ']')
        name = super().green(name)
        level = super().green('[INFO]')
        message = ''.join(map(str, message))
        message = super().green(message)

        return name + level + ' ' + message

    @ output
    def debug(self, *message, flush=False, **kwargs) -> None:
        if self.__mute_debug:
            return

        name = super().bold('[' + self.__name + ']')
        name = super().blue(name)
        level = super().blue('[DEBUG]')
        message = ''.join(map(str, message))
        message = super().blue(message)

        return name + level + ' ' + message

    @ output
    def warning(self, *message, flush=False, **kwargs) -> None:
        if self.__mute_warning:
            return

        name = super().bold('[' + self.__name + ']')
        name = super().yellow(name)
        level = super().yellow('[WARNING]')
        message = ''.join(map(str, message))
        message = super().yellow(message)

        return name + level + ' ' + message

    @ output
    def error(self, *message, flush=False, **kwargs) -> None:
        if self.__mute_error:
            return

        name = super().bold('[' + self.__name + ']')
        name = super().red(name)
        level = super().red('[ERROR]')
        message = ''.join(map(str, message))
        message = super().red(message)

        return name + level + ' ' + message

    def mute(self, *level) -> None:
        if ("info" in level) or ("all" in level):
            self.__mute_info = True
        if ("debug" in level) or ("all" in level):
            self.__mute_debug = True
        if ("warning" in level) or ("all" in level):
            self.__mute_warning = True
        if ("error" in level) or ("all" in level):
            self.__mute_error = True

    def init(self) -> None:
        self.info('logger initialized')
