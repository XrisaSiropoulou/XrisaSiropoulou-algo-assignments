import math


def BurstsViterbi(X, k, lambdas):
    n = len(X)
    C = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    P = [[0] * (n + 1) for _ in range(k + 1)]

    # Initial condition
    C[0][0] = 0

    for t in range(1, n + 1):
        for s in range(k + 1):
            l_min = 0
            c_min = C[t - 1][0] + ti(0, s, n)
            for l in range(1, k + 1):
                c = C[t - 1][l] + ti(l, s, n)
                if c < c_min:
                    c_min = c
                    l_min = l
            C[t][s] = c_min - math.log(lambdas[s]) - lambdas[s] * X[t - 1]
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
    for s in range(1, k + 1):
        if C[n][s] < c_min:
            c_min = C[n][s]
            l_min = s

    return P[l_min][:n + 1]


def ti(i, j, n):
    if j > i:
        return 1 * (j - i) * math.log(n)  # gamma
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
k = 1  # Number of states
lambdas = [2 ** i for i in range(k + 1)]  # Exponential distribution parameters

S = BurstsViterbi(X, k, lambdas)
intervals = identify_intervals(S, X)

for state, start, end in intervals:
    print(f"{state}[{start},{end})")


def trellis_algorithm(state_space, sequence_length, transition_cost):
    num_states = len(state_space)

    T = sequence_length

    C = [[float('inf')] * (T + 1) for _ in range(num_states)]

    P = [[None] * (T + 1) for _ in range(num_states)]

    C[0][0] = 0

    # Forward pass

    for t in range(1, T + 1):

        for i in range(num_states):

            for j in range(num_states):

                cost = C[j][t - 1] + transition_cost(state_space[j], state_space[i], t)

                if cost < C[i][t]:
                    C[i][t] = cost

                    P[i][t] = j

    # Backtrack to find the best path

    min_cost = float('inf')

    final_state = None

    for i in range(num_states):

        if C[i][T] < min_cost:
            min_cost = C[i][T]

            final_state = i

    best_path = [None] * (T + 1)

    best_path[T] = final_state

    for t in range(T, 0, -1):
        best_path[t - 1] = P[best_path[t]][t]

    best_path_states = [state_space[i] for i in best_path]

    return best_path_states, min_cost

# def transition_cost(from_state, to_state, time):




