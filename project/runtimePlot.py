import matplotlib.pyplot as plt
import numpy as np
import re

# Your data seems to be in a regular format, we will process it line by line
# Let's assume 'data' is a string containing the content of the file

data = """
V 5
CNF-SAT-VC: 1,2
Thread CNF-SAT-VC Time: 0.4853 ms
APPROX-VC-1: 1,2
Thread APPROX-VC-1 Time: 0.0202 ms
APPROX-VC-2: 1,2
Thread APPROX-VC-2 Time: 0.0404 ms
V 5
CNF-SAT-VC: 1,2
Thread CNF-SAT-VC Time: 0.3886 ms
APPROX-VC-1: 1,2
Thread APPROX-VC-1 Time: 0.0216 ms
APPROX-VC-2: 1,4,2,3
Thread APPROX-VC-2 Time: 0.0237 ms
V 5
CNF-SAT-VC: 1,2
Thread CNF-SAT-VC Time: 0.4199 ms
APPROX-VC-1: 1,2
Thread APPROX-VC-1 Time: 0.0362 ms
APPROX-VC-2: 1,4,2,3
Thread APPROX-VC-2 Time: 0.0238 ms
V 5
CNF-SAT-VC: 1,2
Thread CNF-SAT-VC Time: 0.4302 ms
APPROX-VC-1: 1,2
Thread APPROX-VC-1 Time: 0.0216 ms
APPROX-VC-2: 1,5,2,4
Thread APPROX-VC-2 Time: 0.0237 ms
V 5
CNF-SAT-VC: 1,2
Thread CNF-SAT-VC Time: 0.5387 ms
APPROX-VC-1: 1,2
Thread APPROX-VC-1 Time: 0.0291 ms
APPROX-VC-2: 1,4,2,5
Thread APPROX-VC-2 Time: 0.0229 ms
V 5
CNF-SAT-VC: 1,2,3
Thread CNF-SAT-VC Time: 0.4246 ms
APPROX-VC-1: 2,1,3
Thread APPROX-VC-1 Time: 0.0229 ms
APPROX-VC-2: 1,5,2,3
Thread APPROX-VC-2 Time: 0.0183 ms
V 5
CNF-SAT-VC: 1,2
Thread CNF-SAT-VC Time: 0.3671 ms
APPROX-VC-1: 1,2
Thread APPROX-VC-1 Time: 0.0207 ms
APPROX-VC-2: 1,4,2,5
Thread APPROX-VC-2 Time: 0.0228 ms
V 5
CNF-SAT-VC: 1,2,4
Thread CNF-SAT-VC Time: 0.3671 ms
APPROX-VC-1: 1,2,4
Thread APPROX-VC-1 Time: 0.0207 ms
APPROX-VC-2: 1,5,2,3
Thread APPROX-VC-2 Time: 0.02 ms
V 5
CNF-SAT-VC: 1,2,3
Thread CNF-SAT-VC Time: 0.379 ms
APPROX-VC-1: 2,1,3
Thread APPROX-VC-1 Time: 0.0244 ms
APPROX-VC-2: 1,4,2,5
Thread APPROX-VC-2 Time: 0.0207 ms
V 5
CNF-SAT-VC: 1,2,3
Thread CNF-SAT-VC Time: 0.405 ms
APPROX-VC-1: 1,2,3
Thread APPROX-VC-1 Time: 0.0202 ms
APPROX-VC-2: 1,4,2,3
Thread APPROX-VC-2 Time: 0.0201 ms
V 5
CNF-SAT-VC: 1,2,3
Thread CNF-SAT-VC Time: 0.3878 ms
APPROX-VC-1: 1,2,3
Thread APPROX-VC-1 Time: 0.0206 ms
APPROX-VC-2: 1,4,2,5
Thread APPROX-VC-2 Time: 0.0224 ms
V 10
CNF-SAT-VC: 2,4,6,9,10
Thread CNF-SAT-VC Time: 25.1717 ms
APPROX-VC-1: 1,2,4,3,5,7
Thread APPROX-VC-1 Time: 0.0566 ms
APPROX-VC-2: 1,6,2,5,3,10,4,9
Thread APPROX-VC-2 Time: 0.0632 ms
V 10
CNF-SAT-VC: 1,2,4,5,9
Thread CNF-SAT-VC Time: 21.263 ms
APPROX-VC-1: 2,1,5,9,4
Thread APPROX-VC-1 Time: 0.0398 ms
APPROX-VC-2: 1,4,2,7,3,9,5,6
Thread APPROX-VC-2 Time: 0.0413 ms
V 10
CNF-SAT-VC: 1,2,3,8,10
Thread CNF-SAT-VC Time: 24.2908 ms
APPROX-VC-1: 2,1,3,10,5
Thread APPROX-VC-1 Time: 0.0704 ms
APPROX-VC-2: 1,6,2,7,3,5,4,10
Thread APPROX-VC-2 Time: 0.0659 ms
V 10
CNF-SAT-VC: 1,2,3,5
Thread CNF-SAT-VC Time: 12.4261 ms
APPROX-VC-1: 2,1,5,3
Thread APPROX-VC-1 Time: 0.0399 ms
APPROX-VC-2: 1,4,2,5,3,7
Thread APPROX-VC-2 Time: 0.0372 ms
V 10
CNF-SAT-VC: 1,7,8,9,10
Thread CNF-SAT-VC Time: 16.5902 ms
APPROX-VC-1: 1,8,4,5,9
Thread APPROX-VC-1 Time: 0.0416 ms
APPROX-VC-2: 1,3,2,9,4,7,5,8
Thread APPROX-VC-2 Time: 0.0578 ms
V 10
CNF-SAT-VC: 1,2,3,4,5
Thread CNF-SAT-VC Time: 13.5786 ms
APPROX-VC-1: 2,1,4,5,3
Thread APPROX-VC-1 Time: 0.0311 ms
APPROX-VC-2: 1,2,3,6,4,10,5,8
Thread APPROX-VC-2 Time: 0.0239 ms
V 10
CNF-SAT-VC: 3,6,7,8,10
Thread CNF-SAT-VC Time: 15.5875 ms
APPROX-VC-1: 3,1,5,2,7,4
Thread APPROX-VC-1 Time: 0.0411 ms
APPROX-VC-2: 1,6,2,3,4,8,5,10,7,9
Thread APPROX-VC-2 Time: 0.0241 ms
V 10
CNF-SAT-VC: 1,2,3,4,5
Thread CNF-SAT-VC Time: 9.3634 ms
APPROX-VC-1: 1,2,3,4,5
Thread APPROX-VC-1 Time: 0.0776 ms
APPROX-VC-2: 1,2,3,5,4,7
Thread APPROX-VC-2 Time: 0.0301 ms
V 10
CNF-SAT-VC: 1,2,3,5
Thread CNF-SAT-VC Time: 11.8361 ms
APPROX-VC-1: 2,1,5,3
Thread APPROX-VC-1 Time: 0.028 ms
APPROX-VC-2: 1,6,2,10,3,4,5,9
Thread APPROX-VC-2 Time: 0.0349 ms
V 10
CNF-SAT-VC: 1,2,5,6,9
Thread CNF-SAT-VC Time: 17.6683 ms
APPROX-VC-1: 2,1,3,4,5,7
Thread APPROX-VC-1 Time: 0.0382 ms
APPROX-VC-2: 1,9,2,6,5,8
Thread APPROX-VC-2 Time: 0.0507 ms
V 15
CNF-SAT-VC: 1,2,3,5,6,7,8,9
Thread CNF-SAT-VC Time: 4898.39 ms
APPROX-VC-1: 2,5,6,1,4,3,7,8,9
Thread APPROX-VC-1 Time: 0.0612 ms
APPROX-VC-2: 1,15,2,10,3,13,4,5,6,11,7,12,9,14
Thread APPROX-VC-2 Time: 0.0546 ms
V 15
CNF-SAT-VC: 1,2,3,4,5,6,7
Thread CNF-SAT-VC Time: 412.767 ms
APPROX-VC-1: 1,3,4,6,2,5,7
Thread APPROX-VC-1 Time: 0.0471 ms
APPROX-VC-2: 1,9,2,3,4,7,5,8,6,12
Thread APPROX-VC-2 Time: 0.0355 ms
V 15
CNF-SAT-VC: 1,2,4,7,9,10,12
Thread CNF-SAT-VC Time: 1092.85 ms
APPROX-VC-1: 2,4,1,5,12,6,7,9
Thread APPROX-VC-1 Time: 0.0483 ms
APPROX-VC-2: 1,9,2,12,3,4,5,10,7,15
Thread APPROX-VC-2 Time: 0.0449 ms
V 15
CNF-SAT-VC: 1,2,3,5,6,7,8,10
Thread CNF-SAT-VC Time: 4551.02 ms
APPROX-VC-1: 1,7,8,2,5,3,6,10
Thread APPROX-VC-1 Time: 0.0426 ms
APPROX-VC-2: 1,7,2,6,3,13,4,8,5,11,10,14
Thread APPROX-VC-2 Time: 0.0434 ms
V 15
CNF-SAT-VC: 1,5,6,7,8,11,15
Thread CNF-SAT-VC Time: 7846.62 ms
APPROX-VC-1: 1,6,15,8,5,3,11
Thread APPROX-VC-1 Time: 0.0319 ms
APPROX-VC-2: 1,12,2,5,3,7,4,15,6,9,8,13
Thread APPROX-VC-2 Time: 0.0496 ms
V 15
CNF-SAT-VC: 1,5,7,8,9,11,14
Thread CNF-SAT-VC Time: 1266.73 ms
APPROX-VC-1: 9,7,1,8,5,14,11
Thread APPROX-VC-1 Time: 0.0544 ms
APPROX-VC-2: 1,12,2,8,3,5,4,14,7,13,9,15
Thread APPROX-VC-2 Time: 0.0524 ms
V 15
CNF-SAT-VC: 2,5,7,8,9,10,12
Thread CNF-SAT-VC Time: 491.851 ms
APPROX-VC-1: 2,1,4,8,5,7,3,9
Thread APPROX-VC-1 Time: 0.0433 ms
APPROX-VC-2: 1,7,2,9,3,10,4,12,5,11,6,8
Thread APPROX-VC-2 Time: 0.1161 ms
V 15
CNF-SAT-VC: 1,2,3,4,5,6,8,11
Thread CNF-SAT-VC Time: 5978.89 ms
APPROX-VC-1: 2,1,3,4,6,8,11,5
Thread APPROX-VC-1 Time: 0.061 ms
APPROX-VC-2: 1,8,2,7,3,5,4,12,6,10,11,14
Thread APPROX-VC-2 Time: 0.0417 ms
V 15
CNF-SAT-VC: 1,2,3,4,7,8,14
Thread CNF-SAT-VC Time: 505.275 ms
APPROX-VC-1: 4,8,7,14,2,1,3
Thread APPROX-VC-1 Time: 0.0466 ms
APPROX-VC-2: 1,7,2,10,3,8,4,6,9,14
Thread APPROX-VC-2 Time: 0.0463 ms
V 15
CNF-SAT-VC: 2,5,6,7,8,13,14
Thread CNF-SAT-VC Time: 1301.25 ms
APPROX-VC-1: 2,6,7,5,13,8,3
Thread APPROX-VC-1 Time: 0.0484 ms
APPROX-VC-2: 1,13,2,4,3,5,6,15,7,10
Thread APPROX-VC-2 Time: 0.0295 ms
V 20
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0278 ms
APPROX-VC-1: 2,1,10,3,4,12,5,7,8,9
Thread APPROX-VC-1 Time: 0.0602 ms
APPROX-VC-2: 1,15,2,7,3,17,4,16,5,14,6,10,9,19,12,13
Thread APPROX-VC-2 Time: 0.0623 ms
V 20
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.022 ms
APPROX-VC-1: 1,6,13,4,10,15,5,8,3
Thread APPROX-VC-1 Time: 0.0383 ms
APPROX-VC-2: 1,3,2,6,4,16,5,19,7,13,8,17,10,12,11,15
Thread APPROX-VC-2 Time: 0.0803 ms
V 20
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0815 ms
APPROX-VC-1: 1,2,6,3,9,13,4,11,18,12
Thread APPROX-VC-1 Time: 0.0491 ms
APPROX-VC-2: 1,2,3,17,4,7,5,13,6,8,9,10,11,12
Thread APPROX-VC-2 Time: 0.0512 ms
V 20
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0406 ms
APPROX-VC-1: 2,15,7,11,18,9,10,1,5,6,12
Thread APPROX-VC-1 Time: 0.0516 ms
APPROX-VC-2: 1,7,2,10,3,18,4,15,5,11,6,20,8,9,12,14
Thread APPROX-VC-2 Time: 0.0659 ms
V 20
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0164 ms
APPROX-VC-1: 2,10,6,12,1,3,4,5,7,9,11
Thread APPROX-VC-1 Time: 0.0879 ms
APPROX-VC-2: 1,20,2,3,4,14,5,10,6,9,7,18,11,16,12,19
Thread APPROX-VC-2 Time: 0.0612 ms
V 20
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0139 ms
APPROX-VC-1: 7,3,6,2,5,20,15,1,11,12,14
Thread APPROX-VC-1 Time: 0.0461 ms
APPROX-VC-2: 1,20,2,7,3,8,5,9,6,19,12,13,14,16
Thread APPROX-VC-2 Time: 0.0593 ms
V 20
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0157 ms
APPROX-VC-1: 3,1,6,15,14,2,7,8,5
Thread APPROX-VC-1 Time: 0.0457 ms
APPROX-VC-2: 1,20,2,12,3,10,4,8,5,19,6,18,7,9,11,15,14,16
Thread APPROX-VC-2 Time: 0.0695 ms
V 20
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.018 ms
APPROX-VC-1: 2,4,3,1,8,9,17,5,12
Thread APPROX-VC-1 Time: 0.0553 ms
APPROX-VC-2: 1,19,2,9,3,17,4,14,5,10,6,8,12,15
Thread APPROX-VC-2 Time: 0.0595 ms
V 20
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0633 ms
APPROX-VC-1: 6,7,1,3,5,8,10,11,2,4,9
Thread APPROX-VC-1 Time: 0.0903 ms
APPROX-VC-2: 1,9,2,5,3,16,4,18,6,14,7,17,8,15,10,12,11,13
Thread APPROX-VC-2 Time: 0.0587 ms
V 20
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0136 ms
APPROX-VC-1: 2,3,10,8,1,7,11,5,6,12
Thread APPROX-VC-1 Time: 0.0708 ms
APPROX-VC-2: 1,20,2,5,3,14,4,10,6,8,7,15,11,18,12,13
Thread APPROX-VC-2 Time: 0.0547 ms
V 25
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0182 ms
APPROX-VC-1: 17,2,16,6,4,14,15,1,8,11,21
Thread APPROX-VC-1 Time: 0.0933 ms
APPROX-VC-2: 1,7,2,12,3,14,4,20,6,25,8,16,10,11,13,15,17,19,18,21
Thread APPROX-VC-2 Time: 0.0746 ms
V 25
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0139 ms
APPROX-VC-1: 2,3,8,6,1,10,15,18,25,5,12,13,14,19
Thread APPROX-VC-1 Time: 0.0537 ms
APPROX-VC-2: 1,11,2,4,3,17,5,15,6,21,7,25,8,10,9,18,12,24,14,20,19,22
Thread APPROX-VC-2 Time: 0.075 ms
V 25
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0154 ms
APPROX-VC-1: 4,18,1,3,9,5,16,6,14,20,7,8,13
Thread APPROX-VC-1 Time: 0.0543 ms
APPROX-VC-2: 1,23,2,3,4,5,6,15,7,10,8,9,11,18,13,24,14,22
Thread APPROX-VC-2 Time: 0.1192 ms
V 25
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0145 ms
APPROX-VC-1: 4,7,2,3,6,14,15,8,10,13,1,9,11,16
Thread APPROX-VC-1 Time: 0.0588 ms
APPROX-VC-2: 1,20,2,25,3,19,4,17,5,13,6,9,7,22,8,12,10,16,11,18,14,23,15,24
Thread APPROX-VC-2 Time: 0.1302 ms
V 25
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.023 ms
APPROX-VC-1: 11,2,1,7,5,12,4,8,13,15,20,10,17
Thread APPROX-VC-1 Time: 0.0925 ms
APPROX-VC-2: 1,23,2,4,3,15,5,25,6,11,7,19,8,18,9,20,10,22,12,21
Thread APPROX-VC-2 Time: 0.1191 ms
V 25
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0273 ms
APPROX-VC-1: 9,2,19,1,10,21,8,11,3,4,5,6,14,15,16
Thread APPROX-VC-1 Time: 0.1116 ms
APPROX-VC-2: 1,9,2,16,3,21,4,19,5,23,6,13,8,24,10,11,14,17,15,22
Thread APPROX-VC-2 Time: 0.2032 ms
V 25
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.1757 ms
APPROX-VC-1: 1,2,16,5,17,24,25,11,15,3,4,9,10,18
Thread APPROX-VC-1 Time: 0.1042 ms
APPROX-VC-2: 1,15,2,3,4,16,5,18,8,11,9,22,10,25,12,17,13,24
Thread APPROX-VC-2 Time: 0.1196 ms
V 25
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0216 ms
APPROX-VC-1: 2,5,10,1,9,18,7,8,14,19,3,4,6,15
Thread APPROX-VC-1 Time: 0.0867 ms
APPROX-VC-2: 1,17,2,24,3,21,4,5,6,16,7,25,8,11,9,15,10,14,13,19
Thread APPROX-VC-2 Time: 0.1069 ms
V 25
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0205 ms
APPROX-VC-1: 11,17,16,1,6,8,10,23,7,15,4,5,13,14
Thread APPROX-VC-1 Time: 0.0842 ms
APPROX-VC-2: 1,21,2,15,3,11,4,8,5,19,6,17,7,22,10,12,13,24,16,18
Thread APPROX-VC-2 Time: 0.1831 ms
V 25
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0242 ms
APPROX-VC-1: 1,10,7,20,14,16,2,5,17,4,6,12
Thread APPROX-VC-1 Time: 0.0771 ms
APPROX-VC-2: 1,7,2,20,3,5,4,10,6,9,12,14,15,17,16,18
Thread APPROX-VC-2 Time: 0.187 ms
V 30
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0442 ms
APPROX-VC-1: 8,1,4,25,21,10,7,12,13,20,23,3,9,11,19
Thread APPROX-VC-1 Time: 0.139 ms
APPROX-VC-2: 1,10,2,23,3,21,4,30,5,13,6,25,7,29,8,24,9,18,11,17,12,26,19,22
Thread APPROX-VC-2 Time: 0.0923 ms
V 30
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0148 ms
APPROX-VC-1: 2,1,22,6,15,3,11,7,12,13,20,26,4,9,19,23
Thread APPROX-VC-1 Time: 0.0718 ms
APPROX-VC-2: 1,6,2,18,3,21,4,22,5,13,7,16,8,15,9,10,11,24,12,25,17,26,19,29,20,23
Thread APPROX-VC-2 Time: 0.1056 ms
V 30
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.057 ms
APPROX-VC-1: 23,2,6,10,8,11,13,17,21,18,19,4,9
Thread APPROX-VC-1 Time: 0.0641 ms
APPROX-VC-2: 1,21,2,14,3,19,4,6,5,8,7,17,9,10,11,26,12,23,13,16,18,30
Thread APPROX-VC-2 Time: 0.1133 ms
V 30
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0168 ms
APPROX-VC-1: 2,14,19,13,25,3,17,1,5,7,12,26,4,9,10,20
Thread APPROX-VC-1 Time: 0.0705 ms
APPROX-VC-2: 1,14,2,13,3,10,4,19,5,29,6,26,7,25,9,11,12,15,17,24,20,23
Thread APPROX-VC-2 Time: 0.0946 ms
V 30
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0134 ms
APPROX-VC-1: 13,2,30,17,3,5,6,19,1,9,4,8,14,18,20,22
Thread APPROX-VC-1 Time: 0.0822 ms
APPROX-VC-2: 1,10,2,5,3,8,4,6,7,19,9,18,11,13,14,23,15,30,17,21,20,28,22,24
Thread APPROX-VC-2 Time: 0.0881 ms
V 30
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0133 ms
APPROX-VC-1: 29,7,1,28,3,2,6,5,15,17,21,26,4,13
Thread APPROX-VC-1 Time: 0.0616 ms
APPROX-VC-2: 1,21,2,20,3,15,4,19,5,27,6,13,7,12,8,26,10,17,11,28,24,29
Thread APPROX-VC-2 Time: 0.0849 ms
V 30
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0141 ms
APPROX-VC-1: 19,12,8,9,11,16,1,3,18,25,26,5,10,13,20
Thread APPROX-VC-1 Time: 0.0689 ms
APPROX-VC-2: 1,30,2,16,3,10,4,18,5,15,7,8,9,25,11,24,12,14,19,26,20,21
Thread APPROX-VC-2 Time: 0.0994 ms
V 30
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0149 ms
APPROX-VC-1: 1,8,4,13,25,28,11,14,21,3,9,22,5,7,20,24
Thread APPROX-VC-1 Time: 0.07 ms
APPROX-VC-2: 1,13,2,4,3,17,5,14,6,8,7,11,9,15,10,25,18,28,20,27,21,23,22,24
Thread APPROX-VC-2 Time: 0.0905 ms
V 30
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0145 ms
APPROX-VC-1: 6,12,13,9,1,15,22,2,5,10,14,24,4,8,11,17
Thread APPROX-VC-1 Time: 0.071 ms
APPROX-VC-2: 1,14,2,18,3,13,4,30,5,21,6,17,7,24,8,28,9,15,10,20,11,29,12,22
Thread APPROX-VC-2 Time: 0.1587 ms
V 30
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0135 ms
APPROX-VC-1: 16,18,12,15,30,2,6,8,19,21,5,10,4,7,17
Thread APPROX-VC-1 Time: 0.0683 ms
APPROX-VC-2: 1,21,2,7,3,6,4,20,5,26,8,27,9,19,10,17,11,30,12,22,13,16,18,28
Thread APPROX-VC-2 Time: 0.0978 ms
V 35
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0194 ms
APPROX-VC-1: 1,10,5,30,2,3,12,17,21,24,9,13,26,4,8,11,14,23,25
Thread APPROX-VC-1 Time: 0.1068 ms
APPROX-VC-2: 1,32,2,14,3,7,4,12,5,26,8,19,9,33,10,27,11,21,13,28,16,30,17,29,23,34
Thread APPROX-VC-2 Time: 0.2413 ms
V 35
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0147 ms
APPROX-VC-1: 3,17,2,4,15,11,10,12,18,24,6,27,13,16,21,23
Thread APPROX-VC-1 Time: 0.0873 ms
APPROX-VC-2: 2,31,3,15,4,33,5,6,9,10,11,12,13,25,14,18,16,24,17,21,23,26,27,34
Thread APPROX-VC-2 Time: 0.1014 ms
V 35
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0136 ms
APPROX-VC-1: 1,15,20,6,10,17,26,27,4,5,14,19,21,23,28,2,16
Thread APPROX-VC-1 Time: 0.0904 ms
APPROX-VC-2: 1,18,2,35,3,15,4,32,5,9,6,33,7,14,8,27,10,21,11,20,12,23,17,29,19,30,22,28,26,31
Thread APPROX-VC-2 Time: 0.127 ms
V 35
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0171 ms
APPROX-VC-1: 2,14,1,10,19,22,24,9,17,23,4,5,3,11,12,16,27
Thread APPROX-VC-1 Time: 0.2279 ms
APPROX-VC-2: 1,13,2,19,3,14,4,34,5,12,6,23,7,17,8,22,9,25,10,16,11,18,24,31
Thread APPROX-VC-2 Time: 0.1165 ms
V 35
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.017 ms
APPROX-VC-1: 24,2,17,1,8,4,20,21,28,3,7,9,12,6,10,14,15,23
Thread APPROX-VC-1 Time: 0.1576 ms
APPROX-VC-2: 1,31,2,10,3,17,4,6,5,28,7,22,8,35,9,24,12,33,14,19,20,32,21,27,23,29
Thread APPROX-VC-2 Time: 0.2227 ms
V 35
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0168 ms
APPROX-VC-1: 33,31,15,22,29,8,13,11,1,4,17,30,2,6,7,24,26
Thread APPROX-VC-1 Time: 0.1614 ms
APPROX-VC-2: 1,9,2,15,3,22,4,24,5,31,6,35,7,10,8,16,11,26,13,30,17,34,18,33,20,29
Thread APPROX-VC-2 Time: 0.1258 ms
V 35
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0191 ms
APPROX-VC-1: 2,8,31,9,21,35,3,4,28,5,6,14,15,26,1,17,22,30
Thread APPROX-VC-1 Time: 0.1632 ms
APPROX-VC-2: 1,8,2,33,3,14,4,12,5,19,6,27,7,35,9,13,11,28,15,30,16,31,17,34,18,21,24,26
Thread APPROX-VC-2 Time: 0.2018 ms
V 35
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0176 ms
APPROX-VC-1: 12,5,9,19,2,7,24,27,3,6,8,10,11,14,34,13,15,17
Thread APPROX-VC-1 Time: 0.1717 ms
APPROX-VC-2: 1,6,2,18,3,33,4,34,5,32,7,22,8,16,9,15,10,30,11,25,12,27,13,19,14,31,24,29
Thread APPROX-VC-2 Time: 0.1896 ms
V 35
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0168 ms
APPROX-VC-1: 7,8,2,19,30,28,3,6,33,16,23,26,1,4,5,9,13,18
Thread APPROX-VC-1 Time: 0.1503 ms
APPROX-VC-2: 1,30,2,34,3,15,4,8,5,32,6,16,7,31,9,29,10,19,12,33,13,35,17,28,18,27,22,26
Thread APPROX-VC-2 Time: 0.1177 ms
V 35
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0153 ms
APPROX-VC-1: 1,15,4,11,17,22,24,3,6,20,30,14,18,23,35
Thread APPROX-VC-1 Time: 0.1903 ms
APPROX-VC-2: 1,35,2,11,3,14,4,31,5,18,6,29,9,30,15,34,16,24,17,28,20,21,23,32
Thread APPROX-VC-2 Time: 0.1163 ms
V 40
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0215 ms
APPROX-VC-1: 16,7,9,35,1,2,4,20,32,10,36,15,17,23,24,25,26,22
Thread APPROX-VC-1 Time: 0.1125 ms
APPROX-VC-2: 1,30,2,8,3,16,4,38,5,35,6,26,7,10,9,36,11,24,12,15,17,39,18,25,19,20,23,29,32,34
Thread APPROX-VC-2 Time: 0.1431 ms
V 40
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.014 ms
APPROX-VC-1: 17,3,8,2,6,12,14,21,24,40,7,16,26,33,35,1,4,11,23,25,29
Thread APPROX-VC-1 Time: 0.1063 ms
APPROX-VC-2: 1,27,2,15,3,19,4,6,5,8,7,23,10,17,11,34,12,20,14,33,16,22,18,24,21,25,26,31,29,32
Thread APPROX-VC-2 Time: 0.1338 ms
V 40
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0234 ms
APPROX-VC-1: 22,1,2,3,8,28,12,27,14,20,24,7,9,23,4,6,10,18,32
Thread APPROX-VC-1 Time: 0.1304 ms
APPROX-VC-2: 1,31,2,7,3,5,4,20,6,8,9,15,10,36,11,22,12,29,13,23,14,35,16,27,18,19,21,28,24,33,32,40
Thread APPROX-VC-2 Time: 0.171 ms
V 40
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0163 ms
APPROX-VC-1: 3,1,10,11,5,13,19,16,17,18,35,2,4,21,37,9,12,15,23,24,25,29
Thread APPROX-VC-1 Time: 0.1453 ms
APPROX-VC-2: 1,12,2,9,3,36,4,11,5,33,6,16,7,10,13,20,14,19,17,38,18,34,22,37,24,40,25,35,29,30
Thread APPROX-VC-2 Time: 0.1542 ms
V 40
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0721 ms
APPROX-VC-1: 11,1,5,6,24,30,37,17,20,2,3,15,16,25,33,7,10,18,22,23
Thread APPROX-VC-1 Time: 0.121 ms
APPROX-VC-2: 1,15,2,35,3,31,4,11,5,32,6,17,7,13,8,30,10,34,12,16,14,37,18,38,19,24,20,33,22,27,23,26,25,40
Thread APPROX-VC-2 Time: 0.1812 ms
V 40
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0167 ms
APPROX-VC-1: 1,10,11,25,26,31,2,5,6,13,19,37,20,21,3,4,7,9,12,18,22,23
Thread APPROX-VC-1 Time: 0.1255 ms
APPROX-VC-2: 1,17,2,21,3,5,4,35,6,20,7,37,9,13,10,11,12,19,14,31,15,26,18,27,22,29,23,32,24,25
Thread APPROX-VC-2 Time: 0.1526 ms
V 40
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0146 ms
APPROX-VC-1: 12,5,1,10,14,15,21,23,29,16,20,25,3,4,31,38,2,7,17
Thread APPROX-VC-1 Time: 0.1851 ms
APPROX-VC-2: 1,40,2,36,3,7,4,24,5,32,6,23,8,25,9,12,10,22,13,38,14,26,15,18,16,34,17,37,19,20,21,33,27,31,28,29
Thread APPROX-VC-2 Time: 0.1683 ms
V 40
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0189 ms
APPROX-VC-1: 13,7,18,1,4,14,21,2,29,37,38,5,6,12,17,3,8,9,11,15
Thread APPROX-VC-1 Time: 0.1159 ms
APPROX-VC-2: 1,29,2,40,3,14,4,35,5,32,6,31,7,37,9,13,10,18,11,22,12,39,15,25,17,19,20,21,24,38
Thread APPROX-VC-2 Time: 0.1935 ms
V 40
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0189 ms
APPROX-VC-1: 11,15,1,3,16,26,38,14,21,2,5,19,20,28,30,4,8,12,25,27
Thread APPROX-VC-1 Time: 0.1066 ms
APPROX-VC-2: 1,11,2,10,3,6,4,32,5,38,8,33,12,17,13,28,14,31,15,23,16,37,19,22,20,36,26,27,30,35
Thread APPROX-VC-2 Time: 0.1374 ms
V 40
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0149 ms
APPROX-VC-1: 2,15,34,40,5,21,38,1,4,23,29,16,17,19,27,6,7,20,22,25,26
Thread APPROX-VC-1 Time: 0.107 ms
APPROX-VC-2: 1,40,2,13,3,27,4,8,5,33,6,39,7,31,9,17,10,21,11,34,12,38,14,29,15,24,16,35,18,19,23,25,26,36
Thread APPROX-VC-2 Time: 0.1611 ms
V 45
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0208 ms
APPROX-VC-1: 16,25,1,2,3,27,12,15,24,29,35,38,5,33,41,6,8,9,11,14
Thread APPROX-VC-1 Time: 0.1947 ms
APPROX-VC-2: 1,33,2,6,3,44,4,38,5,21,7,41,8,36,9,40,10,15,11,45,12,20,13,35,14,24,16,26,22,27,23,29,25,31
Thread APPROX-VC-2 Time: 0.1636 ms
V 45
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.015 ms
APPROX-VC-1: 22,11,39,23,2,19,26,38,1,6,35,4,12,15,17,25,34,3,9,24,31
Thread APPROX-VC-1 Time: 0.1461 ms
APPROX-VC-2: 1,25,2,13,3,38,4,16,6,40,7,26,8,22,9,20,11,17,12,45,15,21,19,35,24,39,28,34,31,43
Thread APPROX-VC-2 Time: 0.227 ms
V 45
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0939 ms
APPROX-VC-1: 7,6,45,20,10,11,16,36,1,9,12,23,8,14,28,3,4,5,15,24,34
Thread APPROX-VC-1 Time: 0.1629 ms
APPROX-VC-2: 1,5,2,36,3,42,4,20,6,23,7,41,8,22,9,28,10,21,11,44,12,37,14,35,15,39,16,27,19,45,24,31
Thread APPROX-VC-2 Time: 0.2125 ms
V 45
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0223 ms
APPROX-VC-1: 1,15,12,2,4,7,28,17,19,24,32,35,3,23,25,31,34,36,43,6,11,18,20,21
Thread APPROX-VC-1 Time: 0.1743 ms
APPROX-VC-2: 1,3,2,19,4,40,5,43,6,37,7,29,8,23,9,28,11,26,12,13,14,31,15,39,16,25,17,44,18,35,20,32,21,38
Thread APPROX-VC-2 Time: 0.3422 ms
V 45
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0233 ms
APPROX-VC-1: 1,2,7,9,23,30,5,15,25,6,10,14,12,17,19,28,3,4,16,20,24,27,38
Thread APPROX-VC-1 Time: 0.3052 ms
APPROX-VC-2: 1,43,2,22,3,37,4,31,5,42,6,9,7,11,8,25,10,40,12,26,13,17,14,30,15,18,16,34,19,29,21,23,28,32,38,41
Thread APPROX-VC-2 Time: 0.3727 ms
V 45
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0189 ms
APPROX-VC-1: 2,20,1,11,13,8,15,23,4,7,16,25,5,12,14,24,31,36,3,17,26
Thread APPROX-VC-1 Time: 0.1478 ms
APPROX-VC-2: 1,12,2,8,3,45,4,39,5,38,6,13,7,42,9,16,11,14,15,44,17,43,18,25,20,24,21,23,22,36,27,31
Thread APPROX-VC-2 Time: 0.196 ms
V 45
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0194 ms
APPROX-VC-1: 17,21,1,10,16,20,23,43,32,6,9,12,14,31,35,45,4,11,13,26,28,33
Thread APPROX-VC-1 Time: 0.152 ms
APPROX-VC-2: 1,36,2,31,3,35,4,21,5,17,6,37,9,27,10,13,11,43,12,23,14,44,15,45,16,40,19,32,20,33,26,41,28,34
Thread APPROX-VC-2 Time: 0.3311 ms
V 45
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0204 ms
APPROX-VC-1: 9,24,38,3,44,7,11,32,33,34,2,4,10,15,16,29,41,1,12,18,30
Thread APPROX-VC-1 Time: 0.2313 ms
APPROX-VC-2: 1,38,2,36,3,20,4,42,5,41,6,9,7,10,8,11,12,19,13,15,14,34,16,24,18,33,22,29,26,44,28,32,30,43
Thread APPROX-VC-2 Time: 0.2891 ms
V 45
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0187 ms
APPROX-VC-1: 24,1,19,4,9,41,32,12,20,30,37,2,3,31,34,36,43,6,13,25,26
Thread APPROX-VC-1 Time: 0.2777 ms
APPROX-VC-2: 1,44,2,9,3,19,4,38,5,32,6,35,7,41,8,20,11,24,12,17,13,39,16,34,21,31,22,37,25,40,26,30,29,36,33,43
Thread APPROX-VC-2 Time: 0.2236 ms
V 45
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0968 ms
APPROX-VC-1: 17,19,2,21,26,29,31,33,6,11,24,27,41,1,4,9,35,42,5,13,18,23,38
Thread APPROX-VC-1 Time: 0.2059 ms
APPROX-VC-2: 1,20,2,23,3,27,4,14,5,7,6,30,9,15,10,11,13,24,16,29,17,45,18,40,19,26,21,44,25,35,28,31,32,33,37,42,38,41
Thread APPROX-VC-2 Time: 0.2609 ms
V 50
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0233 ms
APPROX-VC-1: 35,24,4,12,28,29,44,7,32,10,11,15,26,27,6,16,22,42,47,1,3,17,39
Thread APPROX-VC-1 Time: 0.2586 ms
APPROX-VC-2: 1,35,2,29,3,12,4,49,5,7,6,13,9,28,10,33,11,17,15,22,16,18,19,44,20,26,21,32,24,31,27,34,37,47,39,46
Thread APPROX-VC-2 Time: 0.2042 ms
V 50
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0179 ms
APPROX-VC-1: 2,4,5,16,19,22,20,36,37,11,13,25,26,27,40,42,8,43,1,3,10,32,33
Thread APPROX-VC-1 Time: 0.1377 ms
APPROX-VC-2: 1,19,2,15,3,27,4,23,5,14,6,25,7,16,8,22,9,36,10,45,11,30,13,33,18,43,20,28,24,37,26,46,31,42,32,48,40,41
Thread APPROX-VC-2 Time: 0.2511 ms
V 50
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0154 ms
APPROX-VC-1: 15,26,5,18,36,2,3,47,8,22,25,43,1,4,6,10,11,12,27,39,14,17,21,28,30,32,34
Thread APPROX-VC-1 Time: 0.154 ms
APPROX-VC-2: 1,28,2,40,3,27,4,21,5,29,6,42,8,23,9,15,10,41,11,33,12,47,13,36,14,38,17,44,18,37,22,30,24,26,25,35,31,39,43,49
Thread APPROX-VC-2 Time: 0.2047 ms
V 50
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0149 ms
APPROX-VC-1: 1,10,22,6,44,46,50,4,17,36,40,11,3,9,13,21,32,2,15,16,18,20,23,29,30
Thread APPROX-VC-1 Time: 0.1579 ms
APPROX-VC-2: 1,21,2,27,3,14,4,42,5,11,6,7,9,40,10,12,13,36,15,24,16,17,18,26,19,50,20,48,22,30,23,41,28,44,29,33,32,49,39,46
Thread APPROX-VC-2 Time: 0.2036 ms
V 50
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0154 ms
APPROX-VC-1: 43,8,37,48,3,38,41,49,6,19,21,26,33,4,20,46,2,10,15,22,24,25,31
Thread APPROX-VC-1 Time: 0.1362 ms
APPROX-VC-2: 1,43,2,12,3,16,4,49,5,46,6,23,7,48,8,9,10,50,11,33,14,37,15,36,19,32,20,22,21,45,24,41,25,26,31,44,34,38
Thread APPROX-VC-2 Time: 0.2673 ms
V 50
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0233 ms
APPROX-VC-1: 4,2,11,6,12,20,5,21,39,3,7,22,1,13,19,27,35,41,42,9,26,28,32
Thread APPROX-VC-1 Time: 0.1355 ms
APPROX-VC-2: 1,39,2,46,3,37,4,31,5,34,6,38,7,36,8,19,9,17,10,42,11,45,12,21,13,20,22,29,23,35,27,28,32,48
Thread APPROX-VC-2 Time: 0.1891 ms
V 50
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0153 ms
APPROX-VC-1: 47,21,26,1,7,42,17,37,2,5,9,22,31,3,10,16,18,43,6,12,19,27,38,39
Thread APPROX-VC-1 Time: 0.1381 ms
APPROX-VC-2: 1,11,2,18,3,48,5,8,6,40,7,17,9,50,10,26,12,34,13,47,14,37,15,42,16,38,19,41,20,21,22,45,28,31,39,44
Thread APPROX-VC-2 Time: 0.196 ms
V 50
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0145 ms
APPROX-VC-1: 14,15,30,22,33,3,25,26,35,4,5,18,27,29,48,6,7,12,41,1,9,20,21,32
Thread APPROX-VC-1 Time: 0.1408 ms
APPROX-VC-2: 1,30,2,3,4,17,5,10,6,42,7,22,8,27,9,29,11,12,13,48,14,25,15,28,16,33,18,21,20,47,24,26,32,37,34,35,36,41
Thread APPROX-VC-2 Time: 0.2217 ms
V 50
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0152 ms
APPROX-VC-1: 2,3,22,36,10,16,17,18,27,44,38,47,9,12,19,23,25,46,4,5,6,7,15,20,26,28
Thread APPROX-VC-1 Time: 0.1517 ms
APPROX-VC-2: 1,47,2,11,3,18,4,45,5,42,6,10,7,16,8,22,9,44,12,37,13,36,14,38,15,34,17,46,19,29,20,49,25,43,27,39,28,32
Thread APPROX-VC-2 Time: 0.2825 ms
V 50
CNF-SAT-VC: timeout
Thread CNF-SAT-VC Time: 0.0161 ms
APPROX-VC-1: 30,14,8,21,35,3,13,31,32,5,12,16,17,36,40,1,11,15,27,2,6,18,28,37
Thread APPROX-VC-1 Time: 0.1409 ms
APPROX-VC-2: 1,22,2,8,3,46,4,31,5,10,6,25,7,40,9,13,11,43,12,30,14,45,15,42,16,23,17,33,18,26,21,29,24,35,27,50,32,36,37,44
Thread APPROX-VC-2 Time: 0.218 ms
"""

