import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import yake
#Keywords and text summarisation
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import operator
text = """
"We were so looking forward to Malaika Arora's post on International Yoga Day. Malaika, who has been practicing yoga for years now, shared a post, which had a compilation of some of her pictures and videos from her yoga sessions. In the video, the 47-year-old talks about her passion for yoga and stated that it is a \"way of life\" for her. She says in the video: \"For me yoga is not about working out, getting ripped or getting the right kind of body or body shape or whatever. For me it is a way of life. Aur agar aap apni zindagi mein isey ek hissa bana doge then I don't think you will ever think that yoga is boring. I think just make it a way of life and I think that's how you should live.\"\n\nMalaika Arora, who describes herself as a \"yogi\" on her Instagram bio, captioned the video: \"Namaste everybody! For me, it's yoga day every day because yoga is a way of life as it has taught me so much more than I can pen down here. However, let me take this opportunity and wish all of you'll a happy International Day Of Yoga.\"\n\nCheck out the video shared by Malaika Arora here:\n\nMalaika Arora takes her yoga sessions very seriously, be it aerial or even by the pool. See some of her posts here:\n\nMalaika Arora was seen as one of the judges on the TV reality show India's Best Dancer, alongside choreographers Geeta Kapoor and Terence Lewis. She is best-known for her dance performances to songs such as Chaiya Chaiya, Munni Badnaam Hui, Anarkali Disco Chali and Hello Hello among many others. Last year, she also featured as one of the judges on Supermodel Of The Year, alongside Milind Soman and Masaba Gupta
"""



keywords = []
stemmer = SnowballStemmer("english")
stopWords = set(stopwords.words("english"))
words = word_tokenize(text)
words=[word.lower() for word in words if word.isalpha()]
freqTable = dict()
for word in words:
    word = word.lower()
    if word in stopWords:
        continue
    word = stemmer.stem(word)
    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1

sorted_d = dict(sorted(freqTable.items(), key=operator.itemgetter(1),reverse=True))
first_key = list(sorted_d.values())[0]
for k,v in sorted_d.items():
    sorted_d[k] = int(v)/first_key
for k,v in sorted_d.items():
    if v >= 0.32:
        keywords.append(k)


kw_extractor = yake.KeywordExtractor()
language = "en"
max_ngram_size = 2
deduplication_threshold = 0.2
numOfKeywords = 5
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
keywords = custom_kw_extractor.extract_keywords(text)
print(keywords)