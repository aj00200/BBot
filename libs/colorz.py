c_open = '\x1B['
close = c_open + 'm'
colors = {
    # fg only
    'red':';31m',
    'green':';32m',
    'white':';37m',
    'blue':';34m',

    # fg and bg
    'redblack':'31;40m',
    'greenblack':'32;40m',
    'whiteblack':'37;40m',
    'blueblack':'34;40m',
    'magenta':'35;40m',
    'cayn':'36;40m',
    'yellow':'33;40m'

}
def encode(text, color):
    '''Convert text to a color for terminal printing'''
    if color in colors:
        return c_open + colors[color] + text + c_open + 'm' + close
    else:
        raise ColorError('Color %s does not exist' % color)

class ColorError(Exception):
    def __init__(self, msg):
        self.args.append(msg)
