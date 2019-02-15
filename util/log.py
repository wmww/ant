import enum
import sys
from util import color_code

class Type(enum.Enum):
    BORING = 1
    YIKES = 2
    ARGH = 3

class Logger:
    """
    Log messages and errors

    self.context should be set to None or the object that uses this logger
    """
    def __init__(self):
        self.context = None

    def log(self, context, log_type, message):
        """
        log a message

        context: the object that created the message
        log_type: the log.Type of the message
        message: the message string
        """
        raise NotImplementedError

    def boring(self, *msg):
        self.log(self.context, Type.BORING, ' '.join(map(lambda m: str(m), msg)))

    def yikes(self, *msg):
        self.log(self.context, Type.YIKES, ' '.join(map(lambda m: str(m), msg)))

    def argh(self, *msg):
        self.log(self.context, Type.ARGH, ' '.join(map(lambda m: str(m), msg)))

class StreamLogger(Logger):
    def __init__(self, context, use_color=None):
        self.context = context
        if use_color is None:
            use_color = color_code.stdout_is_tty()
        if use_color:
            self.color = color_code.color
        else:
            def noop(c, arg):
                return arg
            self.color = noop
        self.out = sys.stdout
        self.err = sys.stderr

    def log(self, context, log_type, message):
        assert isinstance(message, str)
        if log_type == Type.BORING:
            type_str = 'Boring'
            clr = '36'
            out_file = self.out
        elif log_type == Type.YIKES:
            type_str = 'Yikes'
            clr = '1;33'
            out_file = self.err
        elif log_type == Type.ARGH:
            type_str = 'Argh'
            clr = '1;31'
            out_file = self.err
        else:
            raise AssertionError('Bat log_type value ' + repr(log_type))
        if context != None:
            context_str = self.color('1;34', ' [' + type(context).__name__ + ']')
        else:
            context_str = ''
        print(self.color(clr, type_str) + context_str + ': ' + message, file=out_file)
