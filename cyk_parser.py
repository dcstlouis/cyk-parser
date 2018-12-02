from collections import OrderedDict
import itertools

class CYKParser:

    def __init__(self, grammar_file):
        self.grammar = self.import_grammar(grammar_file)
        self.reverse_grammar = self.generate_reverse_grammar()

    def import_grammar(self, grammar_file):
        grammar = OrderedDict()
        with open(grammar_file, 'r', encoding='utf-8') as f:
            for production in f:
                p = production.replace('\n', "").split('->')
                variable = p[0].strip()
                symbols = p[1].strip()
                try:
                    grammar[variable].append(symbols)
                except KeyError:
                    grammar[variable] = [symbols]
        return grammar

    def generate_reverse_grammar(self):
        """Creates a grammar to look up variables from terminals"""
        reverse_grammar = OrderedDict()
        for key in self.grammar.keys():
            symbols = self.grammar[key]
            for symbol in symbols:
                try:
                    reverse_grammar[symbol].add(key)
                except KeyError:
                    reverse_grammar[symbol] = set([key]) # avoid duplicates
        return reverse_grammar

    def lookup_symbol(self, symbol):
        """
        if symbol can be produced by a set of terminals or variables
        in the grammar, then return that set. else return an empty set
        """
        try:
            s = self.reverse_grammar[symbol]
            return s
        except KeyError:
            return set()

    def in_grammar(self, s):
        """Uses the CYK algorithm to determine whether s is a valid string"""
        print(s)
        sentence = s
        sentence = s.split()
        n = len(sentence)

        # Start by filling table with empty sets
        table = [[set() for w in sentence] for w in sentence]

        # Fill bottom of table
        for i, w in enumerate(sentence):
            table[0][i] = self.lookup_symbol(w)

        # Now use CYK algorithm to fill in the rest of the table
        for row in range(1, n):
            for col in range(n - row):
                for t in range(row):
                    try:
                        a = table[t][col]
                        b = table[row-t-1][col+1]
                        pairs = itertools.product(a,b) # cartesian product
                        for p in pairs:
                            symbol = "".join(p)
                            symbol_set = self.lookup_symbol(symbol)
                            union = table[row][col].union(symbol_set)
                            table[row][col] = union
                    except IndexError as e:
                        print(e)
                        pass
        return(table[n-1][0])


if __name__ == '__main__':
    parser = CYKParser('grammars/cit596/english.txt')
    result = parser.in_grammar("fish swim in streams")
    print('S' in result)
