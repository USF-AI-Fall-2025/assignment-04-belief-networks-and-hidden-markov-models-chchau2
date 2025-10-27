# Belief-Networks-Hidden-Markov-Models
Fall 2025 CS 362/562

1) Give an example of a word which was correctly spelled by the user, but which was incorrectly “corrected” by the algorithm. Why did this happen?

When I inputted ‘nevada’, the program gave me ‘Nevade’. This is likely due to the algorithm calculating that given that I typed ‘a’, it is still more likely that I meant to type ‘e’, not ‘a’. 
Before my loop in the main method, I printed out the probabilities for ‘d’ and got this output: Sample emission probs for 'd': {'d': 0.7692307692307693, 'a': 0.02197802197802198, 'e': 0.10989010989010989, 'i': 0.03296703296703297, ' ': 0.01098901098901099, 'f': 0.01098901098901099, 't': 0.01098901098901099, 'g': 0.01098901098901099, 'r': 0.02197802197802198} 
The probability for ‘e’ is about 0.11 and is much higher than ‘a’, which was about 0.02. 

2) Give an example of a word which was incorrectly spelled by the user, but which was still incorrectly “corrected” by the algorithm. Why did this happen?

When I entered ‘transistion’, it incorrectly “corrected” to transistion (no change).
Looking at the training data, the sequence of letters, s->i->t is slightly less common than s->i->s. And more specifically, n->s->i->t is less common than n->s->i->s. Because of this, the algorithm kept the spelling for the more likely version, which was the original, incorrect form.


3) Give an example of a word which was incorrectly spelled by the user, and was correctly corrected by the algorithm. Why was this one correctly corrected, while the previous two were not?

One word that was incorrectly spelled was ‘directli’, and it was correctly corrected by the algorithm to ‘directly’. The algorithm correctly thought that a ‘y’ was meant to be typed instead of ‘i’. This one was likely correctly corrected because there are a lot of instances in the training dataset where ‘ly’ is the correct spelling, and not so many instances where ‘li’ is a correct instance. 

4) How might the overall algorithm’s performance differ in the “real world” if that training dataset is taken from real typos collected from the internet, versus synthetic typos (programmatically generated)?

If the training dataset came from real typos from the internet, the results of the algorithm would most likely be a lot more accurate. It would accurately capture the common mistakes people make when typing, instead of fabricated ones. Synthetic typos wouldn’t really reflect how people actually mistype words, so an algorithm trained on fake typos would not be nearly as accurate as one trained on real typing behavior. 
