/* 
this code is to construct a graph structure for implementing the BFS algorithm and find the shortest path between two nodes
this code idea is from https://www.geeksforgeeks.org/shortest-path-unweighted-graph/ and https://blog.nowcoder.net/n/164b413a558b447394896a469a59023c?from=nowcoder_improve
and I made some modification for this assigment
*/
#include <iostream>
#include <vector>
#include <list>
#include <climits>
#include "graph.h"
#include <queue>
#include <algorithm>

using namespace std;

Graph::Graph(int v) : v(v), graph(v + 1000, vector<int>()) {}

// this part of code's idea is from https://www.geeksforgeeks.org/shortest-path-unweighted-graph/ 
//and https://blog.csdn.net/alps1992/article/details/44795113 and i did some modification
vector<int> Graph::shortestPath(int start, int end) {
    vector<bool> visited(v + 1000, false);
    vector<int> distance(v + 1000, -1);
    vector<int> parent(v + 1000, -1);

    queue<int> q;
    q.push(start);
    visited[start] = true;
    distance[start] = 0;

    while (!q.empty()) {
        int curr = q.front();
        q.pop();

        for (int neighbor : graph[curr]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                distance[neighbor] = distance[curr] + 1;
                parent[neighbor] = curr;
                q.push(neighbor);

                if (neighbor == end) {
                    return res(parent, start, end);
                }
            }
        }
    }

    return {};
}

void Graph::addEdge(int start, int end) {
    graph[start].push_back(end);
    graph[end].push_back(start);
}

vector<int> Graph::res(const vector<int>& parent, int start, int end) {
    vector<int> path;
    int curr = end;
    while (curr != -1) {
        path.push_back(curr);
        curr = parent[curr];
    }
    reverse(path.begin(), path.end());
    return path;
}
