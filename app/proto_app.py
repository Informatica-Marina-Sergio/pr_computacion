import tkinter as tk
from tkinter import *
import pickle
import numpy as np
import spacy
import nltk
import re
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
import collections
from collections import Counter
import joblib
pd.set_option("display.max_rows", None, "display.max_columns", None)

class BagOfWords(BaseEstimator, TransformerMixin):
    def __init__(self, min_frequency=1, clip_counts=False, use_tfidf=False):
        self.min_frequency = min_frequency # to reduce our total vocabulary size, we only keep words that appear at least n times
        self.clip_counts = clip_counts # clip the counts to a maximum of 1 (is the word present or not)
        self.use_tfidf = use_tfidf
        
        
    def fit(self, X, y=None):
        
        self.keep_columns = None
        self.vectorizer = DictVectorizer(dtype=np.int64)
        self.tfidf_transformer = None
        if self.use_tfidf:
            self.tfidf_transformer = TfidfTransformer()
        
        if self.clip_counts:
            bags_of_words = X.apply(lambda tokens: Counter(set(tokens)))
        else:
            bags_of_words = X.apply(lambda tokens: Counter(tokens))
        
        X_vectors = self.vectorizer.fit_transform(bags_of_words)
        
        self.keep_columns = np.array(X_vectors.sum(axis=0) >= self.min_frequency).squeeze()

        if self.use_tfidf:
            self.tfidf_transformer.fit(X_vectors[:, self.keep_columns])
        
        return self
    
    def transform(self, X):
        
        if self.clip_counts:
            bags_of_words = X.apply(lambda tokens: Counter(set(tokens)))
        else:
            bags_of_words = X.apply(lambda tokens: Counter(tokens))
        
        X_vectors = self.vectorizer.transform(bags_of_words)
        X_vectors = X_vectors[:, self.keep_columns]
        if self.use_tfidf:
            X_vectors = self.tfidf_transformer.transform(X_vectors)
        
        return X_vectors


root = tk.Tk()

open_file = open('word_list.pkl', "rb")
known_words = pickle.load(open_file)
open_file.close()
print(len(known_words))
for i in known_words:
    if i in ['fiscal', 'reclama', 'seis', 'anos', 'prision', 'contras', 'tres', 'ultras', 'delito', 'odio', 'independentistas']:
        print(i)
noticias_token = np.load('noticias_token.npy', allow_pickle=True)

titulo_label = tk.Label(text="Inserte el titulo de la noticia")
titulo_label.pack()
titulo = Entry(root, width=50)
titulo.pack()

sub_titulo_label = tk.Label(text="Inserte el sub_titulo de la noticia")
sub_titulo_label.pack()
sub_titulo = Entry(root, width=50)
sub_titulo.pack()

cuerpo_label = tk.Label(text="Inserte el cuerpo de la noticia")
cuerpo_label.pack()
cuerpo = Entry(root, width=50)
cuerpo.pack()

nltk.download('stopwords')
nlp = spacy.load('es_core_news_sm')
stopword_es = nltk.corpus.stopwords.words('spanish')
resultado_label = Label(root, text='Esperando consulta')
resultado_label.pack()
def clasificarNoticia():
    resultado_label.config(text = 'Cargando resultado')
    noticia_completa = titulo.get() + " " + sub_titulo.get() + " " + cuerpo.get()
    noticia_completa = noticia_completa.lower()
    noticia_a_predecir = pd.Series(noticia_completa)
    noticia_a_predecir =  noticia_a_predecir.apply(lambda sen: delete_tildes(sen))
    noticia_a_predecir = noticia_a_predecir.apply(lambda L: re.sub('[^a-zA-Z]+', ' ', L).strip())
    noticia_a_predecir =  noticia_a_predecir.apply(lambda msg: [token.text.strip() for token in nlp(msg)])
    noticia_a_predecir = noticia_a_predecir.apply(lambda x: remove_stopwords(x))
    noticia_a_predecir = delete_unknown_words(noticia_a_predecir)
    print(noticia_a_predecir[0])
    all_news = pd.Series(noticias_token)
    all_news = all_news.append(noticia_a_predecir).reset_index(drop=True)

    final_model = joblib.load('modelo_odio.pkl')
    res = final_model.predict(BagOfWords(min_frequency=2).fit_transform(all_news).toarray()[-1].reshape(1, -1))
    print(res)
    if res[0] == 0:
        resultado_label.config(text = 'La noticia no es de odio')
    elif res[0] == 1:
        resultado_label.config(text = 'La noticia se trata de un delito de odio')
    else:
        resultado_label.config(text = 'Error inesperado')





def delete_tildes(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
         ("ñ", "n"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s.strip()
def remove_stopwords(text):
    text = [word.strip() for word in text if word not in stopword_es]
    return text
def delete_unknown_words(token_series):
    token_series[0] = [x for x in token_series[0] if x  in known_words]
    print(token_series)
    return token_series
    

button = Button(root, text="Clasificar noticia", command= clasificarNoticia)
button.pack()

root.mainloop()

