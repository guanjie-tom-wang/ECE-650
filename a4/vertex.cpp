/* 
this code is to construct a graph structure for implementing the VERTEX COVER to CNF-SAT
this code idea is from https://github.com/adkulas/ece650_assignment4 
and I made huge modifications for my work
*/
#include <iostream>
#include <vector>
#include <list>
#include <climits>
#include <chrono>
#include "vertex.hpp"
#include <queue>
#include <algorithm>
#include <minisat/core/SolverTypes.h>
#include <minisat/core/Solver.h>

using namespace std;

Vertex::Vertex(int v) : vertices(v), graph(v + 1, vector<int>()) {}

void Vertex::addEdge(int start, int end) {
    graph[start].push_back(end);
    graph[end].push_back(start);

}

// Private
Minisat::Var Vertex::toVar(int vertex, int position, int k) {
    return (vertex - 1) * k + position;
}
void Vertex::reduceToSAT(int k,Minisat::Solver& solver) {
    // 1. At least one vertex is in each position of the cover.
    for (int i = 0; i <= k; i++) {
        Minisat::vec<Minisat::Lit> clause;
        for (int j = 1; j <= vertices; j++) {
            clause.push(Minisat::mkLit(toVar(j, i, k)));
        }
        solver.addClause(clause);
    }

    // 2. Different positions have different vertices.
    for (int m = 1; m <= vertices; m++) {
        for (int p = 0; p <= k; p++) {
            for (int q = p + 1; q <= k; q++) {
                solver.addClause(~Minisat::mkLit(toVar(m, p, k)), ~Minisat::mkLit(toVar(m, q, k)));
            }
        }
    }

    // 3. Different vertices can't occupy the same position.
    for (int m = 0; m <= k; m++) {
        for (int p = 1; p <= vertices; p++) {
            for (int q = p + 1; q <= vertices; q++) {
                solver.addClause(~Minisat::mkLit(toVar(p, m, k)), ~Minisat::mkLit(toVar(q, m, k)));
            }
        }
    }

    // 4. Each edge in the original graph must be incident to at least one vertex in the cover.
    for (int i = 1; i <= vertices; i++) {
        for (int j : graph[i]) {
            Minisat::vec<Minisat::Lit> clause;
            for (int p = 1; p <= k; p++) {
                clause.push(Minisat::mkLit(toVar(i, p, k)));
                clause.push(Minisat::mkLit(toVar(j, p, k)));
            }
            solver.addClause(clause);
        }
    }
}


bool Vertex::solve(Minisat::Solver& solver, int k) {
    for (int r = 1; r <= vertices; r++) {
        for (int c = 0; c <= k; c++) {
            solver.newVar();
        }
    }

    // Solve the SAT problem
    reduceToSAT(k, solver);
    auto sat = solver.solve();
    
    return sat;
}

vector<int> Vertex::getPath(Minisat::Solver& solver, int k) {
    vector<int> path;
    
    for (int r = 1; r <= vertices; r++) {
        for (int c = 1; c <= k; c++) {
            Minisat::Var var = toVar(r, c, k);
            if (solver.modelValue(var) == Minisat::l_True) {
                path.push_back(r);
            }
        }      
    }
    
    sort(path.begin(), path.end());
    return path;
}

void Vertex::findMinimum() {
    if (graph.empty()) {
        cerr << "Error: No Edges Entered to Graph" << endl;
        return;
    }
    int results[vertices];  //0 is UNSAT, 1 is SAT, -1 is undefined where index is k or vertex cover length
    std::vector<int> result_paths[vertices];
    // Linear Search
    std::fill_n(results, vertices, -1);
    for (int i = 0; i < vertices; i++) {
        Minisat::Solver solver;
        results[i] = solve(solver, i);
        if (results[i] == 1) {
            result_paths[i] = getPath(solver, i);
        }
    }
    

    for (int i = 0; i < vertices; i++) {
        if (results[i] == 1) {
            for (int vertex : result_paths[i]) {
                cout << vertex << " ";
            }
            cout << endl;
            return;
        }
    }
    cerr << "Error: UNSAT" << endl;
}