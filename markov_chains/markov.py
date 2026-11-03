import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray
import networkx as nx


class MarkovChain:
    #Note:
        # P is the same as π, pythons does not allow greek letters in variable names

    def __init__(self, P: ndarray, P0: ndarray):
        self.P = P
        self.P0 = P0

    @property
    def P(self)-> ndarray:
        return self._P

    @P.setter
    def P(self, value: ndarray)-> None:
        if not isinstance(value, np.ndarray):
            raise TypeError("Transition matrix must be a numpy ndarray.")
        if value.ndim != 2 or value.shape[0] != value.shape[1]:
            raise ValueError("Transition matrix must be square.")
        if not np.allclose(value.sum(axis=1), 1):
            raise ValueError("Rows of transition matrix must sum to 1.")
        self._P = value


    @property
    def P0(self)-> ndarray:
        return self._P0

    @P0.setter
    def P0(self, value: ndarray)-> None:
        if not isinstance(value, np.ndarray):
            raise TypeError("Initial probability vector must be a numpy ndarray.")
        if value.ndim != 1:
            raise ValueError("Initial probability vector must be a 1D array.")
        if not np.allclose(value.sum(), 1):
            raise ValueError("Initial probability vector must sum to 1.")
        self._P0 = value

    def stationary_probability(self)-> ndarray:
        """
        calculate the stationary probability.

        :return: stationary probability vector
        :rtype: ndarray
        """
        current_p: ndarray = self.P0.copy()
        last_p: ndarray = np.ones((self.P0.shape[0],)) 
        while not np.allclose(last_p, current_p):
            last_p = current_p
            current_p = current_p @ self.P 
        return current_p

        



    def calculate_probabilities(self, n: int)-> ndarray:
        """
        Calculate the vector of probability after n iteration.

        :param n: number of iterations
        :type n: int

        :return: probability vector after n iterations
        :rtype: ndarray
        """
        current_p: ndarray = self.P0.copy()
        for _ in range(n):
            current_p = current_p @ self.P
        return current_p

    def probability_at_state(self, n: int, state: int)-> float:
        """
        Calculate the probability of being in a state after n iterations.

        :param n: number of iterations
        :type n: int

        :param state: state index
        :type state: int

        :return: probability of being in the specified state after n iterations
        :rtype: float

        :raises ValueError: if the state index is out of bounds
        """
        lenght:int  = self.P0.shape[0]
        if state < 0 or state >= lenght:
            raise ValueError(f"State index must be between 0 and {lenght - 1}.")
        return self.calculate_probabilities(n)[state]

    def plot_probabilities(self, n: int)-> None:
        """
        Plot the evolution of state probabilities.

        :param n: number of iterations
        :type n: int

        :return: none
        :rtype: None
        """
        probability_vectors  = np.zeros((n + 1, self.P0.shape[0]))
        probability_vectors[0] = self.P0
        for i in range(1, n + 1):
            probability_vectors[i] = probability_vectors[i - 1] @ self.P

        plt.figure(figsize=(10, 6))
        for state in range(self.P0.shape[0]):
            plt.plot(probability_vectors[:, state], label=f'State {state}')
        plt.title('Evolution of Probabilities')
        plt.xlabel('Iteration')
        plt.ylabel('Probability')
        plt.legend()
        plt.show()


    def find_required_iterations(self,state: int, probability: float)-> int:
        """
        Find the minimum iterations needed to reach a given probability.

        :param state: state index
        :type state: int

        :param probability: target probability
        :type probability: float

        :return: minimum number of iterations
        :rtype: int

        :raises ValueError: if the state index is out of bounds
        :raises ValueError: if the probability is not between 0 and 1
        """
        lenght:int  = self.P0.shape[0]
        if state < 0 or state >= lenght:
            raise ValueError(f"State index must be between 0 and {lenght - 1}.")
        if probability < 0 or probability > 1:
            raise ValueError("Probability must be between 0 and 1.")

        current_p: ndarray = self.P0.copy()
        iterations: int = 0
        while current_p[state] < probability:
            current_p = current_p @ self.P
            iterations += 1
        return iterations


    def simulate_chain(self,)-> None:
        """
        Simulate a Markov chain.

        :return: none
        :rtype: None
        """
        nodes = []
        n1, n2 = self.P.shape

        for i in range(n1):
            for j in range(n2):
                if self.P[i, j] > 0:
                    nodes.append((i, j, self.P[i, j]))
        nodes = list(set([node for edge in nodes for node in edge[:2]]))
        edges = [(i, j, self.P[i, j]) for i in range(n1) for j in range(n2) if self.P[i, j] > 0]
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_weighted_edges_from(edges)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 6))
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', arrowsize=20)
        edge_labels = {(i, j): f"{self.P[i, j]:.2f}" for i, j in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title('Markov Chain Diagram')
        plt.show()

                

        