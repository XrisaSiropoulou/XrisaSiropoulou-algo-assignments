import math


def BurstsViterbi(X, k, lambdas):
    n = len(X)
    C = [[float('inf')] * (k) for _ in range(n + 1)]
    P = [[0] * (n + 1) for _ in range(k)]

    # Initial condition
    C[0][0] = 0

    for t in range(1, n + 1):
        for s in range(k):
            l_min = 0
            c_min = C[t - 1][0] + ti(0, s, n)
            for l in range(1, k):
                c = C[t - 1][l] + ti(l, s, n)
                if c < c_min:
                    c_min = c
                    l_min = l
            C[t][s] = c_min - math.log(lambdas[s] * math.exp(-(lambdas[s] * X[t - 1])))
            P[s][0:t] = P[l_min][0:t]
            P[s][t] = s

        # Print the cost matrix and path matrix at each time step
        print(f"Time step {t}:")
        print("C matrix:")
        for row in C:
            print(row)
        print("P matrix:")
        for row in P:
            print(row)
        print("\n")

    l_min = 0
    c_min = C[n][0]
    for s in range(1, k):
        if C[n][s] < c_min:
            c_min = C[n][s]
            l_min = s

    return P[l_min][:n + 1]


def ti(i, j, n):
    if j > i:
        return (1 * (j - i) * math.log(n))  # gamma
    else:
        return 0


def identify_intervals(S, X):
    intervals = []
    start = 0
    current_state = S[0]

    for t in range(1, len(S)):
        if S[t] != current_state:
            intervals.append((current_state, X[start], X[t]))
            current_state = S[t]
            start = t

    intervals.append((current_state, X[start], X[-1]))
    return intervals


# Example usage
X = [0, 10, 20, 30, 31, 32, 33, 34, 35, 40]  # Observation sequence
k = math.ceil(1 + math.log(X[-1], 2) + math.log((1 / 1), 2))  # Number of states
lambdas = [(2 ** i) / (X[-1] / len(X)) for i in range(k)]  # Exponential distribution parameters
print(lambdas)
S = BurstsViterbi(X, k, lambdas)
print(S)
intervals = identify_intervals(S, X)

for state, start, end in intervals:
    print(f"{state}[{start},{end})")

# Parameters
T = 40  # total time
n = 10  # number of intervals
s = 2  # scaling parameter
gamma = 1  # transition cost parameter
X = [0, 10, 20, 30, 31, 32, 33, 34, 35, 40]  # Observation sequence

# Compute g
g = T / n

# Compute lambda for each state
lambda_values = [(2 ** i) / (X[-1] / len(X)) for i in range(n)]


# Transition cost function
def transition_cost(i, j, gamma, ln_n):
    if j > i:
        return gamma * (j - i) * ln_n
    else:
        return 0


# Compute transition costs
tau = [[0] * n for _ in range(n)]
ln_n = math.log(n)
for i in range(n):
    for j in range(n):
        tau[i, j] = transition_cost(i, j, gamma, ln_n)

# Example observations
observations = X


# Bellman-Ford Algorithm for Trellis Graph with detailed output
def bellman_ford(n, tau, observations, lambda_values):
    # Initialize distances to inf and set distance to the initial state (0,0) to 0
    inf = float('inf')
    dist = [[inf] * (n + 1) for _ in range(n)]
    dist[0, 0] = 0
    predecessor = [[-1] * (n + 1) for _ in range(n)]
    # Relax edges up to n times
    for t in range(1, n + 1):
        for j in range(n):
            min_cost = inf
            for ell in range(n):
                current_cost = dist[ell, t - 1] + tau[ell, j]
                if current_cost < min_cost:
                    min_cost = current_cost
                    predecessor[j, t] = ell
            f_j = lambda_values[j] * math.exp(-lambda_values[j] * observations[t - 1])
            log_f_j = -math.log(f_j)
            dist[j, t] = log_f_j + min_cost
            # Detailed output for each relaxation
            print(
                f"({t}, {j}) {dist[ell, t - 1]:.2f} -> {dist[j, t]:.2f} from ({t - 1}, {predecessor[j, t]}) {dist[ell, t - 1]:.2f} + {tau[ell, j]:.2f} + {log_f_j:.2f}")

    return dist, predecessor


# Run Bellman-Ford algorithm
dist, predecessor = bellman_ford(n, tau, observations, lambda_values)

# Print the final distance matrix
print("Distance Matrix (dist):")
print(dist)
print("Predecessor Matrix:")
print(predecessor)


# Reconstruct the path from the predecessor matrix
def reconstruct_path(predecessor, n):
    # Start from the last column and find the minimum cost path
    path = []
    min_index = min(range(n), key=lambda i: dist[i][n])
    t = n
    while t > 0:
        path.append(min_index)
        min_index = predecessor[min_index, t]
        t -= 1
    path.append(0)  # Add the start state
    path.reverse()
    return path


path = reconstruct_path(predecessor, n)
print("Optimal Path:")
print(path)


