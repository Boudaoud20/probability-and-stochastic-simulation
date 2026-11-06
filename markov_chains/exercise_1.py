from markov import MarkovChain
import numpy as np
from numpy import ndarray
import time


maze:dict = {
    1: [2, 3, 5],
    2: [1, 4],
    3: [1, 4],
    4: [],
    5: [1]
}
start_s:int = 1

states_n: int = len(maze)
P0:ndarray = np.zeros((states_n,))
P0[start_s-1] = 1



def build_transition_matrix() -> ndarray:
    """
    Builds the transition matrix.

    :return: The transition matrix.
    :rtype: ndarray
    """
    matrix:ndarray = np.zeros((states_n, states_n))
    for current_s, next_s in maze.items():
        if not next_s:
            matrix[current_s-1][current_s-1] = 1
            continue
        probability:float = 1/len(next_s)
        for s in next_s:
            matrix[current_s-1][s-1] = probability
    return matrix

transition_matr:ndarray = build_transition_matrix()

def random_experiment_without_markov():
    """
    Simulates a random experiment without using Markov chains.

    :return: none
    :rtype: None
    """
    current_state:int  = start_s
    while True:
        next_states:list = maze[current_state]
        if not next_states:
            break
        current_state = np.random.choice(next_states)

if __name__ == "__main__":
    markov_chain: MarkovChain = MarkovChain(P=transition_matr, P0=P0) #1
    markov_chain.plot_transition_diagram()
    print("1. Transition Matrix:\n", markov_chain.P)

    stationary_vector_m1: ndarray = markov_chain.stationary_probability(method="linear")#2
    print("\n\n2. Stationary Probability Vector:\n", stationary_vector_m1)

    stationary_vector_m2: ndarray = markov_chain.stationary_probability()#3
    print("\n\n3. Stationary Probability Vector using iteration approach:\n", stationary_vector_m2)

    vector_p: ndarray = markov_chain.calculate_probabilities(n=50,)#4
    print("\n\n3. Probability Vector after 50 steps:\n", vector_p)

    markov_chain.plot_probabilities(n=50,)#5

    start_time: float = time.time()#6
    iteration_num = markov_chain.find_required_iterations(state=4, probability=0.98)
    end_time: float = time.time()
    print(f"\n\n6. Number of iterations required to reach at least 0.98 probability of being in state 4: {iteration_num}")
    print(f"Time taken: {(end_time - start_time)/60:e} minutes")


    start_time: float = time.time()#7
    random_experiment_without_markov()
    end_time: float = time.time()
    print(f"\n\n7. Time taken for random experiment without Markov chains: {(end_time - start_time)/60:e} minutes")

















