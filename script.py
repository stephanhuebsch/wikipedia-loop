import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def get_first_valid_link(url, visited):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first paragraph
    p_tags = soup.find_all('p')
    for p in p_tags:
        # Find all links within the paragraph
        links = p.find_all('a', href=True)

        for a_tag in links:
            # Check if the link is within brackets
            preceding_text = str(p)[:str(p).find(a_tag['href'])]
            if '(' in preceding_text and ')' not in preceding_text:
                # Link is within brackets, skip it
                continue

            link = a_tag['href']
            if link.startswith('/wiki/'):
                return 'https://en.wikipedia.org' + link

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
    with open("wikipedia_chain_data.txt", "a") as file:
        date = datetime.now().strftime("%Y-%m-%d")
        file.write(f"{date}; {start_url[30:]}; {len(visited)}; {current_url[30:]}\n")

if __name__ == "__main__":
    main()

