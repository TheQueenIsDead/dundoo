class Command(object):

    # Type hint with forward reference
    # https://www.python.org/dev/peps/pep-0484/#forward-references
    def __init__(self, previous: 'Command' = None, next: 'Command' = None):
        self.previous = previous
        self.next = next

        # link nodes appropriately
        if self.previous:
            self.previous.set_next(self)
        if self.next:
            self.next.set_previous(self)

    def __str__(self):
        return f"{self.__class__} - Previous: {self.previous.__class__} Next: {self.next.__class__}"

    def set_action(self, action):
        self.__do__ = action

    def run(self) -> None:
        # Should catch any and all Exceptions thrown by custom command classes
        # noinspection PyBroadException
        try:
            self.__do__()
            if self.next:
                self.next.run()
        except Exception:
            self.rollback()

    def rollback(self) -> None:
        self.__undo__()
        if self.previous:
            self.previous.rollback()

    def set_next(self, next: 'Command') -> 'Command':
        self.next = next
        self.next.previous = self
        return self.next

    def set_previous(self, previous: 'Command') -> 'Command':
        self.previous = previous
        self.previous.next = self
        return self.previous

    def get_next(self) -> 'Command':
        return self.next

    def get_previous(self) -> 'Command':
        return self.previous

    def find_head(self) -> 'Command':
        if self.previous:
            return self.previous.find_head()
        return self

    def print_walk(self) -> None:
        print(self)
        if self.next:
            self.next.print_walk()

    def __do__(self) -> None:
        pass

    def __undo__(self) -> None:
        pass
