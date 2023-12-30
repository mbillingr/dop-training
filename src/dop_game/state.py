from validity import validate


class GameState:
    def __init__(self):
        self.state = None
        self.history = []

    def get(self):
        return self.state

    def commit(self, previous, new_state):
        if not validate(previous, new_state):
            raise RuntimeError("invalid state")
        self.history.append(self.state)
        self.state = new_state
