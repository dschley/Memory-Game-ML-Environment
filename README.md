# Memory Game

My intentions with this game is to have an environment to train ML models to play a game that involves memorization.

### How to play

This game can be played by humans as well through the console by running `play_from_console()` with an instance of the Game object.

Otherwise, you can just interact with the game and check the state with the functions: 
 - `step()`
 - `board_state_f()`
 - `is_done()`
 
 As well as the properties of the game object:
 - `score`
 - `board_length`
 - `num_turns`
 - `max_turns`
 
 
 ### ML thoughts
 
 My first idea is to make a neural network based reinforcement learning algorithm to master this game. 
 I definitely think some sort of recurrent architecture is needed to convey memory such as an LSTM,
 however I am still contemplating whether or not to use a CNN to read in the game state.
 My belief is that a CNN could decouple the places that it sees the cards placed in training scenarios
 so that it could just understand locality but not get confused by the randomness of the card placements.
 
 Considering usage of actor-critic/ddpg for the actual training but this may not be possible with memory considerations.
 
 Upon further research, actor-critic may not be the best and the memory problem is its own sub-domain of RL. 
 Need to take into consideration things such as considering this a non-markovian task 
 as well as considering the perceptual aliasing issue.
 
 Examining several papers that address these issues:
 - [A SHORT SURVEY ON MEMORY BASED REINFORCEMENT LEARNING](https://arxiv.org/pdf/1904.06736.pdf)
    - Method 1: Model Free Episodic Control:
        - Keep a table of (state, action) => reward mappings to consult in order to determine the next action. 
        The (s,a) pairs with the highest rewards are inserted into the map, kicking out older observations,
        and when at a particular state, determines action based on value of (s,a) mapping, using average of 
        nearest mapped neighbors to determine that value if that state hasn't been observed yet.
        - Doesn't feel very episodic, or that it could apply to this problem.
        
    - Method 2: Neural Episodic Control:
        - Each action has a map of keys (states vectorized by cnn's) called h 
        to values (list of Q(s,a) for all states which took said action whose state was vectorized to h)
        - Action is determined by evaluating memory maps (specifically the Q(s,a)'s in index h) 
        of each action to see which ones have the best results.
        - Feels like these solutions so far are improvements to memory and learning process rather than
        incorporating memory and learned things specific to the episode to the decision process
        
    - Method 3: Masked Experience Memory:
        - Has a Memory queue that is added to for each observation and reads from via a focused view of it, 
        paramaterized by a trainable _z_, and calculates a vector based on comparing the current observation
        and its distance to each observation in the focused view of the memory queue.
        - Gradient descent trains _z_ which is the sharpness of focus within the memory so the current observation
        can more appropriately compared to the memory at a per problem basis.
        - The current observation, last action taken, and resulting vector of the memory queue calculation 
        are fed into an LSTM based Actor-Critic network.
        - Could be a good candidate for this problem.  Could compare currently flipped card (current 
        observation) to a card it flipped recently (observation in the mem queue) and figure out that
        given it has seen the card currently before, which action did it take to uncover that card in the past
 
 
 An episodic memory structure may be what we need for this.  Giving an opportunity for past observations
 within the episode to have bearing on future decisions.  In order to make the memories more "positive" 
 and "stick around" better, maybe give a small reward for each card flip, big reward for successful match, 
 and negative reward for unsuccessful match.
 
 Ideally one architecture could be trained to play any size game without having to train it for each size scenario.