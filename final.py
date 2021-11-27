import pandas as pd, matplotlib.pyplot as plt, numpy as np
import statsmodels.api as sm
import math

from scipy.stats import gaussian_kde

def main():
    #https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib
    #  https://stackoverflow.com/questions/6148207/linear-regression-with-matplotlib-numpy
    # https://www.tutorialspoint.com/how-can-i-plot-a-single-point-in-matplotlib-python
    
    df = pd.read_csv('pokemon.csv', skiprows=1, names=['Name2', 'Primary Type', 'Attack','Defense', 'Total'], 
    usecols=[1, 2, 4,5,10], encoding='latin-1')
    make_scatterplot(df)
    type_frequency_plot(df)
    make_histogram(df)
    plt.show()

    #print(df)

def make_histogram(df):
    s = df['Total']
    # Put label "Total Stat Value (in tens)"
    #mega = pd.Series(pokemon for pokemon in df['Name2'] if 'mega' in str(pokemon['Name2']).lower())
    #mega = pd.Series(print(pokemon) for pokemon in)

    #print(mega)


    # for pokemon in range(len(df)):
    #     #print(pokemon.type)
    #     if 'mega' in str(df.loc[pokemon, 'Name2']).lower():
    #         #print(str(df.loc[pokemon, 'Name2']).lower())
    #         mega.append(df.iloc[pokemon])
    # Set figure size to automatically be larger
    
    
    fig = plt.figure(figsize=(14, 8))

    s = pd.Series(int(pokemon) for pokemon in df['Total'])

    #print(mega)
    #s = pd.Series(int(pokemon) / 10 for pokemon in df['Total'])
    #plt.hist(s, bins=60, color='#ae9cd6', edgecolor='black', linewidth=1)
    #plt.hist(mega, bins=80, color='red', edgecolor='black', linewidth=1)
    ax = s.plot.hist(bins=45, color='#ae9cd6', edgecolor='black', linewidth=1)

    # Add additional x tick marks
    plt.xticks(np.arange(0, 1200, 50))

    # Add additional y tick marks
    plt.yticks(np.arange(0, 100, 10))

        # Adjust tick fontsize to make it easier to read
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)

    # Background colors
    plt.gcf().set_facecolor('#c8c3d4')
    ax = plt.gca()
    ax.set_facecolor('#c8c3d4')

    # Adjust size of axis and ticks and tick font size

    plt.setp(ax.spines.values(), linewidth=3)
    ax.xaxis.set_tick_params(width=3)
    ax.yaxis.set_tick_params(width=3)
    plt.xlabel("Total Stat Value", fontsize=20)
    plt.ylabel("Frequency", fontsize=20)
    plt.title('Total Pokemon Values', fontsize=30, fontweight='bold')



def type_frequency_plot(df):
    types = [pokemon.capitalize() for pokemon in df['Primary Type']]
    s = pd.Series(types).value_counts().sort_values(ascending = False)
    
    # Set figure size to automatically be larger
    fig = plt.figure(figsize=(9, 10))
    
    # Make bars rainbow colored and slightly wider
    ax = s.plot.bar(width = .75, color=['#ae9cd6', '#8bb9d4', '#a6cfa1', '#dad6a1', '#e1b298', '#e59ca0'])
    #plt.bar(s, 140.1)

    # Add additional y tick marks
    plt.yticks(np.arange(0, 135, 10))

    # Axis labels and title 
    plt.ylabel("Pokemon Freqency", fontsize=20)
    plt.xlabel("Primary Type", fontsize=20)
    plt.title('Frequency of Primary Pokemon Types', fontsize=26, fontweight='bold')
    
    # Make background light grey
    plt.gcf().set_facecolor('lightgrey')
    
    # Add dotted grey lines for each y axis tick
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed')

    # Adjust tick fontsize to make it easier to read
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)

    



def make_scatterplot(df):
    df = pd.read_csv('pokemon.csv', skiprows=1, names=['Attack','Defense'], 
    usecols=[4,5], encoding='latin-1', dtype=np.float64)

    ###############################
    # power_df = pd.DataFrame(columns=['Power'], dtype=np.float64)

    # for row in df.index:
    #     power_df.loc[row, 'Power'] = df.loc[row, 'Defense'] / df.loc[row, 'Attack']
    #df = pd.read_csv('pokemon.csv', skiprows=1, names=['Attack', 'Defense'], 
    #usecols=[4, 5], encoding='latin-1')
    #df = df.set_index('Attack')
    #plt.scatter(df.Attack, df.Defense, s=4)
    ##############################

    # Calculate the point density. x = attack and y = defnese
    xy = np.vstack([df.Attack,df.Defense])
    z = gaussian_kde(xy)(xy)

    # Sort the points by density, so that the densest points are plotted last
    idx = z.argsort()
    x, y, z = df.Attack[idx], df.Defense[idx], z[idx]

    fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, s=100)

    # Best fit line
    m, b = np.polyfit(df.Attack, df.Defense, 1)
    plt.plot(x, m*x + b, color = 'red', lw=3)
    
    ####################
    # x = power_df.index.values
    # print(x)
    # X = sm.add_constant(x)
    # model = sm.OLS(power_df, X)
    # line = model.fit()
    # print(line.params)
    # y = line.params['x1'] * x + line.params['const']
    # plt.plot(x, y, 'red')
    ###################

    # Background colors
    plt.gcf().set_facecolor('#d4f0ff')
    ax = plt.gca()
    ax.set_facecolor('#d4f0ff')

    # X and Y axis size and labels
    plt.xlim(0, 200)
    plt.xlabel("Attack", fontsize=20)

    plt.ylim(0, 225)
    plt.ylabel("Defense", fontsize=20)


    #Border color
    ax.spines['right'].set_color('#d4f0ff')
    ax.spines['top'].set_color('#d4f0ff')

    # Adjust size of axis and ticks and tick font size
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.setp(ax.spines.values(), linewidth=3)
    ax.xaxis.set_tick_params(width=3)
    ax.yaxis.set_tick_params(width=3)

    # Figure title
    plt.title('Power Distribution of All Pokemon', fontsize=26, fontweight='bold')
    
    # Automatically make the figure larger
    fig.set_size_inches(10, 8)

    # Calculate the mean (I am thinking about changing this to median because that 
    # seems like a more appropriate choice for this dataset)
    total_attack = 0
    total_defense = 0
    total = 0
    for row in df.index:
        total_attack += df.loc[row, 'Attack']
        total_defense += df.loc[row, 'Defense']
        total += 1
    mean_attack = total_attack / total
    mean_defense = total_defense / total

    # Plot the mean point on the graph
    plt.plot(mean_attack, mean_defense, marker="o", markersize=12, markeredgecolor = "red", markerfacecolor="red")

    # Add lines to the mean to make it stand out
    plt.hlines(y=74.66, xmin=0, xmax = 80.46, color='grey', linestyle='--', linewidth = 2)
    plt.vlines(x=80.46, ymin=0, ymax = 74.66, color='grey', linestyle='--', linewidth = 2)



if __name__ == "__main__":
    main()