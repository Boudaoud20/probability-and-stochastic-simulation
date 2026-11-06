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
        for row in value:
            for element in row:
                if element < 0 or element > 1:
                    raise ValueError("Transition matrix elements must be between 0 and 1.")
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
        for element in value:
            if element < 0 or element > 1:
                raise ValueError("Initial probability vector elements must be between 0 and 1.")
        if value.shape[0] != self.P.shape[0]:
            raise ValueError("Initial probability vector must have the same length as the number of states.")
        if not np.allclose(value.sum(), 1):
            raise ValueError("Initial probability vector must sum to 1.")
        self._P0 = value

    def _calculate_probability_stationary_iterative_approach(self,max_iter:int = 90000)->ndarray:
        """
        calculate the stationary probability using iterarive approach.

        :return: stationary probability vector
        :rtype: ndarray
        :raises RuntimeError: if the stationary probability does not converge within the maximum number of iterations
        """
        current_p: ndarray = self.P0.copy()
        last_p: ndarray = np.ones((self.P0.shape[0],)) 
        for _ in range(max_iter):
            if np.allclose(last_p, current_p):
                return current_p
            last_p = current_p
            current_p = current_p @ self.P
        raise RuntimeError("Stationary probability did not converge.")

    def _calculate_probability_stationary_linear_approach(self, )->ndarray:
        """
        calculate the stationary probability using linear approach.

        :return: stationary probability vector
        :rtype: ndarray
        """
        n:int = self.P.shape[0]
        B:ndarray = np.array([0 for _ in range(n)]+ [1])
        B = B.reshape((n+1, 1))
        A:ndarray = np.vstack([self.P.T - np.eye(n), np.ones((1, n))])
        return np.linalg.solve(A.T @ A, A.T @ B).flatten()
    
    def stationary_probability(self, method:str="iterative")-> ndarray:
        """
        calculate the stationary probability.

        :return: stationary probability vector
        :rtype: ndarray
        """
        if not method in ["iterative", "linear"]:
            raise ValueError(f"{method} is not exist as method of solving.")

        if method == "iterative":
            return self._calculate_probability_stationary_iterative_approach()
        elif method == "linear":
            return self._calculate_probability_stationary_linear_approach()
        else:
            pass


    def calculate_probabilities(self, n: int,method:str = "iterative" )-> ndarray:
        """
        Calculate the vector of probability after n iteration.

        :param n: number of iterations
        :type n: int

        :return: probability vector after n iterations
        :rtype: ndarray

        :raises ValueError: if n is not a positive integer
        :raises ValueError: if method is not "iterative" or "matrix_power"
        """
        if n < 0:
            raise ValueError("Number of iterations must be a positive integer.")

        if not method in ["iterative", "matrix_power"]:
            raise ValueError(f"{method} is not exist as method of solving.")
        current_p: ndarray = self.P0.copy()
        if method =="iterative":
            for _ in range(n):
                current_p = current_p @ self.P
            return current_p
        else:
            return self.P0 @ np.linalg.matrix_power(self.P, n)

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

        :raises ValueError: if n is not a positive integer
        """
        if n < 1:
            raise ValueError("Number of iterations must be a positive integer.")
        
        probability_vectors  = np.zeros((n + 1, self.P0.shape[0]))
        probability_vectors[0] = self.P0
        for i in range(1, n + 1):
            probability_vectors[i] = probability_vectors[i - 1] @ self.P

        plt.figure(figsize=(10, 6))
        for state in range(self.P0.shape[0]):
            plt.plot(probability_vectors[:, state], label=f'State {state+1}')
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
        if state < 1 or state > lenght:
            raise ValueError(f"State index must be between 1 and {lenght}.")
        if probability < 0 or probability > 1:
            raise ValueError("Probability must be between 0 and 1.")

        current_p: ndarray = self.P0.copy()
        iterations: int = 0
        while current_p[state-1] < probability:
            current_p = current_p @ self.P
            iterations += 1
        return iterations


    def plot_transition_diagram(self,)-> None:
        """
        Plot the transition diagram of the Markov chain.

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

                

        