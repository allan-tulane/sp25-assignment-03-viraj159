import math, queue
from collections import Counter

####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('b--ook', 'bac--k'), ('kook-ab-urr-a', 'kooky-bi-r-d-'), ('relev--ant','-ele-phant'), ('AAAGAATTCA', 'AAA---T-CA')]

def MED(S, T):
    # TO DO - modify to account for insertions, deletions and substitutions
    if (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S))
    else:
        if (S[0] == T[0]):
            return(MED(S[1:], T[1:]))
        else:
            return(1 + min(MED(S, T[1:]), MED(S[1:], T)))


def fast_MED(S, T, MED={}):
    if (S, T) in MED:
        return MED[(S, T)]

    if not S:
        MED[(S, T)] = len(T)
    elif not T:
        MED[(S, T)] = len(S)
    elif S[0] == T[0]:
        MED[(S, T)] = fast_MED(S[1:], T[1:], MED)
    else:
        MED[(S, T)] = 1 + min(fast_MED(S, T[1:], MED), fast_MED(S[1:], T, MED), fast_MED(S[1:], T[1:], MED))

    return MED[(S, T)]


def fast_align_MED(S, T, MED={}):
    if (S, T) in MED:
        return MED[(S, T)]

    if not S:
        MED[(S, T)] = (len(T), '-' * len(T), T)
    elif not T:
        MED[(S, T)] = (len(S), S, '-' * len(S))
    elif S[0] == T[0]:
        distance, aligned_S, aligned_T = fast_align_MED(S[1:], T[1:], MED)
        MED[(S, T)] = (distance, S[0] + aligned_S, T[0] + aligned_T)
    else:
        insert_distance, insert_aligned_S, insert_aligned_T = fast_align_MED(S, T[1:], MED)
        delete_distance, delete_aligned_S, delete_aligned_T = fast_align_MED(S[1:], T, MED)
        replace_distance, replace_aligned_S, replace_aligned_T = fast_align_MED(S[1:], T[1:], MED)

        if insert_distance <= delete_distance and insert_distance <= replace_distance:
            MED[(S, T)] = (1 + insert_distance, insert_aligned_S, T[0] + insert_aligned_T)
        elif delete_distance <= insert_distance and delete_distance <= replace_distance:
            MED[(S, T)] = (1 + delete_distance, S[0] + delete_aligned_S, delete_aligned_T)
        else:
            MED[(S, T)] = (1 + replace_distance, S[0] + replace_aligned_S, T[0] + replace_aligned_T)

    return MED[(S, T)]
