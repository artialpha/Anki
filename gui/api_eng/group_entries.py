

class GroupEntries:
    def __init__(self, file_name):
        self.file_name = file_name
        self.group = []

    def create_group(self):
        with open(self.file_name) as f:
            content = f.readlines()
        self.group = [x.strip().split() for x in content]
        #print(self.group)