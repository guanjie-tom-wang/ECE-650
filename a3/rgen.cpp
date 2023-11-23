#include <iostream>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h> 
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <math.h>
#include <iostream>
#include <chrono>
#include <string>
#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <string>
#include <thread>
#include <cmath>
using namespace std;

// idea from A1:
struct Point {
    int x, y;
    Point(int x, int y) : x(x), y(y) {}
};
//idea from A1
struct LineSegment {
    std::string name;
    std::vector<Point> points;
    LineSegment(const std::string& name) : name(name) {}
};

int getRandom(int min, int max) {
    //idea from https://security.stackexchange.com/questions/184210/how-to-correctly-use-dev-urandom-for-random-generation
   	unsigned int random;
	int fd = -1;

	if ((fd = open("/dev/urandom", O_RDONLY)) == -1) {
		cerr << "cannot open /dev/urandom." << endl;
		exit(1);
	}
	read(fd, &random, sizeof(unsigned int));
	close(fd);
	return  min + (random % (max - min + 1));
}

Point generateRandomPoint(int c) {
    return Point(getRandom(-c, c), getRandom(-c, c));
}

bool pointsOverlap(const Point& p1, const Point& p2) {
    return (p1.x == p2.x && p1.y == p2.y);
}


bool isVaildPoint(vector<Point> points, const Point& p1){
     for (std::vector<Point>::size_type i=0; i < points.size(); i++) {
        if(pointsOverlap(points[i], p1)){
            return false;
        }
    }
    return true;
}

bool TwoLinesOverlap(const Point& p0,const Point& p1,const Point& p2,const Point& p3)
{   
    //idea from https://blog.51cto.com/u_16213423/7304141
    int x1 = p0.x;
    int y1 = p0.y;
    int x2 = p1.x;
    int y2 = p1.y;
    int x3 = p2.x;
    int y3 = p2.y;
    int x4 = p3.x;
    int y4 = p3.y;
    double cross_product_1 = (x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1);
    double cross_product_2 = (x3 - x1) * (y4 - y3) - (x4 - x3) * (y3 - y1);
    double cross_product_3 = (x1 - x3) * (y2 - y1) - (x2 - x1) * (y1 - y3);
    double cross_product_4 = (x1 - x3) * (y4 - y3) - (x4 - x3) * (y1 - y3);

    if (cross_product_1 * cross_product_2 < 0 && cross_product_3 * cross_product_4 < 0) {
        return true;
    } else if (cross_product_1 == 0 && cross_product_2 == 0 && cross_product_3 == 0 && cross_product_4 == 0) {
        // If the four points are collinear, further check for overlap
        double min_x = std::min(std::min(std::min(x1, x2), x3), x4);
        double max_x = std::max(std::max(std::max(x1, x2), x3), x4);
        double min_y = std::min(std::min(std::min(y1, y2), y3), y4);
        double max_y = std::max(std::max(std::max(y1, y2), y3), y4);
        if (min_x <= x1 && x1 <= max_x && min_x <= x2 && x2 <= max_x && min_x <= x3 && x3 <= max_x && min_x <= x4 && x4 <= max_x &&
            min_y <= y1 && y1 <= max_y && min_y <= y2 && y2 <= max_y && min_y <= y3 && y3 <= max_y && min_y <= y4 && y4 <= max_y) {
            return true;
        }
    }
    return false;

}
//idea from A1 generate method
bool isOverLap(vector<Point> points, vector<LineSegment> streetSegments){
    for (std::vector<int>::size_type i = 1; i < points.size(); i ++) {
		for (std::vector<int>::size_type  j = 0; j < streetSegments.size(); j ++) {
			for (std::vector<int>::size_type  k = 1; k < streetSegments[j].points.size(); k ++) {
				if ( TwoLinesOverlap(points[i - 1], points[i],streetSegments[j].points[k - 1], streetSegments[j].points[k])) {
					return true;
				}
			}
		}
	}
	return false;
}
//check if one line two segement overlap
bool isOverLap(vector<Point> points, const Point& p){
    if(points.size() == 0) return false;
    for(std::vector<Point>::size_type i = 1; i <= points.size() - 1; i++){
        if(TwoLinesOverlap(points[i - 1], points[i], points[points.size() - 1], p)){
            return true;;
        }
    }
    return false;
}

int main(int argc, char* argv[]) {
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

    std::vector<LineSegment> streetSegments;
	int count = 0;
    while (true) {
        int streetCount = getRandom(2, s);
        int waitTime = getRandom(5, l);
        streetSegments.clear();
		while(count < streetCount){
            LineSegment line("Street_" + std::to_string(count));
            line.points.clear();
            int lineCount = getRandom(1, n);
            int timesTry = 0;

            for (int j = 0; j <= lineCount; j++) {
                if (timesTry == 25) {
                    cerr << "Error: failed to generate valid input for 25 simultaneous attempts" << endl;
                    exit(1);
                }
                bool validPointGenerated = false;
                while (!validPointGenerated){
                    Point point = generateRandomPoint(c);

                    if (isVaildPoint(line.points, point) && !isOverLap(line.points, point)) {
                        line.points.push_back(point);
                        if (isOverLap(line.points, streetSegments)) {
                            timesTry++;
                            break;
                        } else {
                            timesTry = 0;
                            validPointGenerated = true;
                        }
                    } else {
                        timesTry++;
                        break;
                    }
                }
            }
            if (line.points.size() <= 1 || line.points.size() != static_cast<std::vector<Point>::size_type>(lineCount + 1)) {
                if (timesTry < 25) {
                    timesTry++;
                    continue;
                } else {
                    cerr << "Error: failed to generate valid input for 25 simultaneous attempts" << endl;
                    exit(1);
                }
            }
            if (timesTry == 25) {
                cerr << "Error: failed to generate valid input for 25 simultaneous attempts" << endl;
                exit(1);
            }
            streetSegments.push_back(line);
			count++;
        }
        for (const LineSegment& line : streetSegments) {
            std::cout << "add \"" << line.name << "\"";
            for (const Point& point : line.points) {
                std::cout << " (" << point.x << "," << point.y << ")";

            }
            std::cout << std::endl;

        }
        cout << "gg" << endl;
        std::this_thread::sleep_for(std::chrono::seconds(waitTime));

        for (const LineSegment& line : streetSegments) {
            std::cout << "rm \"" << line.name << "\"" << std::endl;
        }
		count = 0;
    }

    return 0;
}

