import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data set
dataset = sns.load_dataset(name='flights')
# print(dataset)

# Visualizing statistical relationships
# Plot
sns.relplot(x='passengers', y='month', data=dataset)
sns.relplot(x='passengers', y='month', hue='year', data=dataset)

# Plotting categorical data
dataset = sns.load_dataset(name='tips')
sns.catplot(x='day', y='total_bill', data=dataset)

# Visualizing the distribution of dataset
# Uni-variant or Bi-variant
from scipy import stats
c = np.random.normal(loc=5, size=100, scale=2)
sns.distplot(c)

