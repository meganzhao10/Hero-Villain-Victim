def sent_tokenize(text, language='english'):
    tokenizer = load('tokenizers/punkt/{0}.pickle'.format(language))
    return tokenizer.tokenize(text)


class TokenizerI(object):
    def tokenize(self, s):
        if overridden(self.tokenize_sents):
            return self.tokenize_sents([s])[0]
