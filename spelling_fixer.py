import math

#Read and parese txt file
def read_aspell(filename):
    pairs = []
    with open(filename, "r") as f:
        for line in f:
            if ":" in line:
                correct, typo_list = line.strip().split(":", 1)
                correct = correct.strip()
                typos = typo_list.strip().split()
                for typed in typos:
                    pairs.append((correct, typed))
    return pairs


#Find emission probabilties
def find_emission_probs(pairs):
    counts = {}      # counts[correct_letter][typed_letter]
    totals = {}      # total counts for each correct letter

    for correct, typed in pairs:
        #Go through each letter position
        for i in range(min(len(correct), len(typed))):
            c = correct[i]
            t = typed[i]

            if c not in counts:
                counts[c] = {}
                totals[c] = 0

            counts[c][t] = counts[c].get(t, 0) + 1
            totals[c] += 1

    #Convert counts to log probabilities
    probs = {}
    for c in counts:
        probs[c] = {}
        for t in counts[c]:
            p = counts[c][t] / totals[c]
            probs[c][t] = math.log(p) if p > 0 else math.log(1e-31)

    return probs


#Find transition probabilities
def find_transition_probs(pairs):
    counts = {}   # counts[prev][next]
    totals = {}   # totals[prev]

    for correct, _ in pairs:
        prev = "<START>"
        for c in correct:
            if prev not in counts:
                counts[prev] = {}
                totals[prev] = 0

            counts[prev][c] = counts[prev].get(c, 0) + 1
            totals[prev] += 1
            prev = c

        # end of word
        if prev not in counts:
            counts[prev] = {}
            totals[prev] = 0
        counts[prev]["<END>"] = counts[prev].get("<END>", 0) + 1
        totals[prev] += 1

    #Convert counts to log probabilities
    probs = {}
    for prev in counts:
        probs[prev] = {}
        for nxt in counts[prev]:
            p = counts[prev][nxt] / totals[prev]
            probs[prev][nxt] = math.log(p) if p > 0 else math.log(1e-3)

    #Small ending log probability if missing
    for c in probs:
        if "<END>" not in probs[c]:
            probs[c]["<END>"] = math.log(1e-3)

    return probs


# --------------------------------------------------------------------
# Viterbi algorithm (with log probabilities)
# --------------------------------------------------------------------
def viterbi(typed_word, transition_probs, emission_probs, alphabet):
    #Initialize M[t][s] and backpointer[t][s]
    M = [{} for _ in range(len(typed_word))]
    backpointer = [{} for _ in range(len(typed_word))]

    #Initialize
    for s in alphabet:
        trans_log = transition_probs.get("<START>", {}).get(s, math.log(1e-3))
        emit_log = emission_probs.get(s, {}).get(typed_word[0], math.log(1e-3))
        M[0][s] = trans_log + emit_log
        backpointer[0][s] = None

    #Recursion
    for t in range(1, len(typed_word)):
        for s in alphabet:
            emit_log = emission_probs.get(s, {}).get(typed_word[t], math.log(1e-3))
            best_prev = None
            best_val = float("-inf")

            # find max over all possible previous states
            for prev in alphabet:
                trans_log = transition_probs.get(prev, {}).get(s, math.log(1e-3))
                val = M[t - 1][prev] + trans_log + emit_log
                if val > best_val:
                    best_val = val
                    best_prev = prev

            M[t][s] = best_val
            backpointer[t][s] = best_prev

    #Terminate
    best_final_state = None
    best_final_val = float("-inf")
    for s in alphabet:
        end_log = transition_probs.get(s, {}).get("<END>", math.log(1e-3))
        val = M[-1][s] + end_log
        if val > best_final_val:
            best_final_val = val
            best_final_state = s

    #Backtrace
    if best_final_state is None:
        return typed_word

    result = [best_final_state]
    for t in range(len(typed_word) - 1, 0, -1):
        prev = backpointer[t][result[-1]]
        result.append(prev)

    result.reverse()
    return "".join(result)

#Main
def main():
    pairs = read_aspell("aspell.txt")
    emission_probs = find_emission_probs(pairs)
    transition_probs = find_transition_probs(pairs)
    alphabet = list(emission_probs.keys())

    while True:
        typed = input("\nEnter a word or type 'quit' to Quit: ").strip()
        if typed.lower() == "quit":
            break
        corrected = viterbi(typed, transition_probs, emission_probs, alphabet)
        print(f"Did you mean: {corrected}\n")



if __name__ == "__main__":
    main()
