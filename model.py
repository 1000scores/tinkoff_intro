from os import listdir
import pickle
import csv


class Model:

    @staticmethod
    def read_txt(cur_file):
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
    def tokenize(lst_of_texts):
        big_lst = []
        for text in lst_of_texts:
            cur_lst_of_tokens = list(filter(None, text.split(' ')))
            big_lst.append(cur_lst_of_tokens)
        return big_lst

    def __init__(self, language='RU'):
        self.language = language
        self.sentence_end = {'!', '.', '\'', '"', ':', ';', ')', '(', '-'}
        self.data = {}
        if len(self.data) == 0:
            self.train()

    def save_text(self, big_lst):
        for cur_lst_of_tokens in big_lst:
            for index, token in enumerate(cur_lst_of_tokens):
                if index == 0:
                    continue
                if cur_lst_of_tokens[index - 1] not in self.data:
                    self.data[cur_lst_of_tokens[index - 1]] = {}

                if token in self.data[cur_lst_of_tokens[index - 1]]:
                    self.data[cur_lst_of_tokens[index - 1]][token] += 1
                else:
                    self.data[cur_lst_of_tokens[index - 1]][token] = 1

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

    def add_text(self, text):
        text = text.lower()
        lst_of_texts = self.clean_text(text)
        big_lst = self.tokenize(lst_of_texts)
        self.save_text(big_lst)

    def add_data(self):
        for file in listdir('data/'):
            if file[0] == '.':
                continue
            if '.csv' in file:
                self.add_text(self.read_csv(f'data/{file}'))
            elif '.txt' in file:
                self.add_text(self.read_txt(f'data/{file}'))
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

    def save_model(self, path='big_model.pickle'):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def train(self):
        print('Starting training!')
        self.add_data()
        self.sort_data()
        self.save_model()
        print('Training finished!')


temp = Model()
