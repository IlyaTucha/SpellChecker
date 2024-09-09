class Entry:
    def __init__(self, word) -> None:
        self.distance = None
        self.word = word
    
    def __repr__(self) -> str:
        return f'Entry({self.__dict__})'