# Regular expressions for extracting data
vertex_pattern = re.compile(r'V (\d+)')
cnf_sat_pattern = re.compile(r'CNF-SAT-VC: (?:timeout|[\d,]+)\s+Thread CNF-SAT-VC Time: ([\d.]+) ms')
approx_vc_1_pattern = re.compile(r'APPROX-VC-1: [\d,]+\s+Thread APPROX-VC-1 Time: ([\d.]+) ms')
approx_vc_2_pattern = re.compile(r'APPROX-VC-2: [\d,]+\s+Thread APPROX-VC-2 Time: ([\d.]+) ms')
# Extracting data
vertices = vertex_pattern.findall(data)
cnf_sat_times = cnf_sat_pattern.findall(data)
approx_vc_1_times = approx_vc_1_pattern.findall(data)
approx_vc_2_times = approx_vc_2_pattern.findall(data)
print("Vertices found:", len(vertices))
# print("CNF-SAT-VC times:", cnf_sat_times)
print("APPROX-VC-1 times:", len(approx_vc_1_times))
print("APPROX-VC-2 times:", len(approx_vc_2_times))


# Convert times to floats and handle 'timeout' as np.nan
cnf_sat_times = [float(time) if time != 'timeout' else np.nan for time in cnf_sat_times]
approx_vc_1_times = [float(time) if time != 'timeout' else np.nan for time in approx_vc_1_times]
approx_vc_2_times = [float(time) if time != 'timeout' else np.nan for time in approx_vc_2_times]

