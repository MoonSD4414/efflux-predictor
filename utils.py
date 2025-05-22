import numpy as np

def extract_features(sequence):
    # AAC 萃取簡例
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    seq = sequence.upper()
    features = [seq.count(aa)/len(seq) for aa in amino_acids]
    return np.array(features)
