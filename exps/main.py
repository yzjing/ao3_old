"""
Dependencies:
Pytorch
Sklearn
Numpy 1.16+
Known to work with Python 3.6, 3.7
"""

import logging
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from model import LSTM
from preprocessing import get_chord_sequence_index, get_word_vec, train_test_val_split
from train_test import train

torch.manual_seed(1)
# logging.basicConfig(level=logging.DEBUG)

def main(chord_file="chordwords.csv", wordvec_file="wordEmbeddings-002.p", debug_flag=False):
    """
        Run the model using the chordword sequence from the `chord_seq_file`.
        word2vec from the `wordvec_file`.
    """
    chord_to_index, chord_data = get_chord_sequence_index(chord_file)
    vocab_size = len(chord_to_index) + 1 # account for the 0 as padding 
    wordvecs= get_word_vec(wordvec_file)
    if debug_flag:
        debug_chord, debug_wordvec = train_test_val_split(chord_data, wordvecs, debug_flag=True)
        chord_data = debug_chord
        wordvec_data = debug_wordvec
        logging.debug("loaded debug sample")
    else:
        (train_chord,
         train_wordvec,
         test_chord,
         test_wordvec,
         val_wordvec,
         val_chord
         ) = train_test_val_split(chord_data, wordvecs)
        chord_data = train_chord
        wordvec_data = train_wordvec
    lstm = LSTM(
        seq_len=15, vocab_size=vocab_size, embed_size=100, hidden_dim=128, batch_size=10
    )
    optimizer = optim.Adam(lstm.parameters(), lr=0.05)
    criterion = nn.CrossEntropyLoss()
    train(
        lstm=lstm,
        optimizer=optimizer,
        criterion=criterion,
        chord_data=chord_data,
        wordvec_data=wordvec_data,
        num_epochs=100,
    )


if __name__ == "__main__":
    CHORD_SEQ_FILE = "chordwords.csv"
    WORD_VEC_FILE = "wordEmbeddings.p"
    main(CHORD_SEQ_FILE, WORD_VEC_FILE, debug_flag=False)
