class Word:
    def __init__(self, dict):
        self.word = dict['word']
        self.meaning = dict['meaning']
        self.hint = dict['hint']
        self.wrongtimes = dict['wrongtimes']
        self.memorized = dict['memorized']
        self.starred = dict['starred']

    def __str__(self):
        return self.word

    def __lt__(self, other):
        return self.word < other.word
    def __le__(self, other):
        return self.word <= other.word
    def __gt__(self, other):
        return self.word > other.word
    def __ge__(self, other):
        return self.word >= other.word

    def get_right(self):
        if self.wrongtimes > 0:
            self.wrongtimes -= 1

    def get_wrong(self):
        if self.wrongtimes < 5:
            self.wrongtimes += 1