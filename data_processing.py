import urllib.request, urllib.parse, urllib.error
import ssl
import numpy as np
import pandas as pd
from keras.utils import to_categorical

def sequenced (accession):
    url="https://www.ebi.ac.uk/proteins/api/uniparc?size=-1&accession=ACCESSION"
    url = url.replace('ACCESSION', accession)

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:\
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    webpage = str(urllib.request.urlopen(url).read()).split("\\n")[1:]
    sequence = ""
    for line in webpage:
        if ">" in line:
            break
        else:
            sequence += line
    return sequence.strip("'")

def truncate(amino_sequence, position, output_range):
    if position >= len(amino_sequence):
        return None
    if amino_sequence[position-1] != "C":
        return None

    trunseq = ""
    for i in range ((position -1) - output_range, position + output_range):
        if i < 0:
            trunseq += "*"
        elif i >= len(amino_sequence):
            trunseq += "*"
        else:
            trunseq += amino_sequence[i]
    return trunseq

def encode(trunseq):
    char_dict = {"*" : 0, "X" : 0, "A": 1, 'R': 2, 'N': 3, 'D': 4, 'U': 5, 'C': 5, 'Q': 6, 'E': 7, 'G': 8, 'H': 9, 'I': 10, 'L': 11, 'K': 12, 'M': 13, 'F': 14, 'P': 15, 'S': 16, 'T': 17, 'W': 18, 'Y': 19, 'V': 20}
    trunseq = list(trunseq)
    for i in range(len(trunseq)):
        trunseq[i] = char_dict[trunseq[i]]
    one_hot_encode = to_categorical(pd.DataFrame(np.array(trunseq)))
    return one_hot_encode