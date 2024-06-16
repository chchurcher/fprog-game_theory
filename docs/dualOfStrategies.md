# Simulation Findings for Duel of Strategies

This document presents the results of a simulation where various player strategies competed against each other in one-by-one duels. The players in this simulation were:

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

## Player Strategies and Cooperation

### 1. **AllIn**
   - **Strategy**: Bets everything in every round.
   - **Cooperation**: Highest possible cooperation.

### 2. **SaveUpMyMoney (FixedPart 0.9)**
   - **Strategy**: Saves up a fixed part of their money and, in this case, only inputs 90% of its money.
   - **Cooperation**: High cooperation; tries to save money by only giving 90% of its money every round.

### 3. **Pessimistic (PartOfOthers 0.2, 0.8)**
   - **Strategy**: Starts by given 20% of the starting money and then bets only 80% of the opponent’s previous bet.
   - **Cooperation**: Low cooperation; tends to mirror conservative moves of opponents. It is suspicious that the opponent might give less money the next round.

### 4. **TitForTat (PartOfOthers 0.5, 1.0)**
   - **Strategy**: Starts by given 50% of the starting money and matches the opponent’s previous bet afterward.
   - **Cooperation**: Moderate cooperation; fosters stable and predictable interactions.

### 5. **Optimistic (PartOfOthers 0.8, 1.2)**
   - **Strategy**: Starts by given 80% of the starting money and from then on bets a 20% more than the opponent’s previous bet, skewed towards optimistic outcomes.
   - **Cooperation**: High cooperation; encourages mutual gains.

### 6. **Deceit (RepetitivePattern [0.8, 1.0, 1.2, 0.0])**
   - **Strategy**: Follows a repetitive pattern that includes zero bets to deceive the opponent.
   - **Cooperation**: Low cooperation; builds up trust by increasing the amount of money given each round and then 'unpredictability' bets.

### 7. **Mathematician (LinearExtrapolation 0.5)**
   - **Strategy**: Uses linear extrapolation to predict and match the opponent’s future bet. Starts with 50% of its money.
   - **Cooperation**: Moderate cooperation; rational approach fosters some level of predictability.

### 8. **RandomPlayer (seed 123)**
   - **Strategy**: Bets randomly based on a fixed seed for reproducibility.
   - **Cooperation**: Unpredictability makes cooperation difficult.

### 9. **GrimTrigger (7.5)**
   - **Strategy**: Doesn't cooperate until the opponent’s bet exceeds a threshold of €7.50, then starts to bet everything he has.
   - **Cooperation**: Low initial cooperation; severe punishment for non-cooperation, but high cooperation after enough trust of the opponent.

## Performance Analysis

### Summary of Performance

### 1. **AllIn**
   - **Overall Performance**: Generally performs well against all players, but always wins less than the opponent.
   - Reason for general good performances in all participating games, but always gets out with less than opponent.

### 2. **SaveUpMyMoney (FixedPart 0.9)**
   - **Overall Performance**: Effective in long-term games where the opponent is highly cooperative.
   - Performed extremely well against **AllIn**, achieving the highest overall outcome in this duel.
   - Poor performance against low-cooperative players like **Pessimistic (PartOfOthers 0.2, 0.8)**, indicating vulnerability to these strategies.

### 3. **Pessimistic (PartOfOthers 0.2, 0.8)**
   - **Overall Performance**: Bad performance in total, but slightly better in each particular game compared to the opponent.
   - Causes opponents to be even worse than himself.

### 4. **TitForTat (PartOfOthers 0.5, 1.0)**
   - **Overall Performance**: Effective in promoting mutual cooperation; performs well with cooperative opponents.
   - Encourages stable outcomes with high mutual gains.

### 5. **Optimistic (PartOfOthers 0.8, 1.2)**
   - **Overall Performance**: Performs well against most strategies, balancing aggression and optimism.
   - Encourages mutual cooperation and higher collective outcomes.

### 6. **Deceit (RepetitivePattern [0.8, 1.0, 1.2, 0.0])**
   - **Overall Performance**: Effective in confusing and outmaneuvering opponents.
   - Performed moderate against optemistic strategies but bad against non-cooperating players. 

### 7. **Mathematician (LinearExtrapolation 0.5)**
   - **Overall Performance**: Moderate performance in all environments where future trends can be predicted.
   - Bad results against **GrimTrigger**.
   - Performs variably depending on the predictability of opponents.

### 8. **RandomPlayer (seed 123)**
   - **Overall Performance**: Highly variable but overall bad performance due to the randomness.
   - Only slightly better performance against cooperative players.
   - Quite good against **Deceit (RepetitivePattern [0.8, 1.0, 1.2, 0.0])**

### 9. **GrimTrigger (7.5)**
   - **Overall Performance**: High effectiveness against aggressive players, fostering initial cooperation but punishing betrayal.
   - High performance with **AllIn** and **SaveUpMyMoney**.
   - Bad performance with non-cooperative behavior.

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

## Boxplots

![Boxplot with absolute values](/docs/dual_of_strategies/duelOfStrategiesBoxplotAbs.png)
![Boxplot with log values](/docs/dual_of_strategies/duelOfStrategiesBoxplotLog.png)

## Heatmap

![Heatmaps of the simulation](/docs/dual_of_strategies/duelOfStrategiesHeatmap.png)

## Conclusion

The simulation provides insights into the dynamics of different player strategies in a game theory context. Strategies that balanced cooperation with rational decision-making, like **Optimistic** and **TitForTat**, tended to perform well overall. Highly aggressive or deceitful strategies could achieve high scores but were less consistent. Future simulations with more comprehensive testing can provide deeper insights.
