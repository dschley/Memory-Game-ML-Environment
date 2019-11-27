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
 
 Before jumping into memory modules, I want to test this out with a simple LSTM with policy gradients 
 just to test the waters.  I'll consider a game a win if it is completed with less than double the optimal number of moves
 to solve a puzzle of a certain size.
 
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
        can more appropriately be compared to the memory at a per problem basis.
        - The current observation, last action taken, and resulting vector of the memory queue calculation 
        are fed into an LSTM based Actor-Critic network.
        - Could be a good candidate for this problem.  Could compare currently flipped card (current 
        observation) to a card it flipped recently (observation in the mem queue) and figure out that
        given it has seen the card currently before, which action did it take to uncover that card in the past
 
    - Method 4: Integrating Episodic Memory with Reservoir Sampling:
        - Has an external memory module that contains the n (or all n) most recent states with associated importance weights.
        - Has policy and value networks (actor critic) as well as a write network and query network.  The query network 
        outputs a vector the same shape as the states which is used to choose a past state from memory.  That memory, 
        along with the current state, is used to determine the action from the policy network.  The write network is responsible 
        for writing states into the memory module with weights associated to how likely it is to stay in memory.
        - Could possibly be used for this use case.  Seems similar to Masked Experience Memory in that it picks a memory
        to use in conjunction with the current state, however the sampling is slightly different and uses "reservoir sampling"
        rather than "closeness to current state"
        
    - Method 5: Neural Map:
        - This method is intended to give the agent an understanding of where it is in a 3D navigation environment that 
        only has the current position observable
        - Contains a memory map that has the dimensions FeatureDimension X x-Dimension X y-dimension, which maps every 
        x,y coordinate value.
        - Reading from the memory module is done by a CNN which is used with the current state to both make the decision
        based on the policy as well as update the memory map
        - Even though this is intended for 3D environments and "navigation", this could be used for this project because
        we have x,y coordinates, the environment is partially observable and having a "context" of where we are is sort of 
        equivalent in this case as "knowledge of uncovered tiles".  So far looking like one of the most promising but the most complicated.
 
    - Method 6: Memory, RL, and Inference Network (MERLIN):
        - Inspired by predictive sensory coding, hippocampal representation theory, and temporal context model and successor
        representation
        - Utilizes 2 networks, a policy net, and a memory based predictor (MBP). The MBP tries to get an accurate prediction
        of what the next state will be while the policy acts from the state, MBP output, and memory to determine an action
        - This is much more complex than I'm describing here but at the high level its mainly the interaction between those 
        components that drives this solution.  This seems like the best solution so far for this type of problem because 
        if the prediction is accurate, then it's simply just training the policy to match as if the environment was fully
        observable which is pretty simple.
        
    - Method 7: Memory Augmented Control Network (MACN):
        - This model is also intended for navigation in a partially observable environment
        - It observes the locally observable state through a CNN, and hands that off to a network that determines its value function. 
        This value is then used as the key to this observation in the memory.  The locally observed state's value from this
        and the raw feature output from the CNN are fed to a controller network that feeds into itself, a memory reading 
        network, as well as the policy network.  The memory network that is fed input from the controller feeds past outputs
        into itself as well as outputting to the policy network alongside the controller net.
        - The intention is to give both the currently observed state as well as the overall hidden state space some stake 
        in the decision process while also allowing them to influence each other.
        - This has potential to be a good solution, however I'm not sure how the value network will behave in this architecture
        for this problem because the rewards are so sparse and it doesn't take a long series of actions to accomplish a goal, only 2.
         
 An episodic memory structure may be what we need for this.  Giving an opportunity for past observations
 within the episode to have bearing on future decisions.  In order to make the memories more "positive" 
 and "stick around" better, maybe give a small reward for each card flip, big reward for successful match, 
 and negative reward for unsuccessful match.
 
 Ideally one architecture could be trained to play any size game without having to train it for each size scenario.