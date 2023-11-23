#include<vector>
#include <unistd.h>
#include <signal.h>
#include <iostream>
#include <getopt.h>
#include <sys/wait.h> 
#include <fcntl.h>

int main (int argc, char **argv) {
     //below code's idea is from https://git.uwaterloo.ca/ece650-f23/cpp/-/blob/master/using_getopt.cpp?ref_type=heads and https://github.com/adkulas/ece650_assignment3/blob/master/a3-ece650.cpp
	std::string ss;
    int s = 10; // num of streets randint [2,k] k >=2
	std::string nn;
    int n = 5; //num of line segs per street rand int [1,k] k >= 1
	std::string ll;
    int l = 5; //wait rand time rand int [5,k] k>=5
	std::string cc;
    int c = 20; //xy coord range rand int [-k,k] k>=1
    int cl;
    // expected options are '-s value', '-n value', '-l value', and '-c value'
    while ((cl = getopt(argc, argv, "s:n:l:c:?")) != -1) {
        switch (cl)
        {
        case 's':
            ss = optarg;
            s = atoi(ss.c_str());
            if(s < 2) {
                std::cerr << "Error: s must have value >= 2" << std::endl;
                return 1;
            }
            break;

        case 'n':
            nn = optarg;
            n = atoi(nn.c_str());
            if(n < 1) {
                std::cerr << "Error: n must have value >= 1" << std::endl;
                return 1;
            }
            break;

        case 'l':
            ll = optarg;
            l = atoi(ll.c_str());
            if(l < 5) {
                std::cerr << "Error: l must have value >= 5" << std::endl;
                return 1;
            }
            break;

        case 'c':
            cc = optarg;
            c = atoi(cc.c_str());
            if(c < 1) {
                std::cerr << "Error: c must have value >= 1" << std::endl;
                return 1;
            }
            break;
        
        case '?':
            std::cerr << "Error: unknown option: " << optopt << std::endl;
            return 1;
        default:
            return 0;
        }
	}
    std::vector<pid_t> kids;
    pid_t child_pid;    
    // create pipes a1
    int a1[2];
    pipe(a1);
    // create pipes a2
    int a2[2];
    pipe(a2);
    
    // RUN RGEN  
    child_pid = fork();
    if (child_pid == 0) {
        // redirect stdout to the pipe
        dup2(a1[1], STDOUT_FILENO);
        close(a1[0]);
        close(a1[1]);
        
        execv("rgen", argv);
        perror ("Error: Could not execute rgen");
        return 1;
    } 
    else if (child_pid < 0) {
        std::cerr << "Error: could not fork Rgen" << std::endl;
        return 1;  
    }
    kids.push_back(child_pid);

    
    // RUN a1
    child_pid = fork();
    if (child_pid == 0) {
        // redirect stdin from the pipe
        dup2(a1[0], STDIN_FILENO);
        close(a1[1]);
        close(a1[0]);
        // redirect stdout from the pipe
        dup2(a2[1], STDOUT_FILENO);
        close(a2[0]);
        close(a2[1]);
        argv[0] = (char *)"python3";
        argv[1] = (char *)"ece650-a1.py";
        argv[2] = nullptr;
        execvp("python3", argv);
        perror ("Error: Could not execute ece650-a1.py");
        return 1;
    } 
    else if (child_pid < 0) {
        std::cerr << "Error: could not fork ece650-a1.py" << std::endl;
        return 1;  
    }
    kids.push_back(child_pid);

    // RUN a2
    child_pid = fork();
    if (child_pid == 0) {
        // redirect stdin from the pipe
        dup2(a2[0], STDIN_FILENO);
        close(a2[1]);
        close(a2[0]);
        argv[0] = (char*)"ece650-a2";
	    argv[1] = nullptr;
        execv("ece650-a2", argv);
        perror ("Error: Could not execute ece650-a2.cpp");
        return 1;
    } 
    else if (child_pid < 0) {
        std::cerr << "Error: could not fork ece650-a2.cpp" << std::endl;
        return 1;  
    }
    kids.push_back(child_pid);

    child_pid = fork();
    if (child_pid == 0) {
        dup2(a2[1], STDOUT_FILENO);
        close(a2[1]);
        close(a2[0]);
        // redirect stdin from the pipe
        while(!std::cin.eof()){
            std::string line;
            std::getline(std::cin, line);
           std:: cout << line << std::endl;
        }
        exit(1);
    } 
    else if (child_pid < 0) {
        std::cerr << "Error: could not fork a sub main" << std::endl;
        return 1;  
    }
    kids.push_back(child_pid);

    while(true){
        int status = -1;
        waitpid(kids[0], &status, WNOHANG);
        
        if (WIFEXITED(status)) {
           for (pid_t k : kids) {
                int status;
                kill (k, SIGTERM);
                waitpid(k, &status, 0);
            }
            break;
            exit(1);
        }
        int status3 = -1;
        waitpid(kids[3], &status3, WNOHANG);
        if (WIFEXITED(status3)) {
           for (pid_t k : kids) {
                int status;
                kill (k, SIGTERM);
                waitpid(k, &status, 0);
            }
            break;
            exit(1);
        }       
    }
  return 0;
}