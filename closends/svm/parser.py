import os, re, math, codecs
from itertools import chain
from collections import Counter

import jieba
from libsvm.svmutil import *

DEBUG = True

class Preprocess(object):
    def __init__(self, stop_words, sample_num):
        self.stop_words = stop_words
        self.sample_num = sample_num

    def is_useful(self, word):
        """check whether if one word is a stop word"""

        return word not in self.stop_words and not re.search('([A-Za-z]+|\d+\.*\d*)', word)

    def pos_one_text(self, file_path):
        """pos for one text and return the result as a list"""

        with codecs.open(file_path, encoding='utf8') as fr:
            text = fr.read().strip()
            seg_list = list(jieba.cut(text, cut_all=False))
            return [item for item in seg_list if self.is_useful(item)]

    def pos_all_text(self, src_folder, des_folder, cnt_folder):
        """pos for all the texts and write the results into files"""

        files = sorted(os.listdir(src_folder), key=lambda item: int(item[:-4]))[:1000]
        for i in range(len(files)):
            if DEBUG and not i - 1 % 500: print(i)
            pos_result = self.pos_one_text(src_folder + '/' + files[i])
            cnt_words = [key + '\t' + str(value) for key, value in Counter(pos_result).items()]
            with codecs.open(des_folder + '/' + files[i], 'w', encoding='utf8') as fw:
                fw.write('\n'.join(pos_result))
            with codecs.open(cnt_folder + '/' + files[i], 'w', encoding='utf8') as fw:
                fw.write('\n'.join(cnt_words))

    def read_cnt_data(self, root_catelogue):
        """read words in each category, storaged in ndarray"""

        unique_category_words, all_category_words = [], []
        all_folders = os.listdir(root_catelogue)
        for foldername in all_folders:
            category_words = []
            cnt_folder = root_catelogue + '/' + foldername
            files = sorted(os.listdir(cnt_folder), key=lambda item: int(item[:-4]))[:self.sample_num]
            for filename in files:
                with codecs.open(cnt_folder + '/' + filename, encoding='utf8') as fr:
                    category_words.append([line.strip().split('\t')[0] for line in fr.readlines()])
            all_category_words.append(category_words)
            unique_category_words.append(set(list(chain(*category_words))))
        return unique_category_words, all_category_words

    def extract_feature_words(self, root_catelogue):
        """extract feature words adn write them into files"""

        # read data from cnt_data file
        unique_category_words, all_category_words = self.read_cnt_data(root_catelogue)

        category_num = len(all_category_words)
        category_file_num = len(all_category_words[0])
        total_file_num = category_num * category_file_num
        if DEBUG: print(category_num, category_file_num, total_file_num)

        # caculate chi-value for word in every category
        extract_features = []
        for i in range(category_num):
            if DEBUG: print('start category', i + 1)
            category_chi_values = []
            for word in unique_category_words[i]:
                a, b = 0, 0
                for j in range(category_num):
                    if j == i:
                        for file_words in all_category_words[j]:
                            if word in file_words: a += 1
                    else:
                        for file_words in all_category_words[j]:
                            if word in file_words: b += 1
                c, d = category_file_num - a, category_file_num * (category_num - 1) - b
                category_chi_values.append(
                    (a * d - b * c) ** 2 * total_file_num / ((a + b) * (a + c) * (b + d) * (c + d)))
            word_chi_values = sorted(list(zip(unique_category_words[i], category_chi_values)), key=lambda item: item[1], reverse=True)

            # extract the first 1000 words in each category as feature words
            extract_features.extend([word for word, _ in word_chi_values[:1000]])
            with codecs.open('category_feature_' + str(i + 1) + '.txt', 'w', encoding='utf8') as fw:
                fw.write('\n'.join(extract_features))

        # caculate feature-word idf values
        feature_idf_values = self.caculate_IDF(total_file_num, all_category_words, set(extract_features))
        extract_features = list(enumerate(set(extract_features)))
        with codecs.open('extract_features.txt', 'w', encoding='utf8') as fw:
            extract_features = ['{:<10d}{:10}\t{:<10f}'.format(index + 1, word, idf) for (index, word), idf in zip(extract_features, feature_idf_values)]
            fw.write('\n'.join(extract_features))

    def caculate_IDF(self, total_file_num, all_category_words, feature_words):
        """caculate words idf value"""

        word_text_cnts = {}
        for category_words in all_category_words:
            if DEBUG: print('start category ', all_category_words.index(category_words) + 1)
            for file_words in category_words:
                for word in file_words:
                    if not word_text_cnts.get(word):
                        word_text_cnts[word] = 1
                    else:
                        word_text_cnts[word] += 1
        return [math.log(total_file_num / (word_text_cnts[word] + 1)) for word in feature_words]

    def generate_train_vector(self, root_catelogue):
        """convert the text into vector and write into file"""

        feature_words = [re.split('\s+', line.strip()) for line in codecs.open('extract_features.txt', encoding='utf8').readlines()]
        feature_words = dict([(word[1], (word[0], word[2])) for word in feature_words])
        category_feature_words = [[line.strip() for line in codecs.open('category_feature_' + str(i) + '.txt', encoding='utf8').readlines()] for i in range(1, 11)]

        all_folders = os.listdir(root_catelogue)
        for i in range(len(all_folders)):
            category_vectors = []
            cnt_folder = root_catelogue + '/' + all_folders[i]
            files = sorted(os.listdir(cnt_folder), key=lambda item: int(item[:-4]))[:self.sample_num]
            for filename in files:
                with codecs.open(cnt_folder + '/' + filename, encoding='utf8') as fr:
                    vector = []
                    for word in [line.strip().split('\t') for line in fr.readlines()]:
                        if len(word) < 2: continue
                        if word[0] in category_feature_words[i]:
                            TF_IDF = float(word[1]) * float(feature_words[word[0]][1])
                            vector.append((int(feature_words[word[0]][0]), TF_IDF))
                    vector = sorted(vector, key=lambda item: item[0])
                    vector = [str(item[0]) + ':' + str(item[1]) for item in vector]
                    category_vectors.append(' '.join(vector))

            with codecs.open('category_vector_' + '' + str(i + 1) + '.txt', 'w', encoding='utf8') as fw:
                fw.write('\n'.join(category_vectors))


