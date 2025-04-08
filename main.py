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
# TODO - implement top-down memoization
pass

def fast_align_MED(S, T, MED={}):
# TODO - keep track of alignment
pass
