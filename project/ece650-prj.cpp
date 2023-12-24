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
#include <pthread.h>
#include <time.h>  

using namespace std;
pthread_mutex_t lock;
pthread_cond_t cond;
int current_thread = 1;
// Thread function prototypes
int v = -1;

void* threadCNF_SAT_VC(void* args) {
    pthread_mutex_lock(&lock);
    while (current_thread != 1) {
        pthread_cond_wait(&cond, &lock);
    }
    
    clockid_t clock_id;
    struct timespec start, end;
    pthread_getcpuclockid(pthread_self(), &clock_id);
    clock_gettime(clock_id, &start);
    auto* vertices = static_cast<Vertex*>(args);
    // Existing thread logic
    vertices->findMinimum();
    
    // Get end time
    clock_gettime(clock_id, &end);

    // Calculate and print the elapsed time in milliseconds
    // double elapsed_time = (end.tv_sec - start.tv_sec) * 1e3 + (end.tv_nsec - start.tv_nsec) / 1e6;
    // std::cout << "Thread CNF-SAT-VC Time: " << elapsed_time << " ms" << std::endl;
    current_thread = 2;
    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&lock);
    return nullptr;
}

void* threadAPPROX_VC_1(void* args) {
    pthread_mutex_lock(&lock);
    while (current_thread != 2) {
        pthread_cond_wait(&cond, &lock);
    }

    auto* vertices = static_cast<Vertex*>(args);
    clockid_t clock_id;
    struct timespec start, end;
    pthread_getcpuclockid(pthread_self(), &clock_id);
    clock_gettime(clock_id, &start);

    // Example implementation
    // Replace with actual APPROX-VC-1 logic from your Vertex class
    auto result = vertices -> APPROX_VC_1();
    std::cout << "APPROX-VC-1:" << " ";
    int size = result.size();
    int point = 0;
    for (int vertex : result) {
        if(point < size - 1){
            cout << vertex << ",";
        }
        point++;
    }
    cout << result[size - 1] << endl;
    clock_gettime(clock_id, &end);

    // Calculate and print the elapsed time in milliseconds
    // double elapsed_time = (end.tv_sec - start.tv_sec) * 1e3 + (end.tv_nsec - start.tv_nsec) / 1e6;
    // std::cout << "Thread APPROX-VC-1 Time: " << elapsed_time << " ms" << std::endl;
    current_thread = 3;
    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&lock);
    return nullptr;
}

void* threadAPPROX_VC_2(void* args) {
    pthread_mutex_lock(&lock);
    while (current_thread != 3) {
        pthread_cond_wait(&cond, &lock);
    }

    auto* vertices = static_cast<Vertex*>(args);
    clockid_t clock_id;
    struct timespec start, end;
    pthread_getcpuclockid(pthread_self(), &clock_id);
    clock_gettime(clock_id, &start);

    // Example implementation
    // Replace with actual APPROX-VC-2 logic from your Vertex class
    auto result = vertices -> APPROX_VC_2();
    std::cout << "APPROX-VC-2:" << " ";
    int size = result.size();
    int point = 0;
    for (int vertex : result) {
        if(point < size - 1){
            cout << vertex << ",";
        }
        point++;
    }
    cout << result[size - 1] << endl;
    clock_gettime(clock_id, &end);

    // Calculate and print the elapsed time in milliseconds
    // double elapsed_time = (end.tv_sec - start.tv_sec) * 1e3 + (end.tv_nsec - start.tv_nsec) / 1e6;
    // std::cout << "Thread APPROX-VC-2 Time: " << elapsed_time << " ms" << std::endl;
    pthread_mutex_unlock(&lock); // No need to set current_thread or broadcast
    return nullptr;
}



int main(int argc, char** argv) {
    pthread_mutex_init(&lock, NULL);
    pthread_cond_init(&cond, NULL);
    regex vx(R"([V]\s-?\d+)");
    regex ex(R"([E]\s\{[\<-?\d+\,-?\d+\>\,*]+\})");
    regex ex1(R"([E]\s\{})");
    regex sx(R"([s]\s\d+\s\d+)");

    bool isVaildEdge = false;
    bool isReadedE = false;
    Vertex vertices(0);


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
                // cout << "V " <<v << endl;
                
                vertices =  Vertex(v);
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
            // if(vertices == nullptr){
            //     cerr << "Error: graph is not setted" << endl;
            //     continue;
            // }
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
                            vertices.addEdge(start, end);
                        }

                        line = matches.suffix().str();
                    }
                    if(!isBreak){
                        isVaildEdge = true;
                        isReadedE = true;
                        pthread_t thread1, thread2, thread3;
                        pthread_create(&thread1, NULL, threadCNF_SAT_VC, (void*)&vertices);
                        pthread_create(&thread2, NULL, threadAPPROX_VC_1, (void*)&vertices);
                        pthread_create(&thread3, NULL, threadAPPROX_VC_2, (void*)&vertices);
                       
                        pthread_join(thread1, NULL);
                        pthread_join(thread2, NULL);
                        pthread_join(thread3, NULL);
                        current_thread = 1;
                        
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
    pthread_mutex_destroy(&lock);
    pthread_cond_destroy(&cond);
    return 0;
}
