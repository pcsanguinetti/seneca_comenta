from sentence_transformers import SentenceTransformer, util
import pickle
import feedparser
from datetime import datetime
import pandas as pd
import re
import ast

print("Cargando modelo...")
model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
print("Modelo cargado.")


# Import Seneca embeddings

def import_embeddings():
    with open('embeddings_seneca.pkl', "rb") as fIn:
        stored_data = pickle.load(fIn)
        sentences = stored_data['sentences']
        embeddings1 = stored_data['embeddings']
    return sentences, embeddings1

# Parse rss, create content embeddings, obtain most similar

def get_match(list_of_urls):
    titulares = []
    links = []
    contenido = []
    sentences, embeddings1 = import_embeddings()
    pattern = "mata|muere|muert|asesin"

    for url in list_of_urls:
        NewsFeed = feedparser.parse(url)
        for entry in NewsFeed.entries:
            if entry.published_parsed[2] == datetime.now().day and re.search(pattern, entry.description.lower()) is None:
                titulares.append(entry.title)
                links.append(entry.link)
                contenido.append(entry.description)
    
    embeddings2 = model.encode(contenido, convert_to_tensor=True)

    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
    score = 0

    for i in range(len(sentences)):
        for q in range(len(titulares)):
            if cosine_scores[i][q] > score and len(sentences[i]) < 280:
                score = cosine_scores[i][q]
                frase = sentences[i]
                titular = titulares[q]
                link = links[q]
                content = contenido[q]
    
    return frase[1:], titular, score, link, content

# Fill df with register of previous titles and Seneca sentences

def fill_df(frase, titular, link, score):
    df = pd.read_csv("register.csv", index_col=[0])
    df.loc[len(df)] = [frase, titular, link, score, datetime.today()]
    df.to_csv("register.csv")

def chapter(frase):
    with open("epistolas.txt") as f:
        texto = f.read()
    with open("chapterdict.txt") as f:
        capitulos = f.read()
    d = ast.literal_eval(capitulos)

    ubicada = re.search(frase.replace("?", "\?"), texto)
    
    if ubicada is None:
        cap = "s/n"
    else:
        ubicada = ubicada.start()
        for capitulo, ubicacion in d.items():
            if ubicada > ubicacion:
                cap = capitulo
    return cap

# Create text for tweet

def get_tweet():
    urls = ["https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
        "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml",
        "https://www.abc.es/rss/feeds/abcPortada.xml",
        "https://rss.elconfidencial.com/espana/",
        "http://api2.rtve.es/rss/temas_espana.xml",
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada",
        "https://e00-elmundo.uecdn.es/elmundo/rss/internacional.xml"]
    
    frase, titular, score, link, content = get_match(urls)
    print("El titular '{}'\ntiene un score de proximidad de {} con la frase:\n'{}'.\nEl resumen de la nota es: {}\ny se encuentra en {}".format(titular, score, frase, content, link))
    nro = chapter(frase)
    text = '"' + frase + '"' + "\n(Séneca, Epístolas morales a Lucilio, " + str(nro) + ")\n\n" + link
    fill_df(frase, titular, link, score)

    return text