import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

lan = "de" # can be "en" or "de"

def get_first_valid_link(url, visited):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first paragraph
    p_tags = soup.find_all('p')
    for p in p_tags:
        if p.find_parent('table'):
            # Skip paragraphs inside tables
            continue

        # Find all links within the paragraph
        links = p.find_all('a', href=True)

        for a_tag in links:
            # Check if the link is within brackets
            preceding_text = str(p)[:str(p).find(a_tag['href'])]
            open_brackets = preceding_text.count('(')
            close_brackets = preceding_text.count(')')

            if open_brackets > close_brackets:
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

