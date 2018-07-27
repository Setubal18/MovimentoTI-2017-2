import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import floresta, mac_morpho

nomeCien_re = re.compile(r"([^\].a-z])(Ana.[a-z]\w+ [a-z]\w+)", re.MULTILINE | re.IGNORECASE)
Universidade_re = re.compile(r"Uni\w+ ([A-Za-z]\w+ [A-Z]\w+) ", re.MULTILINE | re.IGNORECASE)
refe_re = re.compile(r"\[\d+]", re.MULTILINE | re.IGNORECASE)
num_re = re.compile(r"([0-9])", re.MULTILINE | re.IGNORECASE)

tsents = mac_morpho.tagged_sents()
tagger0 = nltk.DefaultTagger('N')
tagger1 = nltk.UnigramTagger(tsents, backoff=tagger0)
tagger2 = nltk.BigramTagger(tsents, backoff=tagger1)

o = ""
with open('C:\\Ordis\\Arquivos\\Ulbra\\3 Semestre\\MovimentoTI\\Sapos.txt', encoding='ISO-8859-1') as f:
    o = f.readlines()
    print(o)
dados = []

for line in o:
    while (nomeCien_re.search(line)):
        line = re.sub(nomeCien_re, ' (taxonomia) ', line)

    while (Universidade_re.search(line)):
        line = re.sub(Universidade_re, ' (Universidade) ', line)

    while (refe_re.search(line)):
        line = re.sub(refe_re, ' ', line)

    while (num_re.search(line)):
        line = re.sub(num_re, ' (numeros) ', line)

    result = ([word_tokenize(t, 'portuguese') for t in sent_tokenize(line, 'portuguese')])

    sentencas = []
    chunks = []

    for sent in result:
        chunks = []
        for word, tag in tagger2.tag(sent):
             if (word == 'da' or word == 'das' or
                word == 'do' or word == 'dos' or
                word == 'na' or word == 'nas' or
                word == 'no' or word == 'nos'):
                tag = 'PREP'
        chunk = (word + '/' + tag)
        chunks.append(chunk)
    sentencas.append(chunks)

    dados.append(sentencas)

with open('C:\\Ordis\\Arquivos\\Ulbra\\3 Semestre\\MovimentoTI\\resultado.txt', encoding='ISO-8859-1', mode="w") as f:
    for i in dados:
        f.write(str(i) + '\n')
