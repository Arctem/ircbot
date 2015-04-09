class IRCPlugin:
    """A plugin is an IRCBot module that will respond to specific events inside
    of received PRIVMSGs.
    """

    def __init__(self):
        self.owner = None
        self.triggers = {}

    def set_owner(self, owner):
        self.owner = owner

    def run(self, args):
        pass

    def name(self):
        return None

    def description(self):
        return None