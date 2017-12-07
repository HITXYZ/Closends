import re
import codecs

with codecs.open('2.txt', encoding='utf8') as fr:
    lines = [line.strip() for line in fr.readlines()]
    texts = []
    for line in lines:
        tmp = re.sub(r'#', ' ', line)
        text = re.sub(r'(<[^>]+>|【|】|\.\.\.全文|\?\?\?)', '', tmp)
        texts.append(text)
    folder = './data_svm/校园/'
    for i in range(len(texts)):
        with codecs.open(folder + str(i+1) + '.txt', 'w', encoding='utf8') as fw:
            fw.write(texts[i])
