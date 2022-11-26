import csv

class WordDifficulty:
    def __init__(self):
        self.table = {}
        with open('cefr.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                score = {'A1':1, 'A2':2, 'B1':3, 'B2':4 }
                if not row[0] in self.table or score[row[2]] < score[self.table[row[0]]]:  # 簡単なほうを採用する
                    self.table[row[0]] = row[2]

    def getDifficulty(self, word):
        if word in self.table:
            return self.table[word]
        else:
            return "unknown"


if __name__ == '__main__':
    import pprint

    pp = pprint.PrettyPrinter(indent=4)

    df = WordDifficulty()
    result = list( map( df.getDifficulty, ["I", "love", "you", "constant"]) )
    pp.pprint( result )
