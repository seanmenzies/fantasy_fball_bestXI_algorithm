import pandas as pd
import json
from random import randint

with open('fantasy.json') as json_file:
    data = json.load(json_file)

# sort data
elements_df = pd.DataFrame(data['elements'])
element_types = pd.DataFrame(data['element_types'])
teams_df = pd.DataFrame(data['teams'])

key_info = elements_df[['second_name', 'total_points', 'now_cost', 'element_type']]
key_info['position'] = key_info.element_type.map(element_types.set_index('id').singular_name)
key_info['team'] = elements_df.team.map(teams_df.set_index('id').name)

budget = 10000
sorted_players = key_info.sort_values(by='total_points', ascending=False)
goalkeepers = 0
defenders = 0
midfielders = 0
forwards = 0
for index, player in sorted_players.iterrows():
    if player['position'] == 'Goalkeeper' and goalkeepers < 10:
        goalkeepers += 1
    elif player['position'] == 'Defender' and defenders < 20:
        defenders += 1
    elif player['position'] == 'Midfielder' and midfielders < 20:
        midfielders += 1
    elif player['position'] == 'Forward' and forwards < 15:
        forwards += 1
    else:
        sorted_players.drop(index, inplace=True)

order_by_pos = pd.CategoricalDtype(['Goalkeeper', 'Defender', 'Midfielder', 'Forward'], ordered=True)
sorted_players['position'] = sorted_players['position'].astype(order_by_pos)
sorted_players = sorted_players.sort_values(by=['position', 'total_points'], ignore_index=True)

bestXI_points = 0
current_bestXI = None
# initialise indexes of different positions
gk_count = 0
df_count = 10
mf_count = 30
fw_count = 50
# initialise iterations
count = 0
# create current firstXI dataframe
firstXI = sorted_players.copy()


# pushes indexes forward one position at a time so different permutations occur
def switch_players(gk_count, df_count, mf_count, fw_count):
    num = randint(0, 4)
    if num == 1:
        if gk_count < 9:
            gk_count += 1
        else:
            gk_count = 0
    elif num == 2:
        if df_count < 29:
            df_count += 1
        else:
            df_count = 10
    elif num == 3:
        if mf_count < 49:
            mf_count += 1
        else:
            mf_count = 30
    else:
        if fw_count < 64:
            fw_count += 1
        else:
            fw_count = 50
    return gk_count, df_count, mf_count, fw_count


while True:
    idx = 0
    # initialise limit per position
    goalkeepers = 0
    defenders = 0
    midfielders = 0
    forwards = 0
    # empty table whenever loop restarts
    firstXI = firstXI.iloc[0:0]
    # loop through sliced data filling up the team according to 3-4-3 formation
    for index, player in sorted_players.iterrows():
        # break for loop if rules are broken
        if not firstXI.empty and max(firstXI['team'].value_counts().values) > 2:
            break
        elif gk_count < index < 10 and goalkeepers < 2:
            firstXI.loc[idx] = player
            idx += 1
            goalkeepers += 1
        elif df_count <= index < 30 and defenders < 5:
            firstXI.loc[idx] = player
            idx += 1
            defenders += 1
        elif mf_count <= index < 50 and midfielders < 5:
            firstXI.loc[idx] = player
            idx += 1
            midfielders += 1
        elif fw_count <= index < 65 and forwards < 3:
            firstXI.loc[idx] = player
            idx += 1
            forwards += 1
        else:
            continue
    # break while loop if rules are broken so invalid teams are not checked
    if not firstXI.empty and max(firstXI['team'].value_counts().values) > 2 or len(firstXI.index) != 15:
        gk_count, df_count, mf_count, fw_count = switch_players(gk_count, df_count, mf_count, fw_count)
        continue
    else:
        valid = True
        total_cost = firstXI['now_cost'].sum()
        total_points = firstXI['total_points'].sum()
        valid = False if total_cost > budget else True
        # if everything is kosher, add team to current bestXI
        if valid and total_points > bestXI_points:
            current_bestXI = firstXI.copy()
            bestXI_points = current_bestXI['total_points'].sum()
        else:
            # count failed iterations
            count += 1
            print(count)
        gk_count, df_count, mf_count, fw_count = switch_players(gk_count, df_count, mf_count, fw_count)
        # set total iterations when total_points <= bestXI_points
        # prints out results when total iterations hit
        if count >= 250 and current_bestXI is not None:
            print(current_bestXI)
            print(bestXI_points)
            break
