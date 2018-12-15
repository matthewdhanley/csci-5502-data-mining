import matplotlib.pyplot as plt
import pickle
import pandas as pd
import numpy as np


if __name__=="__main__":
    key='review_length_variance'
    f = open("features_df_3mo.pi", mode='rb')
    df = pickle.load(f)
    age = list(df[key])
    # age = [x-min(age) for x in age]

    df2 = df[df['is_open'] == '1']
    age2 = list(df2[key])
    # age2 = [x - min(age2) for x in age2]

    df3 = df[df['is_open'] == '0']
    age3 = list(df3[key])
    # age3 = [x - min(age3) for x in age3]

    fig, ax = plt.subplots(dpi=300, figsize=(3, 3))
    # n, bins, patches = ax.hist(age, bins=200, alpha=0.7,label='All',density=True)
    n2, bins2, patches2 = ax.hist(age2, bins=500, alpha=0.7, label='Open', density=True)
    n3, bins3, patches3 = ax.hist(age3, bins=500, alpha=0.7, label='Closed', density=True)
    ax.grid(linestyle='--', color='black', linewidth=0.5, alpha=0.3)
    ax.set_xlabel('Average Review Length')
    ax.set_ylabel('Density')
    ax.set_xlim(min(age), 150000)
    ax.set_ylim(0, 0.00001)
    ax.legend()
    fig.tight_layout()
    plt.show()
    fig.savefig('review_len.png', bbox_inches='tight')