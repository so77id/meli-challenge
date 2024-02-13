from collections import deque
from concurrent.futures import Future

class PredictionQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, data):
        future = Future()
        self.queue.append((data, future))
        return future

    def dequeue(self):
        return self.queue.popleft()

    def is_empty(self):
        return len(self.queue) == 0
