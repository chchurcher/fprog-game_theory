[Back to Main Documentation](/README.md)
# Simulation Findings for Duel of Strategies

This document presents the results of a simulation where various player strategies competed against each other in games of four players. The players in this simulation were the same as in [Duel of Strategies](/docs/dualOfStrategies.md) and are described there more in detail:

- **AllIn**
- **SaveUpMyMoney (FixedPart 0.9)**
- **Pessimistic (PartOfOthers 0.2, 0.8)**
- **TitForTat (PartOfOthers 0.5, 1.0)**
- **Optimistic (PartOfOthers 0.8, 1.2)**
- **Deceit (RepetitivePattern [0.8, 1.0, 1.2, 0.0])**
- **Mathematician (LinearExtrapolation 0.5)**
- **RandomPlayer (seed 123)**
- **GrimTrigger (7.5)**


![Boxplot with log values](/docs/dual_of_strategies/duelOfStrategiesBoxplotLog.png)

## Game Strategy
Uses the **LinearFunctionByPlayer** game simulation, where a multiplier is calculated by the doubled mean percentage of the individual given money amounts. High cooperation of every player is highly valued whereas low cooperation is punished by even returning less money than the input.


## Performance Analysis

### Cooperation Dynamics
- **High Cooperation Strategies**:  **AllIn**, **SaveUpMyMoney (FixedPart 0.9)** and **Optimistic (PartOfOthers 0.8, 1.2)** generally led to mutual gains and stable interactions. Their cooperative nature made them effective in maintaining positive outcomes over multiple rounds.
- **Low Cooperation Strategies**: **Pessimistic (PartOfOthers 0.2, 0.8)**, **Deceit (RepetitivePattern [0.8, 1.0, 1.2, 0.0])**, and  showed that aggressive or unpredictable strategies often resulted in high variability in outcomes, making them less reliable in fostering cooperative play.
- **Mixed Cooperation Strategies**: **TitForTat (PartOfOthers 0.5, 1.0)**, **RandomPlayer**, **Mathematician (LinearExtrapolation 0.5)**, **GrimTrigger (7.5)** displayed a balance between cooperation and competition, performing variably depending on the opponent's strategy.

![Pie Charts](/docs/dual_of_strategies/duelOfStrategiesPie.png)

### Effectiveness of Cooperation
- **Advantages of Cooperation**: Strategies that encouraged mutual cooperation, such as **AllIn** and **Optimistic**, often led to high outcomes for all players, but 
- **Disadvantages of Cooperation**: While cooperation generally yielded highly positive results for all players in the long term, it generally benefits the opponents more than the player itself. Players with mixed or low cooperation strategies could take advantage of cooperative players.
- **Moderate Cooperation**: Eventough the **Deceit (RepetitivePattern [0.8, 1.0, 1.2, 0.0])** could benefit really well of the opponents trust, the **Optimistic (PartOfOthers 0.8, 1.2)** was the one with the lowest viarity


![Gaussian Chart](/docs/dual_of_strategies/duelOfStrategiesGaussian.png)
## Visual Analysis

### Boxplots

![Boxplot with absolute values](/docs/dual_of_strategies/duelOfStrategiesBoxplotAbs.png)
![Boxplot with log values](/docs/dual_of_strategies/duelOfStrategiesBoxplotLog.png)

###  Heatmap

![Heatmaps of the simulation](/docs/dual_of_strategies/duelOfStrategiesHeatmap.png)

## Conclusion

The simulation provides insights into the dynamics of different player strategies in a game theory context. Strategies that balanced cooperation with rational decision-making, like **Optimistic** and **TitForTat**, tended to perform well overall. Highly aggressive or deceitful strategies could achieve high scores but were less consistent. Future simulations with more comprehensive testing can provide deeper insights.


[Back to Main Documentation](/README.md)