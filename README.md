# Belief-Networks-Hidden-Markov-Models
Fall 2025 CS 362/562

1) Give an example of a word which was correctly spelled by the user, but which was incorrectly “corrected” by the algorithm. Why did this happen?

When I inputted ‘nevada’, the program gave me ‘Nevade’. This is likely due to the algorithm calculating that given that I typed ‘a’, it is still more likely that I meant to type ‘e’, not ‘a’. 
Before my loop in the main method, I printed out the emission probabilities for 'e'.
Here are the outputs:
P(e | e) = 0.57630522088353409 
P(a | e) = 0.03815261044176706
Out of all the times the correct letter was ‘e’, about 57.6% of the time ,‘e’ was typed correctly.
Out of all the times the correct letter was ‘e’, about 3.8% of the time ‘a’ was accidentally typed.
From the training data, the algorithm comptuted that it is far more likely that 'e' would be more likely to be typed correctly than accidentally typing 'a'.

2) Give an example of a word which was incorrectly spelled by the user, but which was still incorrectly “corrected” by the algorithm. Why did this happen?

When I entered ‘transistion’, it incorrectly “corrected” to transistion (no change).
Looking at the training data, the sequence of letters, s->i->t is slightly less common than s->i->s. And more specifically, n->s->i->t is less common than n->s->i->s. Because of this, the algorithm kept the spelling for the more likely version, which was the original, incorrect form.

Additionally, I got these emission transition probabilities. 
Emission:   P(s | s) = 0.65236051502145920
            P(t | s) = 0.03862660944206009
Transition: P(i | s) = 0.14566929133858267
            P(s | i) = 0.09629629629629628
            P(t | i) = 0.10617283950617283
While the probability that 'i' would go to 's' is lower than 'i' would go to 't', it is by a small margin. The algorithm likely still chose "transistion' because the probability 's' was typed correctly was 65%, while the probability that 't' was accidentally typed instead of 's' was only 3%.

3) Give an example of a word which was incorrectly spelled by the user, and was correctly corrected by the algorithm. Why was this one correctly corrected, while the previous two were not?

One word that was incorrectly spelled was ‘directli’, and it was correctly corrected by the algorithm to ‘directly’. The algorithm correctly thought that a ‘y’ was meant to be typed instead of ‘i’. This one was likely correctly corrected because there are a lot of instances in the training dataset where ‘ly’ is the correct spelling, and not so many instances where ‘li’ is a correct instance. 


4) How might the overall algorithm’s performance differ in the “real world” if that training dataset is taken from real typos collected from the internet, versus synthetic typos (programmatically generated)?

If the training dataset came from real typos from the internet, the results of the algorithm would most likely be a lot more accurate. It would accurately capture the common mistakes people make when typing, instead of fabricated ones. Synthetic typos wouldn’t really reflect how people actually mistype words, so an algorithm trained on fake typos would not be nearly as accurate as one trained on real typing behavior. 
