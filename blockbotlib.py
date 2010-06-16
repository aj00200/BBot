def dec2hex(n):
    return "%X" % n
def hex2dec(s):
    try:
        return int(s, 16)
    except:
        return 'error'