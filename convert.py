import os

from convert_to_html import convert_to_html

# Function to read tournament results from file
def read_tournament_results(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

# Function to save HTML content to a file
def save_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Main function
def main():
    # Ensure 'data' and 'output' directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    # Read tournament results from file
    tournament_results_path = 'data/tournament_results.txt'
    tournament_results = read_tournament_results(tournament_results_path)

    # Convert tournament results to HTML
    html_content = convert_to_html(tournament_results)

    # Save HTML content to file
    output_file_path = 'output/table.html'
    save_to_file(output_file_path, html_content)

    print(f"HTML table saved to: {output_file_path}")

if __name__ == "__main__":
    main()
