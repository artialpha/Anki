from . import sense
import itertools

__all__ = [
    'sense'
]

class LexicalEntry:
    def __init__(self, results):
        #x = [[sense.Sense(x["definitions"][0], example['text']) for example in x["examples"]] for x in senses]
        self.results = results["results"]
        y = []
        for r in self.results:
            for entry in r["lexicalEntries"]:
                for sen in entry["entries"][0]["senses"]:
                    if 'examples' in sen:
                        y.append([sense.Sense(sen["definitions"][0], example['text'], results['id']) for example in sen["examples"]])
                        if "subsenses" in sen:
                            for sub in sen["subsenses"]:
                                if 'examples' in sub:
                                    y.append([sense.Sense(sub["definitions"][0], ex['text'], results['id']) for ex in sub["examples"]])
                    else:
                        y.append([sense.Sense(sen["definitions"][0], '', results['id'])])
                        if "subsenses" in sen:
                            for sub in sen["subsenses"]:
                                y.append([sense.Sense(sub["definitions"][0], '', results['id'])])
        self.senses = list(itertools.chain.from_iterable(y))

    def entry_content(self):
        content = ""
        for count, value in enumerate(self.senses, 1):
            content += '<div>' + str(count) + " " + '<b>' + value.word + '</b>' + '<div>' + value.sense_content() + '<div>'
            content += '<hr>'
        return content

    def entry_content_ent(self):
        content = ""
        for count, value in enumerate(self.senses, 1):
            content += '\n' + str(count) + '\n' + value.sense_content() + '\n'
        return content

    def phrasal_verbs(self):
        return [[x['id'], self.results[0]['id']] for x in self.results[0]['lexicalEntries'][0]['phrasalVerbs']]

