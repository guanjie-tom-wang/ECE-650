#include <iostream>
#include <sstream>
#include <vector>
#include <regex>
#include <list>
#include <queue>
#include <algorithm>
#include "graph.h"

using namespace std;

int main(int argc, char** argv) {
    regex vx(R"([V]\s-?\d+)");
    regex ex(R"([E]\s\{[\<-?\d+\,-?\d+\>\,*]+\})");
    regex ex1(R"([E]\s\{})");
    regex sx(R"([s]\s\d+\s\d+)");

    int v = -1;
    int startNode = 0;
    int endNode = 0;
    bool isVaildEdge = false;
    bool isReadedE = false;
    unique_ptr<Graph> graph;

    while (!std::cin.eof()){
        string line;
        getline(cin, line);
        if(line.empty()){
            continue;
        }
       
        if(!line.empty() && line.at(0) == 'V'){
            std::cout << line << std::endl;
            // if(graph != nullptr){
            //     delete graph;
            //     graph = nullptr;
            // } 
            
            isVaildEdge = false;
            isReadedE = false;

            if(regex_match(line, vx)){
                smatch matches;
                regex px(R"(\d+)");
                regex_search(line, matches, px);
                v =std::stoi(matches[0].str());
                if(v <= 1){
                    cerr << "Error: vertices must larger than 1" << endl;
                    v = 0;
                    continue;
                }
                // if(graph != nullptr){
                //     delete graph;
                //     graph = nullptr;
                // }
                graph = unique_ptr<Graph>( new Graph(v));

                continue;
            } else{
                cerr << "Error: input format error" << endl;
                continue;
            }
        }
            
        else if(!line.empty() && line.at(0) == 'E'){
            std::cout << line << std::endl;
            if(isReadedE){
                continue;
            }
            if(graph == nullptr){
                cerr << "Error: graph is not setted" << endl;
                continue;
            }
            if(regex_match(line, ex)){
                smatch matches;
                regex px(R"(-?\d+,-?\d+)");
                bool isBreak = false;
                if(isVaildEdge == false){
                    while (std::regex_search(line, matches, px)) {
                        for (const auto& match : matches) {
                            string delimiter = ",";
                            string number = match.str();
                            string first = number.substr(0, number.find(delimiter));
                            string second = number.substr(number.find(delimiter)+1);
                            int start = std::stoi(first);
                            int end = std::stoi(second);
                            if(start > v || end > v  || start == 0 || end == 0 || start < 0 || end < 0){
                                cerr << "Error: start node and end node must be smaller than the input vertices" << endl;
                                isBreak = true;
                            }
                        }
                        if(isBreak){
                            break;
                        }
                        for (const auto& match : matches) {
                            string delimiter = ",";
                            string number = match.str();
                            string first = number.substr(0, number.find(delimiter));
                            string second = number.substr(number.find(delimiter)+1);

                            int start = std::stoi(first);
                            int end = std::stoi(second);
                            graph->addEdge(start, end);
                            graph->addEdge(end, start);
                        }
                        line = matches.suffix().str();
                    }
                    if(!isBreak){
                        isVaildEdge = true;
                        isReadedE = true;
                    }
                    continue;
                } else{
                    continue;
                }
            } else if(regex_match(line, ex1)){
                isReadedE = true;
                isVaildEdge = true;
                continue;
            } else {
                cerr << "Error: input format error" << endl;
                continue;
            }
        } 
        else if (!line.empty() && line.at(0) == 's'){
            if(!isVaildEdge){
                cerr << "Error: graph is empty" << endl;
                continue;
            }
            if(regex_match(line, sx)){
                smatch matches;
                regex px(R"(\d+)");
                list<string> list;
                while (std::regex_search(line, matches, px)) {
                    for (const auto& match : matches) {
                        list.push_back(match.str());
                    }
                    line = matches.suffix().str();
                }
                startNode =std::stoi(list.front());
                list.pop_front();
                endNode = std::stoi(list.front());
                list.pop_front();
                if( startNode == endNode){
                    cout << startNode << endl;
                    continue;
                }
                if(startNode > v || endNode > v){
                    cerr << "Error: input error startNode and endNode must smaller than vertex" << endl;
                    continue;

                }
                vector<int> shortestPath = graph->shortestPath(startNode, endNode);
                for (vector<int>::size_type i = 0; i < shortestPath.size() - 1; i++){
                    cout << shortestPath[i] << "-";
                }
                if(shortestPath.size() > 0){
                    cout<<shortestPath[shortestPath.size() - 1]<<endl;
                }
                if(shortestPath.size() == 0){
                    cerr<<"Error: there is no path"<<endl;
                }

                continue;
            } else{
                cerr << "Error: input format error" << endl;
                continue;
            }
        }
        else {
            cerr << "Error: input format error" << endl;
            continue;
        }
    }
}
