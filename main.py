'''
Input any finite non-negative integer sequence.
If it is a graph sequence, a corresponding simple graph will be displayed on the interface
'''

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

seq_input = [int(n) for n in input("Input a sequence:").split()]  # Input a sequence
seq_input.sort(reverse=True)  # Sort the input sequence in descending order
print("The sequence is in descending order:", seq_input)

# If the sum of the sequence is odd, it is not a sequence of degrees of the graph
sum_seq_input = np.sum(seq_input)
if sum_seq_input % 2 == 1:
    print("This sequence is not a graph sequence!")
else:
    seq_input = np.array(seq_input)  # Converts the input to an np array
    seq_len = seq_input.size  # Fetch sequence length
    n = seq_len
    matrix_adj = np.zeros((n, n))  # Generate an adjacency matrix of nxn
    matrix_iter = np.array([seq_input])  # Initialize the sequence matrix to store the sequence results after each loop

    ite_num = 0
    # Loop to solve the sequence of subgraphs after deleting the first point and corresponding edge
    while ((seq_input < 0).any() == False) & ((seq_input == 0).all() == False):

        # When the degree of the maximum point is greater than n-1, there is no simple graph
        if (seq_input[0]+1) > n:
            print("This sequence is not a graph sequence!")
            break

        # Cycle count
        ite_num = ite_num + 1
        print("Number of cycles:", ite_num)

        # Execute simple graph sequence decision algorithm
        for i in range(0, seq_input[0]+1):
            seq_input[i] = seq_input[i]-1
        seq_input = np.delete(seq_input, 0)  # Delete the first point of the remaining sequence
        n = n-1
        # Since the np.sort function can only be sorted in ascending order
        # its inverse number is sorted in ascending order and then the inverse number is taken
        seq_input = np.sort(-seq_input)
        seq_input = (-seq_input)
        print(seq_input)

        # Update sequence matrix
        d_inst = np.pad(seq_input, (ite_num, 0), 'constant', constant_values=(0, 0))
        matrix_iter = np.insert(matrix_iter, ite_num, values=d_inst, axis=0)

    # The loop ends, and we decide whether it's all zeros or negative numbers
    if (seq_input < 0).any():
        print("This sequence is not a graph sequence!")
    elif (seq_input == 0).all():

        # When a graph sequence is available, the adjacency matrix is updated using the iterative matrix
        for i in range(ite_num-1, -1, -1):  # Row traversal
            for k in range(i+1, seq_len, 1):  # Column traversal
                matrix_adj[i, k] = matrix_iter[i, k] - matrix_iter[i+1, k]
                matrix_adj[k, i] = matrix_iter[i, k] - matrix_iter[i+1, k]
        print("The adjacency matrix of the graph corresponding to this sequence:")
        print(matrix_adj)

        # Plot using networkx
        G = nx.Graph()
        Matrix = matrix_adj

        # When the value between the corresponding points in the adjacency matrix is 1
        # An edge is added between the two points
        for i in range(len(Matrix)):
            for j in range(len(Matrix)):
                if Matrix[i, j] == 1:
                  G.add_edge(i, j)

        nx.draw(G, with_labels=True)
        plt.show()
