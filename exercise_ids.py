# Commented out exercises have drag'n'drop
# I am not that motivated to get them working, so they'll stay disabled for now
EXERCISE_IDs = {
    'dijkstra': 4,
    'bellman_ford': 13,
    'floyd_warshall': 17,
    'prim': 15,
    'kruskal': 16,
    #'linear_probing': 0,
    #'quadratic_probing': 1,
    #'double_hashing': 2,
    'heap_insert': 20,
    'heap_decrease_key': 10,
    'merge': 7,
    'bubblesort': 19,
    #'selectionsort': 18,
    'bucketsort': 11,
    'pivot_partitioning': 12,
    'simple_string_matching': 5,
    'string_matching_based_on_finite_automaton': 6,
    'binary_search_tree_traverse': 9,
    'b_tree_insert': 21,
    'b_tree_remove': 8
}

def get_exercise_id_from_name(name):
    return EXERCISE_IDs[name]
