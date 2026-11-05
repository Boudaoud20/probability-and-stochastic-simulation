# Markov Chains

**Author:** Bachir Bouiadjra Rochdi
**Faculty of Exact Sciences, Computer Science Department**

## Contents

- [Exercise 1 – The mouse in the maze](#exercise-1)
- [Exercise 2 – The internet user and three websites](#exercise-2)
- [Tools](#tools)

---

## Exercise 1

### Problem statement

A mouse moves through the maze shown in Figure 1. Initially, it is in cell 1. Every minute, it changes cell by choosing, with equal probability, one of the adjacent cells. As soon as it reaches the food (cell 4), it stays there.

```text
              +-------------+-------------+
              |           2 |           4 |
              |             |     food    |
              |                           |
              |             |             |
+-------------+-----   -----+----   ------+
|           5 |           1 |           3 |
|  mouse hole |    mouse    |             |
|                                         |
|             |             |             |
+-------------+-------------+-------------+
```

*Figure 1. The maze in which the mouse lives.*
*(Walls are drawn with `+`, `-` and `|`; gaps in the walls are the doors between adjacent cells. The mouse starts in cell 1.)*

### Questions

**(1)** Give the transition diagram and the stochastic matrix $\Pi$.

**(2)** Compute the stationary probability vector $P^\star$.

**(3)** To compute the stationary probability vector, we have:

$$P^\star = P^\star \Pi$$

$$P^\star(\Pi - I) = \begin{bmatrix} 0 & 0 & \cdots & 0 \end{bmatrix} = \mathbf{0}$$

$$(\Pi^T - I)\,P^{\star T} = \mathbf{0}^T$$

$$\begin{bmatrix} 1 & 1 & \cdots & 1 \end{bmatrix} P^{\star T} = 1$$

$$\begin{bmatrix} \Pi^T - I \\ 1 \;\; 1 \;\; \cdots \;\; 1 \end{bmatrix} P^{\star T} = \begin{bmatrix} \mathbf{0}^T \\ 1 \end{bmatrix}$$

($T$ denotes the transpose of a vector or matrix.) We thus obtain a system of equations $Ax = B$.

- **(a)** Write a Python function that computes the vector $P^\star$ from $\Pi$.
  (Use the NumPy function `np.linalg.solve(A.T @ A, A.T @ B)` to find $P^{\star T}$.)
- **(b)** Compare with the result obtained in (2).

**(4)** Starting from the relation $P_{n+1} = P_n \Pi$, write a Python function that takes as input the initial probability vector $P_0$ and the number of iterations $n$, and returns the vector $P_n$. For $n$ large enough, recover the results of (2) and (3.a).

**(5)** Plot $P_n$ as a function of $n$ on the same graph. Analyze this graph.
(Use the functions `pyplot.plot` and `pyplot.show()` from the `matplotlib` library.)

**(6)** Compute the number of minutes the mouse needs to reach the food with a probability of 0.98.

**(7)** We want to compute the mean time the mouse needs to reach the kitchen. To achieve this, simulate this random experiment in Python (without using the notions of Markov chains).



---

## Exercise 2

### Problem statement

After submitting a query, an internet user may go to one of three sites: A, B or C.

- Site A contains one link to itself and two links to B.
- Site B has 5 links to itself, one to A and one to C.
- Site C has one link to A, 7 links to B and 4 to C.

At the start, the user chooses one of the three sites at random. Afterwards, the probability of moving from a site (at time $n$) to another (at time $n+1$) is proportional to the number of links from the first site to the second.

### Questions

**(1)** Give the transition diagram and the stochastic matrix $\Pi$.

**(2)** Compute the stationary probability vector $P^\star$.

**(3)** Recover $P^\star$ by answering questions (3.a) and (3.b) of [Exercise 1](#exercise-1).

**(4)** Redo questions (4) and (5) of [Exercise 1](#exercise-1).

**(5)** We want to compute the mean time needed for the internet user, initially on site A, to reach site C. To achieve this, simulate this random experiment in Python (without using the notions of Markov chains).

---

## Tools

- Python 3
- `numpy`
- `matplotlib`
- `networkx`
