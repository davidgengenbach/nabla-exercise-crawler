# Commented out exercises have drag'n'drop
# I am not that motivated to get them working, so they'll stay disabled for now
EXERCISE_CONFIGS = {
    'dijkstra': {'id': 4},
    'bellman_ford': {'id': 13},
    'floyd_warshall': {'id': 17},
    'prim': {'id': 15},
    'kruskal': {'id': 16},
    #'linear_probing': {'id': 0},
    #'quadratic_probing': {'id': 1},
    #'double_hashing': {'id': 2},
    'heap_insert': {'id': 20},
    'heap_decrease_key': {'id': 10},
    'merge': {'id': 7},
    'bubblesort': {'id': 19},
    #'selectionsort': {'id': 18},
    'bucketsort': {'id': 11},
    'pivot_partitioning': {'id': 12},
    'simple_string_matching': {'id': 5},
    'string_matching_based_on_finite_automaton': {'id': 6},
    'binary_search_tree_traverse': {'id': 9},
    'b_tree_insert': {'id': 21, 'fill_in': None},
    'b_tree_remove': {'id': 8, 'fill_in': None}
}


def get_exercise_config_from_name(name):
    config = EXERCISE_CONFIGS[name]
    if 'fill_in' not in config:
        config['fill_in'] = '1'
    return config
