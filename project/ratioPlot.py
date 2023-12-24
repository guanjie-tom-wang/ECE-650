import re
import matplotlib.pyplot as plt
import numpy as np

# Assuming 'data' variable holds the content from the text provided earlier.
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
"""
# Regular expressions to find the relevant data
vertex_pattern = re.compile(r'V (\d+)')
cnf_sat_vc_pattern = re.compile(r'CNF-SAT-VC: ([\d,]+)')
approx_vc_1_pattern = re.compile(r'APPROX-VC-1: ([\d,]+)')
approx_vc_2_pattern = re.compile(r'APPROX-VC-2: ([\d,]+)')

# Extracting the data
vertices = vertex_pattern.findall(data)
cnf_sat_vc_solutions = cnf_sat_vc_pattern.findall(data)
approx_vc_1_solutions = approx_vc_1_pattern.findall(data)
approx_vc_2_solutions = approx_vc_2_pattern.findall(data)

# Convert the solutions to sizes
cnf_sat_vc_sizes = [len(solution.split(',')) for solution in cnf_sat_vc_solutions]
approx_vc_1_sizes = [len(solution.split(',')) for solution in approx_vc_1_solutions]
approx_vc_2_sizes = [len(solution.split(',')) for solution in approx_vc_2_solutions]

# Group by vertex size and calculate approximation ratio
ratios_by_vertex = {int(v): {'cnf': [], 'vc1': [], 'vc2': []} for v in set(vertices)}
for v, cnf_size, vc1_size, vc2_size in zip(vertices, cnf_sat_vc_sizes, approx_vc_1_sizes, approx_vc_2_sizes):
    v = int(v)
    # CNF-SAT-VC is the optimal solution, its ratio is always 1
    ratios_by_vertex[v]['cnf'].append(1)
    ratios_by_vertex[v]['vc1'].append(vc1_size / cnf_size)
    ratios_by_vertex[v]['vc2'].append(vc2_size / cnf_size)

# Calculate mean and standard deviation of ratios for each vertex size
mean_ratios = {v: {} for v in ratios_by_vertex}
std_ratios = {v: {} for v in ratios_by_vertex}
for v in ratios_by_vertex:
    mean_ratios[v]['cnf'] = np.mean(ratios_by_vertex[v]['cnf'])  # This will be 1
    mean_ratios[v]['vc1'] = np.mean(ratios_by_vertex[v]['vc1'])
    mean_ratios[v]['vc2'] = np.mean(ratios_by_vertex[v]['vc2'])
    std_ratios[v]['cnf'] = np.std(ratios_by_vertex[v]['cnf'])  # This will be 0
    std_ratios[v]['vc1'] = np.std(ratios_by_vertex[v]['vc1'])
    std_ratios[v]['vc2'] = np.std(ratios_by_vertex[v]['vc2'])

sorted_vertices = sorted(mean_ratios.keys())

# Extract the sorted mean ratios and standard deviations for plotting
sorted_means_cnf = [mean_ratios[v]['cnf'] for v in sorted_vertices]
sorted_means_vc1 = [mean_ratios[v]['vc1'] for v in sorted_vertices]
sorted_means_vc2 = [mean_ratios[v]['vc2'] for v in sorted_vertices]

sorted_std_dev_vc1 = [std_ratios[v]['vc1'] for v in sorted_vertices]
sorted_std_dev_vc2 = [std_ratios[v]['vc2'] for v in sorted_vertices]

# Plotting
plt.figure(figsize=(14, 7))

# Plot continuous lines for the mean ratios
plt.plot(sorted_vertices, sorted_means_cnf, 'o-', color='orange', label='CNF')
plt.plot(sorted_vertices, sorted_means_vc1, 'o-', color='blue', label='VC1')
plt.plot(sorted_vertices, sorted_means_vc2, 'o-', color='green', label='VC2')

# Add error bars
plt.errorbar(sorted_vertices, sorted_means_vc1, yerr=sorted_std_dev_vc1, fmt='o', color='blue', capsize=5)
plt.errorbar(sorted_vertices, sorted_means_vc2, yerr=sorted_std_dev_vc2, fmt='o', color='green', capsize=5)

plt.xlabel('Number of Vertices (|V|)')
plt.ylabel('Approximation Ratio to Optimal Vertex Cover')
plt.title('Approximation Ratio by |V|')
plt.legend()
plt.grid(True)
plt.show()