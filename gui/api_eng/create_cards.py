from . import api as api
from . import lexical_entry as entry
from . import group_entries as group
import io
import re
from . import pyinflect
import itertools

__all__ = [
    'api', 'entry', 'group', 'pyinflect'
]


class CreateCards:
    def __init__(self, app_id, app_key, endpoint, language_code):
        self.api = api.Api(app_id, app_key, endpoint, language_code)

    def multiple_cards(self, words, path):
        errors = []
        text = ''
        for x in words:
            result = self.one_card(x, path)
            if result:
                errors.append((result))
        if errors:
            for er in errors:
                text += er + '\n'
            return text

    def create_phrasals(self, word, path):
        result = self.api.word_json(word[0][0])
        list_phrasals = entry.LexicalEntry(result).phrasal_verbs()
        if not isinstance(list_phrasals, str):
            self.multiple_cards(list_phrasals, path)
        else:
            return list_phrasals

    def create_phrases(self, word, path):
        result = self.api.word_json(word[0][0])
        list_phrases = entry.LexicalEntry(result).phrases()
        if not isinstance(list_phrases, str):
            self.multiple_cards(entry.LexicalEntry(result).phrases(), path)
        else:
            return list_phrases

    def create_abcd(self, words_string, path):
        no_result = ''
        words = words_string.split('/')
        results = [self.api.word_json(word) for word in words]
        entries = [entry.LexicalEntry(r).create_senses() for r in results]

        for ent in entries:
            if ent.no_result:
                no_result += ent.no_result + '\n'

        senses = [ent.senses for ent in entries]
        senses = [item for sublist in senses for item in sublist]   #flat_list
        all_senses = ''
        for ent in entries:
            all_senses += ent.entry_content().content

        for sense in senses:
            self.write_to_file_card(
                senwe=self.delete_inflected_word([sense.word], sense.example) if sense.example else 'no example;',
                question_line=words_string+";",
                sentence_embolden=CreateCards.embolden([sense.word], sense.example) + ";" if sense.example else 'no example;',
                words=sense.word+";",
                definition=sense.definition + ";",
                ipa=sense.ipa + ";",
                all_senses=CreateCards.embolden([sense.word], all_senses) + "\n",
                path_file=path
            )

        return no_result

    def one_card(self, word, path):
        result = self.api.word_json(word[0])

        if not isinstance(result, str) and len(word) > 1:
            entries = entry.LexicalEntry(result)
            entries.create_senses()

            if '_' in word[0]:
                word_to_delete = word[0].split('_')[1:]
            else:
                word_to_delete = [word[0]]
            for sense in entries.senses:
                self.write_to_file_card(
                    senwe=self.delete_inflected_word(word_to_delete, sense.example) if sense.example else "no example;",
                    question_line=self.question_line(word),
                    sentence_embolden=CreateCards.embolden(word_to_delete, sense.example) + ";" if sense.example else "no example;",
                    words=word[1]+";",
                    definition=sense.definition + ";",
                    ipa=sense.ipa + ";",
                    all_senses=CreateCards.embolden(word_to_delete, entries.entry_content().content) + "\n",
                    path_file=path
                )
        else:
            return result

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
    def inflected_word_list(words):
        inflected = [[x[0] for x in list(pyinflect.getAllInflections(w).values())] for w in words]
        inflected = list(itertools.chain(*inflected))
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
        text = ''
        no_result = ''

        results = [self.api.word_json(word) for word in list_of_words]
        entries = [entry.LexicalEntry(result) for result in results]

        entries = [ent.create_senses() for ent in entries]
        entries_text = [ent.entry_content().content for ent in entries]

        for ent in entries:
            if ent.no_result:
                no_result += ent.no_result + '\n'

        for e in entries_text:
            text += e
        return {'text': text, 'message': no_result}

    def get_phrases(self, list_of_words):
        results = [self.api.word_json(word) for word in list_of_words]
        entries = [entry.LexicalEntry(result).phrases() for result in results]
        text = ''

        for e in entries:
            if not isinstance(e, str):
                for phrase in e:
                    text += '<div>' + phrase[0] + '</div>'
                    text += '<hr>'
            else:
                text += '<div>' + e + '</div>'
        return {'text': text, 'message': 'there are no phrases for this entry'}


