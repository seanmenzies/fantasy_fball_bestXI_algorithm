# fantasy football bestXI algorithm

## Rules
- Only two players from each premier league team
- Transfer budget of £100 million
- 3-4-3 formation with no subs
- Data taken from 2020/2021 season

## Features
- Loads raw data from json file (load_data.py) taken from official fantasy premier league API
- Organises and sorts data by position and total points
- Takes slices of top x players from each position and feeds into separate dataframe
- Adds players into a first XI, checks for validity according to above rules, calculates total points, keeping the current bestXI in memory for comparison, then repeats the process with different permutations of players for n iterations. Maximum results occurred around 250-300 iterations.
