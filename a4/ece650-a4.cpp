#include <iostream>
#include <sstream>
#include <vector>
#include <regex>
#include <list>
#include <queue>
#include <algorithm>
#include "vertex.hpp"
#include <minisat/core/SolverTypes.h>
#include <minisat/core/Solver.h>


using namespace std;

int main(int argc, char** argv) {
    regex vx(R"([V]\s-?\d+)");
    regex ex(R"([E]\s\{[\<-?\d+\,-?\d+\>\,*]+\})");
    regex ex1(R"([E]\s\{})");
    regex sx(R"([s]\s\d+\s\d+)");

    int v = -1;
    bool isVaildEdge = false;
    bool isReadedE = false;
    unique_ptr<Vertex> vertices;


    while (!std::cin.eof()){
        string line;
        getline(cin, line);
        if(line.empty()){
            continue;
        }
        if(!line.empty() && line.at(0) == 'V'){
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
                vertices = unique_ptr<Vertex>( new Vertex(v));
                continue;
            } else{
                cerr << "Error: input format error" << endl;
                continue;
            }
        }
            
        else if(!line.empty() && line.at(0) == 'E'){
            if(isReadedE){
                continue;
            }
            if(vertices == nullptr){
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
                            vertices->addEdge(start, end);
                        }

                        line = matches.suffix().str();
                    }
                    if(!isBreak){
                        isVaildEdge = true;
                        isReadedE = true;
                        vertices->findMinimum();
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
        else {
            cerr << "Error: input format error" << endl;
            continue;
        }
    }
}
