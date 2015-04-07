def isMatch(s, p):
    import re
    pattern = re.compile("^" + p + "$")
    if pattern.search(s) is None:
        return False
    return True
