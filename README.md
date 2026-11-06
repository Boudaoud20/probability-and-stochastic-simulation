# Probability and Stochastic Simulation

This repository contains practical assignments completed as part of the **Probability and Stochastic Simulation** course.

The project focuses on implementing and studying probabilistic models and stochastic processes using Python. Each practical assignment is organized into its own module, containing the implementation, exercises, and related documentation.

## Repository Structure

```text
probability-and-stochastic-simulation/
├── markov_chains/
│   ├── __init__.py
│   ├── markov.py
│   ├── exercise_1.py
│   ├── exercise_2.py
│   ├── exercises.md
│   └── figure1.png
├── .gitignore
├── LICENSE
└── README.md
```

## Practical Assignments

### Markov Chains

This assignment introduces Markov chains and their applications.

It covers:
- Representing a Markov chain using a transition matrix.
- Computing stationary probabilities using iterative and linear algebra approaches.
- Calculating state probabilities after a given number of transitions.
- Visualizing transition diagrams and state probability evolution.
- Simulating random processes and estimating expected hitting times through repeated experiments.

#### Running the Exercises

Run the following commands from the repository's root directory:

**Exercise 1:**
```bash
python -m markov_chains.exercise_1
```

**Exercise 2:**
```bash
python -m markov_chains.exercise_2
```

Using `python -m` ensures that Python executes each exercise as a module within the package.

## Requirements

The project uses Python and the following libraries:

- NumPy — numerical computations and matrix operations.
- Matplotlib — plotting and visualization.
- NetworkX — transition diagram visualization.

Install the required libraries with:

```bash
pip install numpy matplotlib networkx
```

## Running the Project

1. Clone the repository.
2. Open a terminal in the repository's root directory.
3. Install the required dependencies.
4. Run the desired exercise using the commands listed above.
