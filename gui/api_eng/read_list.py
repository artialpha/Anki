
class ReadList:
    def __init__(self, filename):
        self.filename = filename

    def list_of_words(self):
        with open(self.filename) as f:
            content = f.readlines()
            content = [x.strip().split() for x in content]
            return content
