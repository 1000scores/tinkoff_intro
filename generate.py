import pickle
from model import Model
import random


def read_model():
    with open('model_data.pickle', 'rb') as f:
        temp_model = pickle.load(f)
        return temp_model


model = read_model()

start_word = model.data[random.randint(0, len(model) - 1)]

text = start_word + ' '
for _ in range(40):
    nw_word = model.data[start_word][random.randint(0, min(len(model[start_word]) - 1, 4))]
    text += nw_word + ' '
    start_word = nw_word

text += '.'
print(text)
