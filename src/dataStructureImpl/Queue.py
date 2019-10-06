class Queue:
    max_size = 0
    q = []
    tail_pos = -1

    def __init__(self, init_size):
        self.max_size = init_size
        self.q = [None] * init_size

    def size(self):
        return self.tail_pos + 1

    def put(self, item):
        if self.tail_pos < self.max_size - 1:
            self.tail_pos += 1
            self.q[self.tail_pos] = item
        else:
            raise OverflowError

    def remove(self):
        if self.tail_pos > -1:
            item = self.q[0]
            self.q[0] = None
            new_q = [None] * (self.max_size - 1)
            index = 0
            for i in self.q:
                if i is not None:
                    new_q[index] = i
                    index += 1
            self.q = new_q
            self.tail_pos -= 1
            return item
        else:
            raise EOFError

    def poll(self):
        try:
            item = self.remove()
            return item
        except EOFError:
            return None

    def peek(self):
        if self.tail_pos < 0:
            return None
        else:
            return self.q[0]

    def pretty_print(self):
        print('Pretty Printing queue with size...')
        print(self.size())
        print('-----------------------------------')
        for item in self.q:
            print(item)


if __name__ == '__main__':
    queue = Queue(6)
    print(queue.size())
    queue.put('A')
    queue.put('B')
    queue.put('C')
    queue.put('D')
    queue.put('E')
    queue.put('F')
    # queue.put('G')
    queue.pretty_print()
    queue.remove()
    queue.pretty_print()
    queue.peek()
    queue.pretty_print()
    queue.poll()
    queue.poll()
    queue.poll()
    queue.poll()
    queue.poll()
    queue.poll()  # This will not raise an exception when the queue is empty
    queue.pretty_print()

