import spacy
from nltk.corpus import stopwords
from string import punctuation
import heapq

nlp=spacy.load("en_core_web_md")
stopwords_list=stopwords.words('english')

#Removing Whitespaces and newlines

def white_spaces(data):
    import re 
    returned_text = re.sub(r'\s+'," ",data)
    return returned_text


def text_summarizer(text):
    text=white_spaces(text)
    doc=nlp(text)
    words=[word.text.lower() for word in doc if (word.text.lower() not in stopwords_list) and (word.text.lower() not in punctuation)]

    word_frequencies={}
    for word in words:
        if word not in word_frequencies:
            word_frequencies[word]=1
        else:
            word_frequencies[word]+=1
            
    max_freq=max(word_frequencies.values())
    for key in word_frequencies:
        word_frequencies[key]= word_frequencies[key]/max_freq
        
    sentence_score={}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_score:
                    sentence_score[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_score[sent]+=word_frequencies[word.text.lower()]
    number_of_sentences=int(len(list(doc.sents))*.3)
    sentence_list=heapq.nlargest(number_of_sentences,sentence_score,key=sentence_score.get)
    text_data=[str(data) for data in sentence_list ]
    return " ".join(text_data)


text_summarizer("Hi")