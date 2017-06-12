import re


def rm_At(_s):
    return re.sub(r'@.+?\u2005', '', _s)


def get_ints(_s):
    return [int(s) for s in _s.split() if s.isdigit()]


def retrieve_At(_s):
    return re.search(r'@.+?\u2005', _s).group(0)
    # return _s.split('@')[1].split('\u2005')[0]