class SVM(object):
    def __init__(self):
        pass

    def train(self, data_path, model_path, param_str=''):
        """train model and save it into file"""

        if not param_str:
            param_str = '-c 32768 -g 3.05175e-05 -q'
        y, x = svm_read_problem(data_path)
        svm_prob = svm_problem(y, x)
        svm_param = svm_parameter(param_str)
        model = svm_train(svm_prob, svm_param)
        svm_save_model(model_path, model)

    def predict(self, data_path, modal_path):
        """predict label for unlabel data"""

        y, x = svm_read_problem(data_path)
        svm_model = svm_load_model(modal_path)
        p_label, p_acc, p_val = svm_predict(y, x, svm_model)
        # ACC, MSE, SCC = evaluations(y, p_label)
        return p_label, p_acc, p_val


if __name__ == '__main__':
    svm_lab = SVM()
    svm_lab.train('train.1', 'svm.model')
    svm_lab.predict('test.1', 'svm.model')

    with codecs.open('stop_words.txt', encoding='utf8') as fr:
        stop_words = list(fr.read().strip().split('\r\n'))
    stop_words.append('\u3000')

    src_root_catelogue = 'C:/Users/gzhang/Desktop/svm_data'
    des_root_catelogue = 'C:/Users/gzhang/Desktop/pos_data'
    cnt_root_catelogue = 'C:/Users/gzhang/Desktop/cnt_data'
    lab = Preprocess(stop_words, 20)

    all_folders = os.listdir(src_root_catelogue)
    # for folder in all_folders:
    #     src_folder = src_root_catelogue+'/'+folder
    #     des_folder = des_root_catelogue+'/'+folder
    #     cnt_folder = cnt_root_catelogue+'/'+folder
    #     if not os.path.exists(des_folder): os.mkdir(des_folder)
    #     if not os.path.exists(cnt_folder): os.mkdir(cnt_folder)
    #     lab.pos_all_text(src_folder, des_folder, cnt_folder)

    # lab.extract_feature_words(cnt_root_catelogue)
    # lab.generate_train_vector(cnt_root_catelogue)
