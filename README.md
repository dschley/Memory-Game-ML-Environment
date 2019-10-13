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
 Ideally one architecture could be trained to play any size game without having to train it for each size scenario.