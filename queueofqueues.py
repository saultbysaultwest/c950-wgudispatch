
class QueueOfQueues:
    def __init__(self, name):
        self._queues = []  # A private list to store delivery queues
        self.name = name

    # add a new queue to the list
    def add_queue(self, queue):
        print("Adding", queue.name, "DeliveryQueue to", self.name, "QueueOfQueue")
        self._queues.append(queue)
        # print(f"Queue added. Total queues now: {len(self._queues)}.")

    # get next queue in list, returns None if no more
    def get_queue(self):
        if self._queues:
            queue = self._queues.pop(0)  # pop both retrieves and removes
            # print(f"Queue retrieved and removed. Queues remaining: {len(self._queues)}.")
            return queue
        else:
            # print("No more queues to retrieve.")
            return None
    
    # I can haz queue?
    def has_queue(self):
        if len(self._queues) > 0:
            return len(self._queues)
        else:
            return None
        
