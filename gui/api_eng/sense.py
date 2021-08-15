from .eng_to_ipa import transcribe as ipa

__all__ = [
    'ipa'
]


class Sense:
    def __init__(self, definition, example, word):
        self.word = word
        self.definition = definition + '<div>' + ipa.convert(definition) + '<div>'
        self.definition = self.definition.replace(";", ",")
        self.example = example
        self.example = self.example.replace(";", ",")
        self.ipa = ipa.convert(example)

    def sense_content(self):
        return '<div>' + self.definition + '<div>' + self.example + '<div>' + self.ipa

    @staticmethod
    def embolden(word, text):
        l_word = len(word)
        position_word_start = text.find(word)
        position_word_end = position_word_start + l_word
        text = text[:position_word_start] + "<b>" + word + "</b>" + text[position_word_end:]
        return text
