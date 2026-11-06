from markov import MarkovChain
import numpy as np
from numpy import ndarray
import time

maze:dict ={
    "A": ["A","B","B"],
    "B": ["B","B","B","B","B","A","C"],
    "C":["A", "B","B","B","B","B","B","B","C","C","C","C"]
}
states_n: int = len(maze)

P0: ndarray = np.array([1/3, 1/3, 1/3])

def from_state_to_index(state: str) -> int:
    """
    Converts a state to index.

    :param state: The state to convert.
    :type state: str

    :return: The index of the state in the transition matrix.
    :rtype: int
    """
    d:dict = {"A": 0, "B": 1, "C": 2}
    return d[state]

def build_transition_matrix() -> ndarray:
    """
    Builds the transition matrix.

    :return: The transition matrix.
    :rtype: ndarray
    """
    matrix:ndarray = np.zeros((states_n, states_n))
    for current_s, next_s in maze.items():
        if not next_s:
            matrix[from_state_to_index(current_s)][from_state_to_index(current_s)] = 1
            continue
        repetition_c: dict = {'A': 0, 'B': 0, 'C': 0}
        for state in next_s:
            repetition_c[state] += 1
        length: int = len(next_s)
        for s in next_s:
            matrix[from_state_to_index(current_s)][from_state_to_index(s)] = repetition_c[s] / length
    return matrix


def random_experiment_without_markov():
    """
    Simulates a random experiment without using Markov chains.

    :return: none
    :rtype: None
    """
    current_state:str  = "A"
    while True:
        next_states:list = maze[current_state]
        if not next_states:
            break
        current_state = np.random.choice(next_states)
        if current_state == "C":
            break


if __name__ == "__main__":
    transition_matrix:ndarray = build_transition_matrix()
    markov_chain: MarkovChain = MarkovChain(P=transition_matrix, P0=P0) #1
    markov_chain.plot_transition_diagram()
    print("\n\n1. Transition Matrix:\n", markov_chain.P)

    stationary_vector_m1: ndarray = markov_chain.stationary_probability()#2
    print("\n\n2. Stationary Vector using iteration approach:\n", stationary_vector_m1)

    stationary_vector_m2: ndarray = markov_chain.stationary_probability(method="linear")#3
    print("\n\n3. Stationary Vector using linear approach:\n", stationary_vector_m2)

    vector_p: ndarray = markov_chain.calculate_probabilities(n=20,)#4
    print("\n\n4. Probability Vector after 20 steps:\n", vector_p)

    markov_chain.plot_probabilities(n=20,)#5

    start_time: float = time.time()
    random_experiment_without_markov()#6
    end_time: float = time.time()
    print(f"\n\n6. Time taken for random experiment without Markov chains: {(end_time - start_time)/60:e} minutes",)





