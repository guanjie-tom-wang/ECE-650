/* 
this code is to construct a graph structure for implementing the VERTEX COVER to CNF-SAT
this code idea is from https://github.com/xin-y/ECE-650---Methods-and-Tools-for-Software-Engineering/blob/master/project/ece650-prj.cpp
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
    if(vertices > 15){
        cerr << "CNF-SAT-VC: timeout" << endl;
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
            std::cout << "CNF-SAT-VC:" << " ";
            int size = result_paths[i].size();
            int point = 0;
            for (int vertex : result_paths[i]) {
                if(point < size - 1){
                    cout << vertex << ",";
                }
                point++;
            }
            cout << result_paths[i][size - 1] << endl;
            // cout << endl;
            return;
        }
    }
    cerr << "Error: UNSAT" << endl;
}
  std::vector<int> Vertex::APPROX_VC_1() {
    std::vector<int> vertex_cover;
    std::vector<std::vector<int>> local_graph = graph; // Copy of the graph

    while (!local_graph.empty()) {
        // Find the vertex with the highest degree
        std::vector<int>::size_type max_degree = 0;
        int max_vertex = -1;
        for (std::vector<std::vector<int>>::size_type i = 0; i < local_graph.size(); ++i) {
            if (local_graph[i].size() > max_degree) {
                max_degree = local_graph[i].size();
                max_vertex = i;
            }
        }

        if (max_vertex == -1) {
            break; // No vertices left
        }

        // Add this vertex to the vertex cover
        vertex_cover.push_back(max_vertex);

        // Remove all edges connected to this vertex
        local_graph[max_vertex].clear();
        for (auto& neighbors : local_graph) {
            neighbors.erase(std::remove(neighbors.begin(), neighbors.end(), max_vertex), neighbors.end());
        }
    }

    return vertex_cover;
}
    std::vector<int> Vertex::APPROX_VC_2() {
        std::vector<int> vertex_cover;
        std::vector<std::vector<int>> local_graph = graph; // Copy of the graph

        while (!local_graph.empty()) {
            // Pick an edge
            int u = -1, v = -1;
            for (std::vector<std::vector<int>>::size_type i = 0; i < local_graph.size(); ++i) {
                if (!local_graph[i].empty()) {
                    u = i;
                    v = local_graph[i][0];
                    break;
                }
            }

            if (u == -1 || v == -1) {
                break; // No edges left
            }

            // Add endpoints to the vertex cover (if not already included)
            if (std::find(vertex_cover.begin(), vertex_cover.end(), u) == vertex_cover.end()) {
                vertex_cover.push_back(u);
            }
            if (std::find(vertex_cover.begin(), vertex_cover.end(), v) == vertex_cover.end()) {
                vertex_cover.push_back(v);
            }

            // Remove all edges connected to these vertices
            local_graph[u].clear();
            local_graph[v].clear();
            for (auto& neighbors : local_graph) {
                neighbors.erase(std::remove(neighbors.begin(), neighbors.end(), u), neighbors.end());
                neighbors.erase(std::remove(neighbors.begin(), neighbors.end(), v), neighbors.end());
            }
        }

        return vertex_cover;
    }

