import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

lan = "en" # tested for "en" or "de"

def get_first_valid_link(url, visited):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get all the relevant elements in the order they appear
    elements = soup.find_all(['p', 'li'])
    
    for element in elements:
        if element.find_parent('table'):
            # Skip elements inside tables
            continue

        first_link = find_first_link_in_element(element)
        if first_link:
            return first_link

    return None

def find_first_link_in_element(element):
    # Find all links within the element
    links = element.find_all('a', href=True)

    for a_tag in links:
        # Check if the link is within round or square brackets
        preceding_text = str(element)[:str(element).find(a_tag['href'])]
        open_round_brackets = preceding_text.count('(')
        close_round_brackets = preceding_text.count(')')
        open_square_brackets = preceding_text.count('[')
        close_square_brackets = preceding_text.count(']')

        if open_round_brackets > close_round_brackets or open_square_brackets > close_square_brackets:
            # Link is within brackets, skip it
            continue

        link = a_tag['href']
        if 'Help:IPA' in link:
            continue
        
        if link.startswith('/wiki/'):
            return 'https://' + lan + '.wikipedia.org' + link

    return None

def main():
    start_url = input("Enter a Wikipedia URL: ")
    visited = set()
    print()
    
    current_url = start_url
    while current_url not in visited:
        visited.add(current_url)
        print("Visiting:", current_url[30:])
        next_url = get_first_valid_link(current_url, visited)

        if not next_url:
            print("No valid link found or end of chain reached.")
            break
        current_url = next_url
    
    print("Visiting:", current_url[30:])
    
    print("\nVisited pages:", len(visited))
    print("The visited pages repeat at:", next_url[30:])
    
    # Exporting to a text file
    with open("wikipedia_loop_data.txt", "a") as file:
        date = datetime.now().strftime("%Y-%m-%d")
        file.write(f"{date}; {lan}; {start_url[30:]}; {len(visited)}; {current_url[30:]}\n")

if __name__ == "__main__":
    main()

