import regex
from convert_to_excel import convert_to_excel
from player import Player

# Define a regular expression pattern
# \p{L} : any kind of letter from any language
pattern = regex.compile(
    r'(^\d{3}\s*)'    # unwanted garbage at the beginning of the line
    r'(?P<id>\d+)\s*'
    r'(?P<name>\p{L}[\p{L}\s,]*\p{L})\s*'
    r'(\d{3,4}\s*)'    # unwanted garbage in the middle of the line
    r'(?P<points>[\d\.]+)'
    r'(\s*)'    
    r'(?P<order>[\d]+)'
    r'(\s*)'
    r'(?P<result_chunk>.*)'    
)


# Function to convert tournament results into HTML table
def convert_to_html(tournament_results):

    # Create a list of players object
    players = []

    # # Parse tournament results (basic points and won/lost games)
    for line in tournament_results:
        
        # Initial single player object
        player = Player()

        match = pattern.match(line)
        if not match:
            print(f"Invalid line: {line}")
            continue

        player.id = int(match.group('id'))
        player.name = match.group('name')
        player.points = float(match.group('points'))

        # Split the result string into chunks of three characters
        result_chunk = match.group('result_chunk').split()
        chunks = [result_chunk[i:i + 3] for i in range(0, len(result_chunk), 3)]
        # Extract opponent IDs with corresponding results
        for chunk in chunks:
            opponent_id  = int(chunk[0])
            result = int(chunk[2])   
            player.opponent_ids.append(opponent_id)
            if result == 1:  # 1 indicates a won game
                player.won_opponent_ids.append(opponent_id)
            elif result == 0.5: # 0.5 indicates a drawn game
                player.drawn_opponent_ids.append(opponent_id)
            elif result == 0: # 0 indicates a lost game
                player.lost_opponent_ids.append(opponent_id)

        players.append(player)

    # Calculate Buchholz and Sonneborn-Berger points
    for player in players:
        # Calculate Buchholz points. Sum all points of opponents
        player.buchholz = sum([opponent.points for opponent in players if opponent.id in player.opponent_ids])
        # Calculate Sonneborn-Berger points
        player.sonneborn_berger = (
            sum([opponent.points for opponent in players if opponent.id in player.won_opponent_ids]) +
            0.5 * sum([opponent.points for opponent in players if opponent.id in player.drawn_opponent_ids])            
        )

    # Add order column in which players are sorted by points, Buchholz points and Sonneborn-Berger points
    for i, player in enumerate(sorted(players, key=lambda x: (x.points, x.buchholz, x.sonneborn_berger), reverse=True)):
        player.order = i + 1

    # Replace player IDs with order numbers
    lookup_table = {player.id: player.order for player in players}
    for player in players:
        player.opponent_ids = [lookup_table[pid] for pid in player.opponent_ids]
        player.won_opponent_ids = [lookup_table[pid] for pid in player.won_opponent_ids]
        player.drawn_opponent_ids = [lookup_table[pid] for pid in player.drawn_opponent_ids]
        player.lost_opponent_ids = [lookup_table[pid] for pid in player.lost_opponent_ids]
        
    # Create a list of results for each player
    for player in players:
        for opponent_id in range(1, len(players) + 1):
            if opponent_id in player.won_opponent_ids:
                player.results.append('1')
            elif opponent_id in player.drawn_opponent_ids:
                player.results.append('½')
            elif opponent_id in player.lost_opponent_ids:
                player.results.append('0')
            else:
                player.results.append('')

    # Sort players by order
    players = sorted(players, key=lambda x: x.order)

    # Header for the HTML table
    html_content = '<table border="1" cellpadding="3" cellspacing="2">\n'
    html_content += '\t<thead>\n'
    html_content += '\t\t<th>#</th>\n'
    html_content += '\t\t<th>Nimi</th>\n'

    # Add round numbers to the header
    for i in range(1, len(players)+1):
        html_content += f'\t\t<th width="5%" style="text-align: center;">{i}</th>\n'
    # Add final statistics to the header
    html_content += '\t\t<th>Pisteet</th>\n'
    html_content += '\t\t<th>Buchholz</th>\n'
    html_content += '\t\t<th>Sonneborn-Berger</th>\n'
    html_content += '\t</thead>\n'
    html_content += '\t<tbody>\n'

    # Add rows to the HTML table
    for player in players:
        html_content += '\t\t<tr>\n'
        html_content += f'\t\t\t<td>{player.order}</td>\n'
        html_content += f'\t\t\t<td>{player.name}</td>\n'

        # Add results for each round
        for index, result in enumerate(player.results):
            # Order starts from 1, but index starts from 0
            if index  +1 == player.order:
                html_content += f'\t\t\t<td class="silver_bkg" style="text-align: center;">&nbsp;</td>\n'
            elif result == '':
                html_content += f'\t\t\t<td style="text-align: center;">&nbsp;</td>\n'
            else:
                html_content += f'\t\t\t<td style="text-align: center;">{result}</td>\n'

        # Add final statistics
        html_content += f'\t\t\t<td>{player.points}</td>\n'
        html_content += f'\t\t\t<td>{player.buchholz}</td>\n'
        html_content += f'\t\t\t<td>{player.sonneborn_berger}</td>\n'
        html_content += "\t\t</tr>\n"

    # Footer for the HTML table
    html_content += "\t</tbody>\n"
    html_content += "</table>\n"

    convert_to_excel(players)

    return html_content