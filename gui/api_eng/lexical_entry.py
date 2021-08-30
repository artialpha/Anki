from . import sense
import itertools
from urllib.parse import unquote
from .eng_to_ipa import transcribe as ipa

__all__ = [
    'sense'
]


class LexicalEntry:
    def __init__(self, results):
        #x = [[sense.Sense(x["definitions"][0], example['text']) for example in x["examples"]] for x in senses]
        self.results = results
        self.senses = []
        self.create_senses()

    def create_senses(self):
        y = []
        for r in self.results["results"]:
            for entry in r["lexicalEntries"]:
                for sen in entry["entries"][0]["senses"]:
                    if 'examples' in sen and 'definitions' in sen:
                        y.append([sense.Sense(sen["definitions"][0], example['text'], unquote(self.results['id'])) for
                                  example in sen["examples"]])
                        if "subsenses" in sen:
                            for sub in sen["subsenses"]:
                                if 'examples' in sub:
                                    y.append([sense.Sense(sub["definitions"][0], ex['text'],
                                                          unquote(self.results['id'])) for ex in sub["examples"]])
                    else:
                        if 'definitions' in sen:
                            y.append([sense.Sense(sen["definitions"][0], '', unquote(self.results['id']))])
                            if "subsenses" in sen:
                                for sub in sen["subsenses"]:
                                    if 'definitions' in sub:
                                        y.append([sense.Sense(sub["definitions"][0], '', unquote(self.results['id']))])
        self.senses = list(itertools.chain.from_iterable(y))

    def entry_content(self):
        content = ""
        for count, value in enumerate(self.senses, 1):
            content += '<div>' + str(count) + " " + '<b>' + unquote(value.word) + ' ' \
                       + ipa.convert(value.word.replace('_', ' ')) + '</b>' + '<div>' + value.sense_content() + '<div> '
            content += '<hr>'
        return content

    def entry_content_ent(self):
        content = ""
        for count, value in enumerate(self.senses, 1):
            content += '\n' + str(count) + '\n' + value.sense_content() + '\n'
        return content

    def phrasal_verbs(self):
        return [[x['id'], self.results['id']] for x in self.results["results"][0]['lexicalEntries'][0]['phrasalVerbs']]

    def phrases(self):
        return [[unquote(lxe['id']), self.results['id']] for lxe in self.results["results"][0]['lexicalEntries'][0]['phrases']]

