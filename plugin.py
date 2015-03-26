class IRCPlugin:
    """A plugin is an IRCBot module that will respond to specific events inside
    of received PRIVMSGs.
    """

    def __init__(self):
        self.owner = None

    def set_owner(self, owner):
        self.owner = owner

    def trigger(self, args):
        return False

    def run(self, args):
        pass