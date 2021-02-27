# pearson
# spearman
# power log

# %Biden vs covid cases
# %Trump vs covid cases
# %Biden vs %Frequently+Always mask use
# %Trump vs %Frequently+Always mask use
# %Biden vs %Sometimes and below mask use
# %Trump vs %Sometimes and below mask use


from scipy.stats import pearsonr, spearmanr
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score


def pearson(data, category_a, category_b):
    print(f'Pearson Coefficient ({category_a}, {category_b}):\t', pearsonr(data[category_a], data[category_b]))

def spearman(data, category_a, category_b):
    print(f'Spearman Coefficient ({category_a}, {category_b}):\t', spearmanr(data[category_a], data[category_b]))

def linearRegression(data, category_a, category_b):
    X_train, X_test, Y_train, Y_test = train_test_split(data[category_a].to_numpy().reshape(-1, 1), data[category_b].to_numpy(), test_size=0.2)

    linear_model = LinearRegression()
    model = linear_model.fit(X_train, Y_train)
    r2_linear = model.score(X_test, Y_test)
    print(f'R2 of Linear Regression ({category_a}, {category_b}): {r2_linear}')