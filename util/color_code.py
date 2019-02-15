import re
import sys

reset_code = '\x1b[0m'

def stdout_is_tty():
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

# if string is not None, resets to normal at end
def color(code, string):
    if string == '':
        return ''
    if code:
        result = '\x1b[' + code + 'm'
    else:
        result = reset_code
    if string:
        result += string
        if code:
            result += reset_code
    return result

def remove(string):
    return re.sub('\x1b\[[\d;]*m', '', string)