vertices = [int(v) for v in vertices]
print("guanjie ",vertices)
# Grouping times by vertex count
times_by_vertex = {}
# cnf_sat_times
for v, cnf, vc1, vc2 in zip(vertices, cnf_sat_times, approx_vc_1_times, approx_vc_2_times):
    v = int(v)
    print("guanjie 1",v)

    if v not in times_by_vertex:
        times_by_vertex[v] = { 'cnf':[], 'vc1': [], 'vc2': []}
    if(v <= 15):
        times_by_vertex[v]['cnf'].append(cnf)
    print("guanjie 2",v)
    times_by_vertex[v]['vc1'].append(vc1)
    times_by_vertex[v]['vc2'].append(vc2)

# Calculating averages and standard deviations
average_times = {}
std_times = {}
for v, times in times_by_vertex.items():
    average_times[v] = {method: np.nanmean(method_times) for method, method_times in times.items()}
    std_times[v] = {method: np.nanstd(method_times) for method, method_times in times.items()}

# Data for plotting
vertex_counts = sorted(average_times.keys())
print("Vertices to be plotted:", vertex_counts)
avg_vc1 = [average_times[v]['vc1'] for v in vertex_counts]
avg_vc2 = [average_times[v]['vc2'] for v in vertex_counts]
std_vc1 = [std_times[v]['vc1'] for v in vertex_counts]
std_vc2 = [std_times[v]['vc2'] for v in vertex_counts]
avg_cnf = [average_times[v]['cnf'] for v in vertex_counts]
std_cnf = [std_times[v]['cnf'] for v in vertex_counts]
# Plotting with the adjusted standard deviation
plt.figure(figsize=(10, 5))
# plt.errorbar(vertex_counts, avg_vc1, yerr=std_vc1, label='APPROX-VC-1', fmt='-o', capsize=5)
# plt.errorbar(vertex_counts, avg_vc2, yerr=std_vc2, label='APPROX-VC-2', fmt='-^', capsize=5)
plt.errorbar(vertex_counts, avg_cnf, yerr=std_cnf, label='CNF-SAT-VC', fmt='-s', capsize=5)

plt.xlabel('Number of Vertices (V)')
plt.ylabel('Average Time (ms)')
plt.title('Average Running Time by V with Standard Deviation')
plt.legend()
plt.grid(True)

# plt.ylim(0, 10000) 
plt.xlim(0, 20)
plt.yscale('log')

# Adjust the y-axis limits if needed, depending on your data
max_value = max(avg_vc1 + avg_vc2 + avg_cnf)
plt.ylim(bottom=min(avg_vc1 + avg_vc2 + avg_cnf), top=10 ** np.ceil(np.log10(max_value)))

plt.tight_layout()
plt.show()


