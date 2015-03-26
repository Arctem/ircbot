def parsemsg(s):
    """ via http://stackoverflow.com/questions/930700/python-parsing-irc-messages """
    s = s.strip()
    prefix = ''
    trailing = []
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)

    return prefix, command, args