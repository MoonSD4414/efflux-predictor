import numpy as np

def extract_aac_features(sequence):
    sequence = sequence.upper()
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    total = len(sequence)
    features = [sequence.count(aa) / total for aa in amino_acids]
    return np.array(features)
