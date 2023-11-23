#include <vector>
using namespace std;
class Graph {
private:
    int v;
    vector<std::vector<int>> graph;

public:
    Graph(int v);
    void addEdge(int start, int end);
    vector<int> shortestPath(int start, int end);

private:
    vector<int> res(const vector<int>& parent, int start, int end);
};