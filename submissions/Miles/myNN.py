from sklearn import datasets
from sklearn.neural_network import MLPClassifier
import traceback

'''
My bayes into Neural Networks
'''

from submissions.Miles import food



class DataFrame:
    data = []  # grid of floating point numbers
    feature_names = []  # column names
    target = []  # list of the target value
    target_names = []  # target labels



foodFF = DataFrame()  # what I pass on to examples
foodFF.data = []
targetData = []

'''
Extract data from the CORGIS food.
'''


food = food.get_reports()

for info in food:
    try:
        # item = str(info["Category"])
        item = float(info["Data"]["Fat"]["Saturated Fat"])
        targetData.append(item)

        fiber = float(info["Data"]["Fiber"])
        carbohydrate = float(info["Data"]["Carboydrate"]) # they misspelled carbohydrates LOL
        water = float(info["Data"]["Water"])
        vitamin = float(info["Data"]["Vitamins"]["Vitamin C"])

        foodFF.data.append([fiber, carbohydrate, water, vitamin])

    except:
        traceback.print_exc()


foodFF.feature_names = [


    'Fiber',
    'Carbohydrates',
    'Water',
    'Vitamin C',
]

'''
Build the target list,
one entry for each row in the input frame.

The Naive Bayesian network is a classifier,
i.e. it sorts data points into bins.
The best it can do to estimate a continuous variable
is to break the domain into segments, and predict
the segment into which the variable's value will fall.
In this example, I'm breaking Trump's % into two
arbitrary segments.
'''

foodFF.target = []



def foodTarget(percentage):

    if percentage > 10:
        return 1
    return 0



for item2 in targetData:
    # choose the target
    target_t = foodTarget(item2)
    foodFF.target.append(target_t)
# comparing the fat contents of a food to other contents of same food
foodFF.target_names = [
    'Saturated Fat is <= 10%',
    'Saturated Fat is > 10%',
    # 'Butter',
    # 'Milk',
    # 'Cheese'
]

Examples = {
    'Food': foodFF,
}

# start the new info for neural networks


'''
Make a custom classifier,
'''
mlpc = MLPClassifier(
    hidden_layer_sizes = (100,),
    activation = 'identity',
    solver='lbfgs', # 'adam',
    # alpha = 0.0001,
    batch_size='auto',
    learning_rate = 'adaptive', # 'constant',
    # power_t = 0.5,
    max_iter = 1000, # 200,
    # shuffle = True,
    # random_state = None,
    # tol = 1e-4,
    # verbose = False,
    # warm_start = False,
    # momentum = 0.9,
    # nesterovs_momentum = True,
    # early_stopping = False,
    # validation_fraction = 0.1,
    # beta_1 = 0.9,
    # beta_2 = 0.999,
    # epsilon = 1e-8,
)

'''
Try scaling the data.
'''
foodScaled = DataFrame()

def setupScales(grid):
    global min, max
    min = list(grid[0])
    max = list(grid[0])
    for row in range(1, len(grid)):
        for col in range(len(grid[row])):
            cell = grid[row][col]
            if cell < min[col]:
                min[col] = cell
            if cell > max[col]:
                max[col] = cell

def scaleGrid(grid):
    newGrid = []
    for row in range(len(grid)):
        newRow = []
        for col in range(len(grid[row])):
            try:
                cell = grid[row][col]
                scaled = (cell - min[col]) \
                         / (max[col] - min[col])
                newRow.append(scaled)
            except:
                pass
        newGrid.append(newRow)
    return newGrid

setupScales(foodFF.data)
foodScaled.data = scaleGrid(foodFF.data)
foodScaled.feature_names = foodFF.feature_names
foodScaled.target = foodFF.target
foodScaled.target_names = foodFF.target_names

Examples = {
    'FoodDefault': {
        'frame': foodFF,
    },
    'FoodSGD': {
        'frame': foodFF,
        'mlpc': mlpc
    },
    'FoodScaled': {
        'frame': foodScaled,
    },
}