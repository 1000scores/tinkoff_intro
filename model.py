from os import listdir
import pickle
import csv


class Model:

    @staticmethod
    def read_txt(self, cur_file):
        with open(cur_file, 'r') as f:
            text = f.read()
            return text

    @staticmethod
    def read_csv(file):
        with open(file, 'r') as f:
            reader = csv.reader(f)
            temp = list(reader)
            temp = [elem[2] for elem in temp]
            text = ''
            for elem in temp:
                text += elem + '.'
            return text

    @staticmethod
    def tokenize(self, lst_of_texts):
        big_lst = []
        for text in lst_of_texts:
            cur_lst_of_tokens = list(filter(None, text.split(' ')))
            big_lst.append(cur_lst_of_tokens)
        return big_lst

    def __init__(self, language='RU'):
        self.language = language
        self.sentence_end = {'!', '.', '\'', '"', ':', ';', ')', '(', '-'}
        self.data = {}
        self.train()

    def save_text(self, big_lst, words_as_key):
        for cur_lst_of_tokens in big_lst:
            for index, token in enumerate(cur_lst_of_tokens):
                if index < words_as_key:
                    continue
                cur_key = ''
                for i in range(1, words_as_key):
                    cur_key += cur_lst_of_tokens[index - i]

                if cur_key not in self.data:
                    self.data[cur_key] = {}

                if token in self.data[cur_key]:
                    self.data[cur_key][token] += 1
                else:
                    self.data[cur_key][token] = 1

    def clean_text(self, text):
        lst = []
        current = ''
        for symbol in text:
            if symbol in self.sentence_end:
                lst.append(current)
                current = ''
            elif self.language == 'RU' and 'а' <= symbol <= 'я':
                current += symbol
            elif self.language == 'ENG' and 'a' <= symbol <= 'z':
                current += symbol
            elif symbol == ' ':
                current += symbol

        if current != '':
            lst.append(current)

        return lst

    def add_text(self, text, words_as_key):
        text = text.lower()
        lst_of_texts = self.clean_text(text)
        big_lst = self.tokenize(lst_of_texts)
        self.save_text(big_lst, words_as_key)

    def add_data(self, words_as_key):
        for file in listdir('data/'):
            if file[0] == '.':
                continue
            if '.csv' in file:
                self.add_text(self.read_csv(f'data/{file}'), words_as_key)
            elif '.txt' in file:
                self.add_text(self.read_txt(f'data/{file}'), words_as_key)
            print(f'Added {file}')

    def sort_data(self, words_for_token=10):
        for token in self.data:
            temp = []
            for token2, value in self.data[token].items():
                temp.append((value, token2))
            temp.sort(reverse=True)
            temp2 = []
            for index, elem in enumerate(temp):
                if index == words_for_token:
                    break
                temp2.append(elem[1])
            self.data[token] = temp2

    def save_model(self, path='data.pickle'):
        with open(path, 'wb') as f:
            pickle.dump(self.data, f)

    def train(self, words_as_key=2):
        print('Starting training!')
        self.add_data(words_as_key)
        self.sort_data()
        self.save_data()
        print('Training finished!')
