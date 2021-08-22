from . import api as api
from . import lexical_entry as entry
from . import group_entries as group
import io
import re
from . import pyinflect

__all__ = [
    'api', 'entry', 'group', 'pyinflect'
]


class CreateCards:
    def __init__(self, app_id, app_key, endpoint, language_code):
        self.api = api.Api(app_id, app_key, endpoint, language_code)

    def multiple_cards(self, words, path):
        for x in words:
            self.one_card(x, path)

    def create_phrasals(self, word, path):
        result = self.api.word_json(word[0][0])
        self.multiple_cards(entry.LexicalEntry(result).phrasal_verbs(), path)

    def create_phrases(self, word):
        result = self.api.word_json(word[0][0])
        self.multiple_cards(entry.LexicalEntry(result).phrases())

    def create_abcd(self, words_string, path):
        words = words_string.split('/')
        results = [self.api.word_json(word) for word in words]
        entries = [entry.LexicalEntry(r) for r in results]
        senses = [ent.senses for ent in entries]
        senses = [item for sublist in senses for item in sublist]   #flat_list
        all_senses = ''
        for ent in entries:
            all_senses += ent.entry_content()

        for sense in senses:
            self.write_to_file_card(
                senwe=self.delete_inflected_word(sense.word, sense.example) if sense.example else 'no example;',
                question_line=words_string+";",
                sentence_embolden=CreateCards.embolden(sense.word, sense.example) + ";" if sense.example else 'no example;',
                words=sense.word+";",
                definition=sense.definition + ";",
                ipa=sense.ipa + ";",
                all_senses=CreateCards.embolden(sense.word, all_senses) + "\n",
                path_file=path
            )


    def one_card(self, word, path):
        result = self.api.word_json(word[0])

        entries = entry.LexicalEntry(result)
        for x in entries.senses:
            print(x.sense_content())

        if '_' in word[0]:
            word_to_delete = word[0].split('_')[1]
        else:
            word_to_delete = word[0]
        for sense in entries.senses:
            self.write_to_file_card(
                senwe=self.delete_inflected_word(word_to_delete, sense.example) if sense.example else "no example;",
                question_line=self.question_line(word),
                sentence_embolden=CreateCards.embolden(word[0], sense.example) + ";" if sense.example else "no example;",
                words=word[1]+";",
                definition=sense.definition + ";",
                ipa=sense.ipa + ";",
                all_senses=CreateCards.embolden(word[0], entries.entry_content()) + "\n",
                path_file=path
            )

    @staticmethod
    def write_to_file_card(senwe, question_line, sentence_embolden, words, definition, ipa, all_senses, path_file):
        with io.open(path_file, "a+", encoding="utf-8") as file_object:
            file_object.write(senwe)
            file_object.write(question_line)
            file_object.write(sentence_embolden)
            file_object.write(words)
            file_object.write(definition)
            file_object.write(ipa)
            file_object.write(all_senses)

    @staticmethod
    def delete_inflected_word(word, to_write):
        inf = CreateCards.inflected_word_list(word)
        if not inf:
            inf = [word]

        to_write = ' '.join(i if i not in inf else "..." for i in re.findall(r"[\w']+|[.,!?;]", to_write))
        to_write += ";"
        return to_write

    @staticmethod
    def inflected_word_list(word):
        inflected = [x[0] for x in list(pyinflect.getAllInflections(word).values())]
        inflected.extend([x.capitalize() for x in inflected])
        return list(set(inflected))

    @staticmethod
    def question_line(word):
        if word[1] == 'X':
            return "...;"
        else:
            return word[1]+";"

    @staticmethod
    def embolden(word, text):
        inflected = CreateCards.inflected_word_list(word)
        positions = []
        for inf in inflected:
            positions.extend([(a.start(), a.end()) for a in list(re.finditer(inf, text))])
        positions.sort(reverse=True)
        for pos in positions:
            text = text[:pos[0]] + "<b>" + text[pos[0]:pos[1]] + "</b>" + text[pos[1]:]
        return text

    def get_definitions(self, list_of_words):
        results = [self.api.word_json(word) for word in list_of_words]
        entries = [entry.LexicalEntry(result).entry_content() for result in results]
        text = ''
        for e in entries:
            text += e
        return text


