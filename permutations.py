# -*- coding: utf-8 -*-

''' Symbols for adding to end of password '''
SYMBOLS = ["~", "!", "@", "#$", '.?', "-", "1"]

class CapitalizeIterator:
    def __init__(self, dict_iter):
        self.dict_iter = dict_iter
        self.word = None

    def __iter__(self):
        return self

    def next(self):
    	if self.word is None:
    		ret = self.dict_iter.next()
    		self.word = ret
    	else:
    		ret, self.word = self.word.capitalize(), None
    	return ret

class SymbolsIterator:
    def __init__(self, dict_iter, symbols):
        self.dict_iter = dict_iter
        self.word = None
        self.length = len(symbols)
        self.symbols = symbols
        self.i = 0

    def __iter__(self):
        return self

    def next(self):
    	if self.word is None or self.i >= self.length:
    		ret = self.dict_iter.next()
    		self.word = ret
    		self.i = 0
    	else:
    		ret = self.word + self.symbols[self.i]
    		self.i += 1
    	return ret


def capitalize(fn):
    def wrapped(*args, **kwargs):
        return CapitalizeIterator(fn(*args, **kwargs))
    return wrapped

def add_symbols(fn):
    def wrapped(*args, **kwargs):
        return SymbolsIterator(fn(*args, **kwargs), SYMBOLS)
    return wrapped

