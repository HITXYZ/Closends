import codecs
from random import shuffle
from wordcloud import WordCloud
from django.conf import settings
import matplotlib.pyplot as plt


def generate_cloud(word_num):
    """generate wordcloud with the given word_num"""

    with codecs.open(settings.BASE_DIR + '/closends/word2cloud/words.txt', 'r', encoding='utf8') as fr:
        words = fr.read()

    word_list = []
    for word, num in word_num:
        word_list += [word] * num * 30
    shuffle(word_list)

    text = ' '.join(word_list) + words
    cloud = WordCloud(
        width=800,
        height=600,
        max_words=2000,
        min_font_size=20,
        max_font_size=120,
        font_path="simhei.ttf",
        background_color='black'
    )

    word_cloud = cloud.generate(text)  # 产生词云
    cloud.to_file(settings.BASE_DIR + '/static/closends/wordcloud/cloud.jpg')
    return word_cloud


if __name__ == '__main__':
    word_num = [('中文', 20), ('外语', 10), ('法语', 100), ('玛丽', 62), ('魅力', 42)]
    word_cloud = generate_cloud(word_num)
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()
