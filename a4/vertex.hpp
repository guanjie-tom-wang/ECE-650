#pragma once

#include <iostream>
#include <vector>
#include <minisat/core/SolverTypes.h>
#include <minisat/core/Solver.h>

class Vertex {
private:
    
    int vertices;
    std::vector<std::vector<int>> graph;

    Minisat::Var toVar(int row, int column, int k);
    void reduceToSAT(int k, Minisat::Solver& solver);
    bool solve(Minisat::Solver& solver, int k);
    std::vector<int> getPath(Minisat::Solver& solver, int k);

public:
    Vertex (int v); 
   
    // Mutators
    void addEdge(int start, int end);
    void findMinimum();
   
};