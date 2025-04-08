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
    # Create a key
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
    
    # If first characters match, no operation needed for them
    if S[0] == T[0]:
        result = fast_MED(S[1:], T[1:], MED)
    
    else:
        # insertion, deletion, substitution
        deletion = 1 + fast_MED(S[1:], T, MED)  
        insertion = 1 + fast_MED(S, T[1:], MED)  
        substitution = 1 + fast_MED(S[1:], T[1:], MED)
        
        # Take the minimum of the three
        result = min(deletion, insertion, substitution)
    
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
            
            # If first characters match
            if S[0] == T[0]:
                result = calculate_MED(S[1:], T[1:])
                MED[key] = result
                OPS[key] = ('M',) + OPS[(S[1:], T[1:])]  # M for match
            else:
                # Calculate costs
                del_cost = 1 + calculate_MED(S[1:], T)
                ins_cost = 1 + calculate_MED(S, T[1:])
                sub_cost = 1 + calculate_MED(S[1:], T[1:])
                
                # Find minimum cost
                min_cost = min(del_cost, ins_cost, sub_cost)
                MED[key] = min_cost
                
                # Store the operation used
                if min_cost == del_cost:
                    OPS[key] = ('D',) + OPS[(S[1:], T)]  # D for deletion
                elif min_cost == ins_cost:
                    OPS[key] = ('I',) + OPS[(S, T[1:])]  # I for insertion
                else:  # substitution
                    OPS[key] = ('S',) + OPS[(S[1:], T[1:])]  # S for substitution
            
            return MED[key]
        
        calculate_MED(S, T)
    else:
        OPS = {}
        
        def reconstruct_ops(S, T):
            key = (S, T)
            
            if S == "":
                OPS[key] = ('I',) * len(T)
                return
            elif T == "":
                OPS[key] = ('D',) * len(S)
                return
            
            if S[0] == T[0]:
                if (S[1:], T[1:]) not in OPS:
                    reconstruct_ops(S[1:], T[1:])
                OPS[key] = ('M',) + OPS[(S[1:], T[1:])]
            else:
                # Check which gives minimal cost
                del_key = (S[1:], T)
                ins_key = (S, T[1:])
                sub_key = (S[1:], T[1:])
                
                if del_key not in OPS:
                    reconstruct_ops(S[1:], T)
                if ins_key not in OPS:
                    reconstruct_ops(S, T[1:])
                if sub_key not in OPS:
                    reconstruct_ops(S[1:], T[1:])
                
                del_cost = 1 + MED[del_key] if del_key in MED else float('inf')
                ins_cost = 1 + MED[ins_key] if ins_key in MED else float('inf')
                sub_cost = 1 + MED[sub_key] if sub_key in MED else float('inf')
                
                min_cost = min(del_cost, ins_cost, sub_cost)
                
                if min_cost == del_cost:
                    OPS[key] = ('D',) + OPS[del_key]
                elif min_cost == ins_cost:
                    OPS[key] = ('I',) + OPS[ins_key]
                else:
                    OPS[key] = ('S',) + OPS[sub_key]
        
        if (S, T) not in OPS:
            reconstruct_ops(S, T)
    
    # construct the alignment strings based on operations
    align_S = ""
    align_T = ""
    
    # Get operations for the full strings
    ops = OPS[(S, T)]
    i, j = 0, 0
    
    for op in ops:
        if op == 'M':  # Match
            align_S += S[i]
            align_T += T[j]
            i += 1
            j += 1
        elif op == 'D':  # Deletion from S
            align_S += S[i]
            align_T += '-'
            i += 1
        elif op == 'I':  # Insertion into S
            align_S += '-'
            align_T += T[j]
            j += 1
        elif op == 'S':  # Substitution
            align_S += S[i]
            align_T += T[j]
            i += 1
            j += 1
    
    return (align_S, align_T)
