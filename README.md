# Wireless-Network-Handoff-Algorithm
This repository is mainly used to compare different handoff algorithm, including Threshold, Best-Effort, Entropy, My Algorithm.

## Threshold
I chose a minimum receiving power P_MIN, if the receiving power is lower than P_MIN, handoff the base station to the strongest power provided by the base station received by the car.

## Best-Effort
Cars always chose the base station which providing the strongest power.

## Entropy
Choose a entropy first, and if the difference of the provided power between the BS connected to by the car and the BS providing the strongest power is lower than the entropy, not to implement handoff, otherwise, make the handoff.

## My Algorithm
This algorithm is an optimization of entropy, the difference between this algorithm and entropy is that when choosing new BS, entropy tends to choose the BS providing the strongest BS, however, my algorithm tends to choose the nearest BS associated with the car.
