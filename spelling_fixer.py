import math

#Parse file
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



#Calculate emmision probability
#Estimate P(typed | correct) for every pair of letters.
def find_emission_probs(pairs):
    emission_counts = {}
    total_counts = {}

    #loop over each pair
    for correct, typed in pairs:
        #loop over each letter
        for i in range(min(len(correct), len(typed))):
            c_char, t_char = correct[i], typed[i]

            # initialize nested dict if needed
            if c_char not in emission_counts:
                emission_counts[c_char] = {}
                total_counts[c_char] = 0

            #count how often each correct letter produces each typed letter
            emission_counts[c_char][t_char] = emission_counts[c_char].get(t_char, 0) + 1
            total_counts[c_char] += 1

    # Normalize to probabilities
    # ex) If 'l' was typed correctly 50 times and mistyped as 'i' 3 times:
    # P(l|l)=50/53=0.94,  P(i|l)=3/53=0.06
    emission_probs = {}
    for c_char in emission_counts:
        emission_probs[c_char] = {}
        for t_char in emission_counts[c_char]:
            emission_probs[c_char][t_char] = (emission_counts[c_char][t_char] / total_counts[c_char])
    return emission_probs

#Calculate transition probability
#Estimate P(next_letter | previous_letter) for the correct letters.
def find_transition_probs(pairs):
    transition_counts = {}
    total_counts = {}
    #only need the correct word
    for correct, _ in pairs:
        #indicate start
        prev = "<START>"

        #loop through each correct letter
        for c in correct:

            #initialize dictionary if needed
            if prev not in transition_counts:
                transition_counts[prev] = {}
                total_counts[prev] = 0

            #record transition
            transition_counts[prev][c] = transition_counts[prev].get(c, 0) + 1
            total_counts[prev] += 1
            #save letter for next
            prev = c

        # end transition
        if prev not in transition_counts:
            transition_counts[prev] = {}
            total_counts[prev] = 0
        transition_counts[prev]["<END>"] = transition_counts[prev].get("<END>", 0) + 1
        total_counts[prev] += 1

    # Normalize to probabilities, convert counts to probabilities
    # ex) transition_probs['c']['a'] = 10 / 15 = 0.6667
    transition_probs = {}
    for prev in transition_counts:
        transition_probs[prev] = {}
        for nxt in transition_counts[prev]:
            transition_probs[prev][nxt] = (transition_counts[prev][nxt] / total_counts[prev])
    
    for c in transition_probs:
        if "<END>" not in transition_probs[c]:
            transition_probs[c]["<END>"] = 1e-3  # small chance to end

    return transition_probs


def viterbi(typed_word, transition_probs, emission_probs, alphabet):
    #keeps track of the most likely path
    V = [{}]
    path = {}

    #first letter
    for state in alphabet:
        #probability the word starts with state
        trans_p = transition_probs.get("<START>", {}).get(state, 1e-3)
        #probability the letter emits the typed letter
        emit_p = emission_probs.get(state, {}).get(typed_word[0], 1e-3)
        #use log to avoid overflow
        V[0][state] = math.log(trans_p) + math.log(emit_p)
        path[state] = [state]

    #rest of letters
    for t in range(1, len(typed_word)):
        V.append({})
        new_path = {}

        #for each possible current correct letter
        for state in alphabet:
            emit_p = emission_probs.get(state, {}).get(typed_word[t], 1e-3)
            best_prob = float("-inf")
            best_prev = None

            #check all possible previous letters
            for prev_state in alphabet:
                prob = (
                    V[t - 1][prev_state]
                    + math.log(transition_probs.get(prev_state, {}).get(state, 1e-3))
                    + math.log(emit_p)
                )
                if prob > best_prob:
                    best_prob = prob
                    best_prev = prev_state

            V[t][state] = best_prob
            new_path[state] = path[best_prev] + [state]
        path = new_path

    best_state_here = max(V[t], key=V[t].get)

    #ending the word
    best_prob = float("-inf")
    best_state = None
    for state in alphabet:
        prob = V[-1][state] + math.log(transition_probs.get(state, {}).get("<END>", 1e-3))
        if prob > best_prob:
            best_prob = prob
            best_state = state

    if best_state is None:
        return typed_word

    return "".join(path[best_state])




def main():
    pairs = read_aspell("aspell.txt")
    emission_probs = find_emission_probs(pairs)
    transition_probs = find_transition_probs(pairs)
    alphabet = list(emission_probs.keys())

    while True:
        typed = input("Enter a word or type 'quit' to Quit: ").strip()
        if typed.lower() == "quit":
            break
        corrected = viterbi(typed, transition_probs, emission_probs, alphabet)
        print(f"Did you mean: {corrected}\n")


if __name__ == "__main__":
    main()
