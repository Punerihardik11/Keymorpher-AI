class TypedText:
    def __init__(self):
        self.content = ""

    def append_text(self, char):
        self.content += char

    def delete_text(self):
        self.content = self.content[:-1]

    def get_text(self):
        return self.content
