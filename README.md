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

## How to run this repository

1. Clone this repo by enter
```
git clone https://github.com/KyleShao1016/Wireless-Network-Handoff-Algorithm.git
```
2. Now, you can run the file 'always_oncall.py' by enter
```
python3 always_oncall.py # this file simulates the scenario that everycars always on-call.
```
or run the file 'random_select_oncall_cars.py'
```
python3 random_select_oncall_cars.py # this file simulates the actual scenario that randomly select a car to call and also randomly assign the holding time to it. 
```
3. The default algorithm would be Best-Effort, if you want to change the algorithm, just enter the corresponding key below to change the algorithm.
** 1 -> Best-Effort **
** 2 -> Entropy **
** 3 -> Threshold **
** 4 -> My Algorithm **
And for 'random_select_oncall_cars.py', because the color of cars which not currently on-call will be black, if you want to make the existed cars invisible, just press key '5', and press '6' to make it visible.
