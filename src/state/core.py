import logging
from collections import deque

class StateManager(object):
    def __init__(self):
        import queue
        self.current_state = None
        self._timeline = deque()
        self.stores = queue.PriorityQueue()
        self.logger = logging.getLogger()

    def dispatch(self, action):
        if isinstance(action, dict):
            # Executes all possible stores
            for _, store in self.stores.queue:
                # Inserts action as a past event on a list
                self._timeline.append((self.current_state, action))
                self.current_state = store(self.current_state, action)
        else:
            self.logger.warning("[STATE] Action must be a dictionary. Ignoring dispatch...")

    def create_store(self, *args, **kwargs):
        for a in args:
            self._insert_store(a)
        for _, a in kwargs.items():
            self._insert_store(a)

    def _insert_store(self, store):
        import inspect
        if inspect.isfunction(store):
            self.stores.put((1, store))
        elif isinstance(store, tuple) and len(store) >= 2:
            if isinstance(store[0], int) and inspect.isfunction(store[1]):
                self.stores.put((store[0], store[1]))
            else:
                self.logger.warning("[STATE] Expects store to be a tuple (<priority:Int>, <store_func:Callable>)")
        else:
            self.logger.warning("[STATE] Invalid store for PyTEA. Must be a function or callable object")
