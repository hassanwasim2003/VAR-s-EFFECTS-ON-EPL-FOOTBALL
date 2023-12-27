import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import numpy as np
plt.style.use('ggplot')

# This program displays an animated bar graph to compare each season's overall
# points (with and without VAR penalty calls).

# Abbreviated Team Names
abbv = {
    'Liverpool' : "L'pool",
    'Tottenham' : 'Spurs',
    'West Ham': 'W. Ham',
    'Leicester City': 'LCFC',
    'Newcastle Utd': 'NUFC',
    'Crystal Palace': 'CPFC',
    'Brentford': "Bees",
    'Aston Villa': "AVFC",
    'Southampton': 'Soton',
    'Leeds Utd': 'Leeds',
    'Norwich City': 'NW City',
    'Sheffield Utd':  'SUFC',
    'AFC Bournemouth':  'AFCB',
    'W.B. Albion': 'WBA'
}

# This function returns the average of a list
def getAverage(numList):
  total = 0
  for i in range(len(numList)):
    total += numList[i]
  return (float(total) / float(len(numList)))

# These functions will help set the bar positions at each frame.
def listAt(aList, index):
  finalList = []
  for i in range(len(aList)):
    finalList.append((intervalList(aList[i]))[index])
  return finalList

def intervalList(pts):
  return (np.linspace(0, pts)).tolist()

def seasons_str(csv):
  column_names = list(csv.columns)
  season_string = ""
  for cols in column_names:
    if re.match(r"20\d\d/\d\d", cols) and cols != '2017/18' and cols != '2018/19':
      season_string += f'\n- {cols}'

  return season_string

try:
    # Read and parse data from CSV file using URL
    data = pd.read_csv("https://raw.githubusercontent.com/SebastianAshcallay/CMSC206/main/GroupProject_PL_Table[version2].csv")

    # Ask user to indicate which season to display
    #season = input("\nWhich season do you want to graph? \n- 2019/20\n- 2020/21\n- 2021/22\n>>> ")
    season = input(f"\nWhich season do you want to graph? {seasons_str(data)}\n>>> ")
    teams = data[season].tolist()
    for n in range(len(teams)):
      if teams[n] in abbv.keys():
        teams[n] = abbv[teams[n]]

    # Sets VAR vs. no VAR overall points for each team in the indicated season
    varPts = data[f'Pts ({season})'].tolist()
    noVarPts = data[f'Pts (No VAR)({season})'].tolist()

    # Add Average Points (VAR v. No VAR)
    avgVarPts = getAverage(varPts)
    varPts.append(int(round(avgVarPts)))
    avgNoVarPts = getAverage(noVarPts)
    noVarPts.append(int(round(avgNoVarPts)))
    teams.append('Avg Pts')

    # Print Results
    print(f"\nIn the Premier League's {season} season, the participating teams averaged"
            + f"\na total of {round(avgVarPts)} pts. with VAR, and a total of {round(avgNoVarPts)} pts. without VAR.")
    if round(avgNoVarPts) > round(avgVarPts):  
      print(f'\n>>> Teams Averaged more Points without VAR <<<')
    elif round(avgVarPts) > round(avgNoVarPts):
      print(f'\n>>> Teams Averaged more Points with VAR <<<')
    else:
      print(f'\n>>> Teams Averaged same number of Points with/without VAR <<<')

    # Describe Red/Green X-axis Labels
    print('\n\nNote: X-axis label colors describe which teams were benefitted/disadvantaged'
            + '\nby the implementation of VAR:')
    print('* Red: Disadvatanged (dropped positions in final standings)')
    print('* Green: Benefitted (climbed positions in final standings)')
    print('* Black: Same position with/without VAR penalty calls\n\n')

    # Create Graph Background
    df = pd.DataFrame(dict(graph= teams,n=varPts, m=noVarPts))
    ind = np.arange(len(df))
    width = 0.4

    fig, ax = plt.subplots()

    # Add FuncAnimation
    count = 0
    def animate(i):
        global count
        a1 = listAt(varPts, count) # Sets points per frame
        a2 = listAt(noVarPts, count) # Sets points (no VAR) per frame

        plt.cla() # Clears graph, sets space for new graph
        ax.barh(ind, a1, width, color='blue', label='VAR (Penalty Calls)') # First bar
        ax.barh(ind + width, a2, width, color='green', label='No VAR') # Second bar
        ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)], xlim=[0,110])
        plt.gca().invert_yaxis()
        plt.xlabel(f'Pts (Season: {season})')
        ax.legend()

        # Show which teams had advantages/disadvantages as a result of VAR
        shifts = data[f'Shift({season})'].tolist()
        for i in range(len(shifts)):
          if shifts[i] < 0:
            plt.gca().get_yticklabels()[i].set_color("red")
          elif shifts[i] > 0:
            plt.gca().get_yticklabels()[i].set_color("green")

        plt.legend()
        plt.title("Premier League Table (VAR vs. No VAR)")

        count += 1
        
    ani = FuncAnimation(fig, animate, frames = 49, interval = 100, repeat= False)
    plt.show()

except Exception as ex:
    print(f'Error: [{str(ex)}]')
