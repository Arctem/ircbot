from circuits import Event

class sendmessage(Event):
    """Send a PRIVMSG to the server."""

class command(Event):
    """Someone called a specific command."""

class directmessage(Event):
    """Someone addressed our bot directly."""

class generalmessage(Event):
    """Someone said something that was not a command or DM."""

class enablehelp(Event):
    """Let the help module know you exist."""

class debugout(Event):
    """Print normal debug output to console."""

class debugalert(Event):
    """Print some kind of alert to console."""
