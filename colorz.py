open = '\x1B['
close = open+'m'
colors = {
    'red':'31;40m', 
    'green':'32;40m', 
    'white':'37;40m', 
    'blue':'34;40m', 
    'magenta':'35;40m', 
    'cayn':'36;40m', 
    'yellow':'33;40m'
}
def encode(text, color, ):
    if color in colors:
        return open+colors[color]+text+open+'m'+close
    else:
        raise ColorError('Color %s does not exist'%color)
class ColorError(Exception):
    def __init__(self, msg):
        self.args.append(msg)
