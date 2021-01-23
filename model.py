from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis
from torchmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH

import json
import numpy as np

def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]

with open(VOCAB_PATH, 'r') as f:
    vocabulary = json.load(f)

st = SentenceTokenizer(vocabulary, 300)
model = torchmoji_emojis(PRETRAINED_PATH)

def emojify_sentences():
    l = ["You look great today!"]
    tokenized, _, _ = st.tokenize_sentences(l)
    prob = model(tokenized)

    result = []
    for prob in [prob]:
        for i in range(len(l)):
            t_prob = prob[i]
            ind_top = top_elements(t_prob, 5)
            result.append(list(zip(ind_top, (t_prob[ind] for ind in ind_top))))
    
    return result