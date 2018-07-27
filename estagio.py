import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import mac_morpho

link_re = re.compile(r"[ (\[{“']https?://ww[0-9a-z.-]+\.[a-z.]{2,6}[/\w.-]*/?\??[^ ]*[ .!?,;\)\]\}]", re.MULTILINE | re.IGNORECASE)
data_re = re.compile(r"(^|[ (\[{“'])\d{1,2}([/.-])\d{1,2}([/.-])\d{2,4}([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
hora_re = re.compile(r"(^|[ (\[{“'])[0-9]{1,2}:?h[0-9]{1,2}(m|(min))?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
valor_re = re.compile(r"(^|[ (\[{“'])[a-zA-Z]{0,2}\$ *\d+([.,]\d*)*([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
espacoPontuacao_re = re.compile(r"\s+([,.;!?ºª:])", re.MULTILINE | re.IGNORECASE)
pontuacaoEspaco_re = re.compile(r"([.;!?ºª:])([^ ])", re.MULTILINE | re.IGNORECASE)
potuacaoRepetida_re = re.compile(r"([^.!?,;:])([.!?,;:])([.!?;,:]+)", re.MULTILINE | re.IGNORECASE)
nao_re = re.compile(r"(^|[ (\[{“'])(((NÃ|NA|Nã|Na|na)(O|o))|ñ)([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE)
nao2_re = re.compile(r"(^|[ (\[{“'])(n|N)( [^0-9])", re.MULTILINE)
risos_re = re.compile(r"(^|[ (\[{“'])(([rs]{3,}|[k]{2,}|[ha]{4,}|[he]{4,}|[hua]{3,})+ *)+([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
notaRuim_re = re.compile(r"(^|[ (\[{“'])nota([ :])?(é|foi)? ?(([01234](,\d+)?)|zero|m[ií]nima|um|dois|tr[eê]s|quatro)([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
notaBoa_re = re.compile(r"(^|[ (\[{“'])nota[ :]?(é|foi)? ?((([56789]|1\.?0+)(\.\d{3}|,\d)*)|dez|mil|m[aá]xima|cem|cinco|seis|sete|oito|nove)([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
letraRepetida_re = re.compile(r"([!-/<=>bdghj-nqtv-à-õ])\1+", re.MULTILINE | re.IGNORECASE)
valeu_re = re.compile(r"vale([uw]|r[{aá])?( +(muito)|(realmente))? +[àa] +pena[- .!?,;\)\]\}”'_:]", re.MULTILINE | re.IGNORECASE)
voce_re = re.compile(r"(^|[ (\[{“'])vo?ce?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
que_re = re.compile(r"(^|[ (\[{“'])q([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
porque_re = re.compile(r"(^|[ (\[{“'])pq([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
emoticonFeliz_re = re.compile(r"(^|[ (\[{])(=\))(\2+|[ .!?,;\)\]\}]+|$)", re.MULTILINE | re.IGNORECASE)
emoticonFeliz2_re = re.compile(r"(^|[ (\[{])(:\))(\2+|[ .!?,;\)\]\}]+|$)", re.MULTILINE | re.IGNORECASE)
emoticonTriste_re = re.compile(r"(^|[ (\[{])(:\()(\2+|[ .!?,;\)\]\}]+|$)", re.MULTILINE | re.IGNORECASE)
emoticonTriste2_re = re.compile(r"(^|[ (\[{])(=\()(\2+|[ .!?,;\)\]\}]+|$)", re.MULTILINE | re.IGNORECASE)
vogalRepetida_re = re.compile(r"([aeiou])\1+", re.MULTILINE | re.IGNORECASE)
eh_re = re.compile(r"eh([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
espacoRepetido_re = re.compile(r"\s{2,}", re.MULTILINE | re.IGNORECASE)
recomendo_re = re.compile(r"(^|[ (\[{“'])r+-?e+-?c+-?o+-?m+-?e+-?n+-?d+-?(a+-?d+-?)?o([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
otimo_re = re.compile(r"(^|[ (\[{“'])[aeiouà-ü]*-?t+-?i+-?m+-?([oa])+-?(s)*([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
excelente_re = re.compile(r"(^|[ (\[{“'])e+-?x+-?c+-?e+-?l+-?e+-?n+-?t+-?e+-?(s)*([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
fantastico_re = re.compile(r"(^|[ (\[{“'])f+-?a+-?n+-?t+-?[aeiouà-ü]*-?s+-?t+-?i+-?c+-?([oa])+-?(s)*([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
maravilhoso_re = re.compile(r"(^|[ (\[{“'])m+-?a+-?r+-?a+-?v+-?i+-?l+-?h+-?o+-?s+-?([oa])+-?(s)*([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
bom_re = re.compile(r"(^|[ (\[{“'])b+-?o+-?[mn]+-?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
agradavel_re = re.compile(r"(^|[ (\[{“'])a+-?g+-?r+-?a+-?d+-?[aeiouà-ü]*v+-?e+-?(l|is)+-?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
indispensavel_re = re.compile(r"(^|[ (\[{“'])i+-?n+-?d+-?i+-?s+-?p+-?e+-?n+-?s+-?[aeiouà-ü]*v+-?e+-?(l|is)+-?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
incrivel_re = re.compile(r"(^|[ (\[{“'])[aeiouà-ü]*-?n+-?c+-?r+-?[aeiouà-ü]*v+-?e+-?(l|is)+-?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
impecavel_re = re.compile(r"(^|[ (\[{“'])i+-?m+-?p+-?e+-?c+-?[aeiouà-ü]*-?v+-?e+-?(l|is)+-?(mente)?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
pessimo_re = re.compile(r"(^|[ (\[{“'])p+-?[aeiouà-ü]*-?(s-?)+i+-?m+-?([oa])+-?(s)*([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
ridiculo_re = re.compile(r"(^|[ (\[{“'])r+-?i+-?d+-?[aeiouà-ü]*-?c+-?u+-?l+-?([oa])+-?(s)*([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
horrivel_re = re.compile(r"(^|[ (\[{“'])h?-?o+-?(r-?)+[aeiouà-ü]*-?v+-?e+-?(l|is)+-?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
terrivel_re = re.compile(r"(^|[ (\[{“'])t+-?e+-?(r-?)+[aeiouà-ü]*-?v+-?e+-?(l|is)+-?(mente)?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
decepcao_re = re.compile(r"(^|[ (\[{“'])d+-?e+-?c?s?-?e+-?p+-?[scç]+-?[aeiouà-ü]*-?o+-?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
ilusao_re = re.compile(r"(^|[ (\[{“'])(d+-?e+-?s+-?)?i+-?l+-?u+-?s+-?[aeiouà-ü]*-?o+-?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
chateacao_re = re.compile(r"(^|[ (\[{“'])c+-?h+-?a+-?t+-?e+-?a+-?[cç]+-?[aeiouà-ü]*-?o+-?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
pizza_re = re.compile(r"(^|[ (\[{“'])p+-?i+-?(z-?)+a+-?([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
chope_re = re.compile(r"(^|[ (\[{“'])c+-?h+-?o+-?p+-?e*([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)
garcom_re = re.compile(r"(^|[ (\[{“'])gar[sç]+o[nm]([- .!?,;\)\]\}”'_:]|$)", re.MULTILINE | re.IGNORECASE)

tsents = mac_morpho.tagged_sents()
tagger0 = nltk.DefaultTagger('N')
tagger1 = nltk.UnigramTagger(tsents, backoff=tagger0)
tagger2 = nltk.BigramTagger(tsents, backoff=tagger1)

o = ""
with open('c:\\dev\\estagio\\analise.txt', encoding='UTF-8') as f:
    o = f.readlines()

dados = []
for line in o:
    while(link_re.search(line)):
        line = re.sub(link_re, '. ', line)

    while(data_re.search(line)):
        line = re.sub(data_re, ' (data) ', line)

    while(valor_re.search(line)):
        line = re.sub(valor_re, ' (valor) ', line)

    while(espacoPontuacao_re.search(line)):
        line = re.sub(espacoPontuacao_re, r'\1', line)

    while(potuacaoRepetida_re.search(line)):
        line = re.sub(potuacaoRepetida_re, r'\1\2', line)

    while(nao_re.search(line)):
        line = re.sub(nao_re, ' não ', line)

    while(nao2_re.search(line)):
        line = re.sub(nao2_re, r' não \3', line)

    while(risos_re.search(line)):
        line = re.sub(risos_re, ' (sorridente) ', line)

    while(notaRuim_re.search(line)):
        line = re.sub(notaRuim_re, ' (ruim) ', line)

    while(notaBoa_re.search(line)):
        line = re.sub(notaBoa_re, r' (ótimo)\7 ', line)

    while(eh_re.search(line)):
        line = re.sub(eh_re, 'é ', line)

    while(valeu_re.search(line)):
        line = re.sub(valeu_re, '(gostei) ', line)

    while(voce_re.search(line)):
        line = re.sub(voce_re, r'\1você\2', line)

    while(que_re.search(line)):
        line = re.sub(que_re, r'\1que\2', line)

    while(porque_re.search(line)):
        line = re.sub(porque_re, r'\1por que\2', line)

    while(emoticonFeliz_re.search(line)):
        line = re.sub(emoticonFeliz_re, ' (feliz) ', line)

    while(emoticonFeliz2_re.search(line)):
        line = re.sub(emoticonFeliz2_re, ' (feliz) ', line)

    while(emoticonTriste_re.search(line)):
        line = re.sub(emoticonTriste_re, ' (tristeza) ', line)

    while(emoticonTriste2_re.search(line)):
        line = re.sub(emoticonTriste2_re, ' (tristeza) ', line)

    while(vogalRepetida_re.search(line)):
        line = re.sub(vogalRepetida_re, r'\1', line)

    while(letraRepetida_re.search(line)):
        line = re.sub(letraRepetida_re, r'\1', line)

    while(hora_re.search(line)):
        line = re.sub(hora_re, ' (hora) ', line)

    while(espacoRepetido_re.search(line)):
        line = re.sub(espacoRepetido_re, ' ', line)

    while (pontuacaoEspaco_re.search(line)):
        line = re.sub(pontuacaoEspaco_re, r'\1 \2', line)

    line = re.sub(recomendo_re, r'\1gostei\3', line)
    line = re.sub(otimo_re, r'\1ótim\2\3\4', line)
    line = re.sub(excelente_re, r'\1excelente\2\3', line)
    line = re.sub(fantastico_re, r'\1fantástic\2\3\4', line)
    line = re.sub(maravilhoso_re, r'\1maravilhos\2\3\4', line)
    line = re.sub(bom_re, r'\1bom\2', line)
    line = re.sub(agradavel_re, r'\1agradáve\2\3', line)
    line = re.sub(indispensavel_re, r'\1indispensáve\2\3', line)
    line = re.sub(incrivel_re, r'\1incríve\2\3', line)
    line = re.sub(impecavel_re, r'\1impecáve\2\3\4', line)
    line = re.sub(pessimo_re, r'\1péssim\3\4\5', line)
    line = re.sub(ridiculo_re, r'\1ridícul\2\3\4', line)
    line = re.sub(horrivel_re, r'\1horríve\3\4', line)
    line = re.sub(terrivel_re, r'\1terríve\3\4\5', line)
    line = re.sub(decepcao_re, r'\1decepção\2', line)
    line = re.sub(ilusao_re, r'\1\2ilusão\3', line)
    line = re.sub(chateacao_re, r'\1chateação\2', line)
    line = re.sub(pizza_re, r'\1pizza\3', line)
    line = re.sub(chope_re, r'\1chope\2', line)
    line = re.sub(garcom_re, r'\1garçom\2', line)

    result = ([word_tokenize(t, language='portuguese') for t in sent_tokenize(line, language='portuguese')])

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

with open('c:\\dev\\estagio\\comentarios - analise.txt', encoding='UTF-8', mode='w') as f:
    for h in dados:
        f.write(str(h) + '\n')