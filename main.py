import math, queue
from collections import Counter

####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('b--ook', 'bac--k'), ('kook-ab-urr-a', 'kooky-bi-r-d-'), ('relev--ant', '-ele-phant'),
              ('AAAGAATTCA', 'AAA---T-CA')]


def MED(S, T):
    # TO DO - modify to account for insertions, deletions and substitutions
    if (S == ""):
        return (len(T))
    elif (T == ""):
        return (len(S))
    else:
        if (S[0] == T[0]):
            return (MED(S[1:], T[1:]))
        else:
            return (1 + min(MED(S, T[1:]), MED(S[1:], T)))


def fast_MED(S, T, MED={}):
    # Create key
    key = (S, T)

    # Return result
    if key in MED:
        return MED[key]

    # Base cases
    if S == "":
        MED[key] = len(T)
        return MED[key]
    elif T == "":
        MED[key] = len(S)
        return MED[key]

    if S[0] == T[0]:
        result = fast_MED(S[1:], T[1:], MED)
    else:
        deletion = 1 + fast_MED(S[1:], T, MED)  # Delete from S
        insertion = 1 + fast_MED(S, T[1:], MED)  # Insert into S

        # Take the minimum
        result = min(deletion, insertion)

    # return the result
    MED[key] = result
    return result


def fast_align_MED(S, T, MED={}):
    if not MED:
        OPS = {}

        def calculate_MED(S, T):
            key = (S, T)

            if key in MED:
                return MED[key]

            # Base cases
            if S == "":
                MED[key] = len(T)
                OPS[key] = ('I',) * len(T)  # All insertions
                return MED[key]
            elif T == "":
                MED[key] = len(S)
                OPS[key] = ('D',) * len(S)  # All deletions
                return MED[key]

            if S[0] == T[0]:
                result = calculate_MED(S[1:], T[1:])
                MED[key] = result
                OPS[key] = ('M',) + OPS[(S[1:], T[1:])]  # M for match
            else:
                del_cost = 1 + calculate_MED(S[1:], T)
                ins_cost = 1 + calculate_MED(S, T[1:])

                # Find minimum cost
                min_cost = min(del_cost, ins_cost)
                MED[key] = min_cost

                # Store operation used
                if min_cost == del_cost:
                    OPS[key] = ('D',) + OPS[(S[1:], T)]  # D for deletion
                else:  # insertion
                    OPS[key] = ('I',) + OPS[(S, T[1:])]  # I for insertion

            return MED[key]

        calculate_MED(S, T)

        #  construct the alignment strings
        i, j = 0, 0
        align_S = ""
        align_T = ""

        def build_alignment(S, T, i, j):
            key = (S, T)

            # Base cases
            if S == "":
                return "-" * len(T), T
            elif T == "":
                return S, "-" * len(S)

            if key not in OPS:
                return "", ""

            if OPS[key][0] == 'M':  # Match
                s_rest, t_rest = build_alignment(S[1:], T[1:], i + 1, j + 1)
                return S[0] + s_rest, T[0] + t_rest
            elif OPS[key][0] == 'D':  # Deletion
                s_rest, t_rest = build_alignment(S[1:], T, i + 1, j)
                return S[0] + s_rest, "-" + t_rest
            else:  # Insertion
                s_rest, t_rest = build_alignment(S, T[1:], i, j + 1)
                return "-" + s_rest, T[0] + t_rest

        align_S, align_T = build_alignment(S, T, 0, 0)
        return align_S, align_T
    else:

        def reconstruct_alignment(S, T):
            if S == "":
                return "-" * len(T), T
            if T == "":
                return S, "-" * len(S)

            if S[0] == T[0]:
                rest_S, rest_T = reconstruct_alignment(S[1:], T[1:])
                return S[0] + rest_S, T[0] + rest_T
            else:
                delete_key = (S[1:], T)
                insert_key = (S, T[1:])

                if delete_key not in MED:
                    fast_MED(S[1:], T, MED)
                if insert_key not in MED:
                    fast_MED(S, T[1:], MED)

                delete_dist = MED.get(delete_key, float('inf'))
                insert_dist = MED.get(insert_key, float('inf'))

                if 1 + delete_dist <= 1 + insert_dist:
                    # Deletion is optimal
                    rest_S, rest_T = reconstruct_alignment(S[1:], T)
                    return S[0] + rest_S, "-" + rest_T
                else:
                    # Insertion is optimal
                    rest_S, rest_T = reconstruct_alignment(S, T[1:])
                    return "-" + rest_S, T[0] + rest_T

        # Get the alignment
        return reconstruct_alignment(S, T)
