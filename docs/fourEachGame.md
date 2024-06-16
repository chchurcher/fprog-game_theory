[Back to Main Documentation](/README.md)
# Simulation Findings for "Four each Game"

This document presents the results of a simulation where various player strategies competed against each other in games of four players. The players in this simulation are the same as in [Duel of Strategies](/docs/dualOfStrategies.md) without the **Mathematician (LinearExtrapolation 0.5)** and the **RandomPlayer**:

- **AllIn**
- **SaveUpMyMoney (FixedPart 0.9)**
- **Pessimistic (PartOfOthers 0.2, 0.8)**
- **TitForTat (PartOfOthers 0.5, 1.0)**
- **Optimistic (PartOfOthers 0.8, 1.2)**
- **Deceit (RepetitivePattern [0.8, 1.0, 1.2, 0.0])**
- **GrimTrigger (7.5)**


![Heatmap with outcomes](/docs/four_each_game/fourEachGameHeatmapOutcomes.png)

## Game Strategy
Uses the **LinearFunctionByPlayer** game simulation, where a multiplier is calculated by the doubled mean percentage of the individual given money amounts. High cooperation of every player is highly valued whereas low cooperation is punished by even returning less money than the input.

## Cooperation Dynamics
As described in [Duel of Strategies](/docs/dualOfStrategies.md) the cooperation style of the players can be evaluated as the following.
- **High Cooperation Strategies**:  **AllIn**, **SaveUpMyMoney (FixedPart 0.9)**, **Optimistic (PartOfOthers 0.8, 1.2)**
- **Low Cooperation Strategies**: **Pessimistic (PartOfOthers 0.2, 0.8)**, **Deceit (RepetitivePattern [0.8, 1.0, 1.2, 0.0])**
- **Moderate Cooperation Strategies**: **TitForTat (PartOfOthers 0.5, 1.0)**, **GrimTrigger (7.5)**
- 

## Visual Analysis

### Pie charts

![Pie Charts](/docs/four_each_game/fourEachGamePie.png)

As is can be seen here, the mean outcome of the players only differs slightly between the most players. Only the **Pessimistic (PartOfOthers 0.2, 0.8)** and **TitForTat (PartOfOthers 0.5, 1.0)** players do have a lower mean outcome.

### Boxplots

![Boxplot with absolute values](/docs/four_each_game/fourEachGameBoxplotAbs.png)
![Boxplot with log values](/docs/four_each_game/fourEachGameBoxplotLog.png)

Interesting is in the boxplot with the log values, that also the median outcome is more or less the same for every player, but the more optimistic ones do have a larger range of possible outcomes.

###  Gaussian

![Gaussian Chart](/docs/four_each_game/fourEachGameGaussianLog.png)

## Conclusion

The **Pessimistic (PartOfOthers 0.2, 0.8)** strategy has the lowest mean outcome, but the highest minimal outcome. Therefor it can be said that low cooperation is a save conservative strategy for loosing money. On the other hand it also has a low probability of winning money. Highly cooperative strategies as **AllIn** can have bad outcome but do perform in the long run better.


[Back to Main Documentation](/README.md)