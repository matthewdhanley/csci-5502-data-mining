import pickle
import matplotlib.pyplot as plt
import pygal
import numpy as np
from scipy.interpolate import spline



if __name__ == "__main__":
    p = open('time_from_open.pickle', 'rb')
    a = pickle.load(p)
    weeks = [int(x) for x in a.keys()]
    num_reviews = [int(x) for x in a.values()]
    num_reviews = [x for _,x in sorted(zip(weeks, num_reviews))]
    weeks = sorted(weeks)
    # chart = pygal.Bar()
    # chart.title = "Number of Restraunts with Y reviews X weeks from opening"
    # chart.x_labels = map(str, range(0, len(weeks)))
    # chart.y_labels = 'Number of Restaurants'
    # chart.add('', num_reviews)
    # chart.render()
    f, ax = plt.subplots(dpi=300, figsize=(3, 3))
    # ax.set_xlabel('Weeks from Open')
    # ax.set_ylabel('Number of Restaurants\n w/ at least one review')
    # # ax.plot(weeks, num_reviews)
    # d = np.zeros_like(num_reviews)
    # ax.grid(linestyle='--',color='black', linewidth=0.5, alpha=0.3)
    # ax.set_ylim(0, 1250)
    # ax.set_xlim(0,max(weeks))
    # print(d.shape)
    # ax.fill_between(weeks, num_reviews, alpha=0.6)
    # plt.savefig('foo.png', bbox_inches='tight')

