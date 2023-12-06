import pandas as pd

from player import Player

def convert_to_excel(rawdata):

    filename = 'output/tournament_results.xlsx'
    # Define basic fixed column names
    fixed_columns = ['#', 'Nimi', 'Pisteet', 'Buchholz', 'Sonneborn-Berger']

    # add results columns for each round after the second fixed column
    first_player: Player = rawdata[0]
    results_length = len(first_player.results)
    columns = fixed_columns[:2] + [i for i in range(1, results_length + 1)] + fixed_columns[2:]

    # Initial data structure
    data = {column: [] for column in columns}

    for player in rawdata:
        data['#'].append(player.order)
        data['Nimi'].append(player.name)
        data['Pisteet'].append(player.points)
        data['Buchholz'].append(player.buchholz)
        data['Sonneborn-Berger'].append(player.sonneborn_berger)

        for round_number, result in enumerate(player.results):
            round_column = round_number + 1
            data[round_column].append(float(result) if len(result) > 0 else '')

    # Debugging
    for key, value in data.items():
        print(f'{key}: {value}')

    # Create a Pandas dataframe from the list of dictionaries
    df = pd.DataFrame(data)

    # Create a Pandas Excel writer
    writer = pd.ExcelWriter(filename)

    # Convert the dataframe to an XlsxWriter Excel object
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    writer.close()
    print(f'Excel file {filename} created successfully.')
    
