from validity import validate
import generics as _


class GameState:
    def __init__(self):
        self.state = None
        self.history = []

    def get(self):
        return self.state

    def commit(self, previous, new_state):
        actual_new_state = reconcile(self.state, previous, new_state)
        if not validate(previous, actual_new_state):
            raise RuntimeError("invalid state")
        self.history.append(self.state)
        self.state = actual_new_state


def reconcile(current, previous, new):
    if current is previous:
        return new
    return three_way_merge(current, previous, new)


def three_way_merge(current, previous, new):
    prev_to_cur = _.diff(previous, current)
    prev_to_new = _.diff(previous, new)
    if _.have_paths_in_common(prev_to_cur, prev_to_new):
        raise ConflictError("Conflicting concurrent mutations")
    return _.merge(current, prev_to_new)


class ConflictError(Exception):
    pass
