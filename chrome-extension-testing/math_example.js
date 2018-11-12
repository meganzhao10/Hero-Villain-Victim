
var __name__ = "__main__";
function sent_tokenize(text, language) {
    language = language === void 0 ? "english" : language;
    var tokenizer;
    tokenizer = load("tokenizers/punkt/{0}.pickle".format(language));
    return tokenizer.tokenize(text);
}