def BurstsViterbi(X, k, ti, fs):
    n = len(X)
    C = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    P = [[0] * (n + 1) for _ in range(k + 1)]
    
    # Initial condition
    C[0][0] = 0

    for t in range(1, n + 1):
        for s in range(k + 1):
            l_min = 0
            c_min = C[t - 1][0] + ti(0, s)
            for ℓ in range(1, k + 1):
                c = C[t - 1][l] + ti(l, s)
                if c < c_min:
                    c_min = c
                    l_min = l
            C[t][s] = c_min - fs(X[t - 1])
            P[s][0:t] = P[t_min][0:t]
            P[s][t] = s

    l_min = 0
    c_min = C[n][0]
    for s in range(1, k + 1):
        if C[n][s] < c_min:
            c_min = C[n][s]
            l_min = s

    return P[l_min][:n + 1]

#def ti(i, j):


#def fs(X_t):


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

#def transition_cost(from_state, to_state, time):

