import copy

class Context:
    def __init__(self):
        super(Context, self).__init__()

    def with_app(self, app):
        new = copy.copy(self)
        new.app = app
        return new