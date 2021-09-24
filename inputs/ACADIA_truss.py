data_in = {
    "name": "ACADIA_truss",
    "output_vid": "outputs/ACADIA_truss.gif",
    "backtrack": "peterson",
    "n_max_steps": 1000,
    "n_gradient_steps": 0,
    #
    "vertices": {
        0: (1, 1.0),
        1: (4, 1.0),
        2: (1, 5.0),
        3: (4, 5.0),
        4: (7, 5.0),
        5: (8, 5.0),
        6: (9, 5.0),
    },
    "edges":{
        0: (0,1),
        1: (0,2),
        2: (0,3),
        3: (2,3),
        4: (1,3),
        5: (1,2),
    },
    "edge_lengths": [],
    "rigid_edge": [0],
    #
    "plotting_features1": {
        'n_color':'#afcdfa',
        'e_color': ['k'],      
        'width': 2
    },
    "plotting_features2": {
        'n_color':'#ffbfd7',
        'e_color': 'r',      
        'width': 2,
    },
    #
    "initial_conditions":{
        0: {
            0: (1, 1.),
            1: (4, 1.),
            2: (6, -5.),
            3: (-3, 0.),
            4: (7, 5.0),
            5: (8, 5.0),
            6: (9, 5.0),
        },
        1: {
            0: (1, 1.),
            1: (4, 1.),
            2: (-6, -1.),
            3: (3, 2.),
            4: (7, 5.0),
            5: (8, 5.0),
            6: (9, 5.0),
        },
    },
}