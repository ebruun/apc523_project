# Graph Realizations

Nonlinear root solver for rigid graph realizations and structural analysis of resulting assemblies by the direct stiffness method

Repository for APC523: Numerical Algorithms for Scientific Computing - Final Project

Edvard P.G. Bruun, Isabel M. de Oliveira

Instructor: Prof. Gregory W. Hammett

Princeton University, Spring 2021

## Executive summary

Minimally rigid graphs (called Laman graphs) are defined as graphs that have the least amount of edges that are required for rigidity. This means that removing any node or edge would result in a flexible graph, which has an infinite many potential configurations. From a structural engineering perspective, there is an interesting connection between graph theory and the design of truss and space frame structures. For example, an isomorphic graph (i.e., 1 to 1 mapping between a graph and the elements of a structure) can be created as a representation of a truss structure. A topological analysis of the graph can then be used to determine whether the underlying structure is stable or not, that is, without using any form of structural analysis. Laman graphs can be characterized through their assembly, where every minimally rigid graph can be built up starting from a single edge using a specific rule-set. In this project, we use this rule-set to generate rigid graphs. We are also interested in different configurations (or realizations) of these graphs, so we will explore how the same set of elements can produce different structures. To do this task, we use nonlinear solvers such as Newton-Raphson and Gradient Descent, and compare how these methods perform. Backtracking is used in to avoid overshoots in the iterations leading to a possible solution (i.e., each new iteration is guaranteed to reduce the error). We expect that the initial guess will highly influence the result. Additionally, we are interested in analysing the resulting graph with a finite element model of truss bar elements. Truss elements only carry axial loads, and simulate a structure with pinned connections. To conduct this analysis, we must solve a system of linear equations composed by the stiffness matrix, a vector of unknown displacements, and the force vector. If the provided graphs from the previous analysis are rigid, then we will expect only to find positive definite stiffness matrices. Hence, the stiffness matrix may be inverted to find a solution. Furthermore, we will compare other methods of solving systems of linear equations, such as LU Decomposition, Biconjugate Gradient, and GMRES.

The project is divided into two main parts: (1) graph realizations and nonlinear solvers; and (2) FEM truss solver and a comparison of linear solvers. Moving forward, it will be interesting to use both parts of this project to find which graph realizations are the most efficient according to a given goal. For example, which graph realization provides the smallest deflection to an applied load and given support conditions? Can we include the FEM solver into the Newton-Raphson steps to weight the solution for one graph realization or another? This project will provide the first steps to achieve further results in the design of truss-like structures.

## Getting Started

The package requirements are Autograd, Networkx, Numpy, and SciPy. To create a conda environment...

    * with a Mac, use:

`conda env create -f environment.yml`

    * with Windows, use:

`conda create --name APC523 --file requirements.txt`

Then, activate the environment using:

`conda activate APC523`

### Part 1: Graphs
To run an iteration on a medium size graph, just run `python main.py`, the iterations will be shown in a new matplotlib window. To change the options, see instructions in that same file.

Turn output plots on and off as needed, note that GIFs take a long time to create for analyses over 20 iterations. There are several example output GIFs found in the output folder, new outpit will be saved here. There are three predefined input files that can be run, turn these on/off in the package definition portion of the main.py file.

### Part 2: FEM

To run the script with a simple truss with three nodes and two elements, run `python fem_analysis.py`.

To change the settings, such as the material properties or the graph example, follow instructions in the comments of te scrip example in  `fem_analysis.py`. Two other input graphs are available through switching Options 1, 2, and 3 in that same file.
