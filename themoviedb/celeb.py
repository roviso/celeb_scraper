#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
from imdb import IMDB
from parser import ImdbParser

from mediawikiapi import MediaWikiAPI


imdb = IMDB()
mediawikiapi = MediaWikiAPI()


# Define your API keys and URLs here
movieAPI = 'fec8616772d5432aacc95609416a2129'
movieBaseURL = "https://api.tmdb.org/3/search/person?api_key="+movieAPI+"&query="


def fetch_actor_information(actor_name):
    nameCall = titleCase(actor_name)

    tmdbURL = movieBaseURL + nameCall
    
    response1 = requests.get(tmdbURL)
    
    if response1.status_code != 200:
        print("Error:", response1.status_code)
        return
    
    resp1_data = response1.json()

    actor_info_dict = {}

    if resp1_data['total_results'] == 0:
        print("No Such Actor")
        actor_info_dict['error'] = "No Such Actor"
    else:
        movies_list = []
        for movie in resp1_data['results'][0]['known_for']:
           
            movies_list.append(movie)

        actor_id = resp1_data['results'][0]['id']

        response2 = requests.get(f"https://api.themoviedb.org/3/person/{actor_id}?api_key={movieAPI}&language=en-US")

        if response2.status_code != 200:
            print("Error:", response2.status_code)
            return

        resp2_data = response2.json()

        actor_details = resp2_data

        
        actor_info_dict['movies'] = movies_list
        actor_info_dict['actor_details'] = actor_details

    return actor_info_dict

def titleCase(name):
    return name.title()

def formatDate(date):
    return date  # Placeholder, actual formatting code should go here



def get_celeb_networth_link(celeb_name):
    """
    Fetch the link for the given celebrity name from celebritynetworth.com.
    """
    url = f"https://www.celebritynetworth.com/?s={celeb_name.replace(' ', '+')}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    ol_tag = soup.find('ol', class_='post_list')
    if ol_tag:
        li_tag = ol_tag.find('li')
        if li_tag:
            a_tag = li_tag.find('a', class_='anchor')
            if a_tag:
                return a_tag['href']
    return None

def extract_section_content(h2_tag):
    """
    Extract content following the given h2 tag until the next h2 tag.
    """
    content = []
    for sibling in h2_tag.find_next_siblings():
        if sibling.name == 'h2':
            break
        if sibling.name == 'p':
            content.append(sibling.get_text(strip=True))
    return ' '.join(content)

def extract_celeb_info(link, celeb_name):
    """
    Extract information about the celebrity from the provided link.
    """
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    div_tag = soup.find('div', id='profile_bio')
    info = {}
    if div_tag:
        for dt, dd in zip(div_tag.find_all('dt'), div_tag.find_all('dd')):
            key = dt.get_text(strip=True)
            value = dd.get_text(strip=True)
            info[key] = value

    toc_div = soup.find('div', id='cnw_toc')
    if toc_div:
        next_h2 = toc_div.find_next_sibling('h2')
        if next_h2 and ("What is" in next_h2.get_text() or f"What was {celeb_name}'s Net Worth" in next_h2.get_text()):
            info["Net Worth Content"] = extract_section_content(next_h2)

        toc_info = {}
        for li in toc_div.find_all('li'):
            section_name = li.a.get_text(strip=True)
            section_id = li.a['data-section-id']
            section_h2 = soup.find('h2', id=section_id)
            if section_h2:
                toc_info[section_name] = extract_section_content(section_h2)
        info['Table of Contents'] = toc_info

    return info

def main():
    celeb_name = input("Enter the celebrity name: ")
    link = get_celeb_networth_link(celeb_name)
    if link:
        info = extract_celeb_info(link, celeb_name)
        if info:
            with open(f"{celeb_name.replace(' ', '_')}.json", 'w') as f:
                json.dump(info, f, indent=4)
            print(f"Information for {celeb_name} saved to {celeb_name.replace(' ', '_')}.json")
        else:
            print(f"No information found for {celeb_name}")
    else:
        print(f"No link found for {celeb_name}")
    
    # Fetch actor's movie information
    actor_info = fetch_actor_information(celeb_name)
    
    actor_info["wiki_summary"] = mediawikiapi.summary(celeb_name, auto_suggest = False)
    
    actor_info["imdb_summary"] = imdb.person_by_name(celeb_name)
    
    if actor_info:
        # Merge the actor's movie information with the previously extracted celebrity information
        info.update(actor_info)
        
    
    
     # Save the combined information to a JSON file
    if info:
        with open(f"{celeb_name.replace(' ', '_')}.json", 'w') as f:
            json.dump(info, f, indent=4)
        print(f"Information for {celeb_name} saved to {celeb_name.replace(' ', '_')}.json")
    else:
        print(f"No information found for {celeb_name}")
        
        
if __name__ == "__main__":
    main()
