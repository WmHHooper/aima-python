from sklearn import datasets
from sklearn.neural_network import MLPClassifier
import numpy as np
import tensorflow as tf
#
my_data = [
    [0, 1,],
    [2, 3,],
    [4, 5,],
    [6, 7,],
    [8, 9, ],
    [10, 11, ],
    [12, 13, ],
    [14, 15, ],
    [16, 17, ],
    [18, 19, ],
    [20, 21, ],
    [22, 23, ],
    [24, 25, ],
    [26, 27, ],
    [28, 29, ],
    [30, 31, ],
    [32, 33, ],
    [34, 35, ],
    [36, 37, ],
    [38, 39, ],
    [40, 41, ],
    [42, 43, ],
    [44, 45, ],
    [46, 47, ],
    [48, 49, ],
    [50, 51, ],
    [52, 53, ],
    [54, 55, ],
    [56, 57, ],
    [58, 59, ],
    [60, 61, ],
    [62, 63, ],
    [64, 65, ],
    [66, 67, ],
    [68, 69, ],
    [70, 71, ],
    [72, 73, ],
    [74, 75, ],
    [76, 77, ],
    [78, 79, ],
    [80, 81, ],
    [82, 83, ],
    [84, 85, ],
    [86, 87, ],
    [88, 89, ],
    [90, 91, ],
    [92, 93, ],
    [94, 95, ],
    [96, 97, ],
    [98, 99, ],
    [100, 101],
#change


]
slices = tf.data.Dataset.from_tensor_slices(my_data)
next_item = slices.make_one_shot_iterator().get_next()


X = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1],
            [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1],
            [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1],
            [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]]

y = [[1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0],
     [1, 0, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1],
     [1, 0, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1],
     [0, 1, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1]]

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(4), random_state=1)

clf.fit(X, y)

y2 = clf.predict(X)

success = y == y2

iris = datasets.load_iris()

Examples = {

    'IrisDefault': {
        "frame": iris,
    },
}