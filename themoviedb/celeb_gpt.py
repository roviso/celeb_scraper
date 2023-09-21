#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
from imdb import IMDB
from parser import ImdbParser

from mediawikiapi import MediaWikiAPI
import openai

imdb = IMDB()
mediawikiapi = MediaWikiAPI()

API_KEY: str = "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"

openai.api_key = API_KEY

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


def bio_summary(data):

    system_message = {
        "role": "system",
        # "content": prompts['system_message_content']
        "content": f'''You are a powerful ai tasked to write long blog on the biography of a celebrity with the data given to you. Use the Template below to create a blog about the individual:
        Keyword Bio: Early Life, Relationship, Career & Net Worth
Introduction
***  FILL IN THE CELEBRITY INTRODUCTION ***

Keyword | Quick Facts
*** Table Showing following key and values
1) Real Name/Full Name 
2) Nick Name
3) Gender
4) Known as
5) Date of Birth
6) Birthplace
7) Father
8) Mother
9) Siblings
10) Age
11) Height
12) Weight
13) Ethnicity
14) Nationality
15) Religion
16) Education
17) Profession
18) Monthly Income
19) Net Worth
20) Marital Status
21) Wife/Husband or (Bf/gf)
22) Marriage Date (if married)
23) Children
      
        
Keyword | Early Life, Family (Siblings)
*** WRITE ABOUT THE CELEBRITY Early Life, Family (Siblings) ***

Keywords | Education & Early Career

Keywords |Ethnicity, Nationality & Religion

Keywords | Quotes.

Keyword | Career

Keyword | Dating History(Boyfriend/Girlfriend?)

Keywords | Podcast

Keywords |Trophies and Honours:

Keyword | Stats

Keyword | Age, Height, and Weight (Body Measurements)

Keyword | Salary and Net Worth

Keyword | Income Source, Brand Promotion & Collaborations

Keyword | Net worth in Different Currencies, including Bitcoin

Keywords | Charity works

Keyword | Cars, Houses, Assets


Keyword | Social Media Presence

Conclusion
  '''
    }
    
    user_message = {
        "role": "user", 
        "content": f'here is the data of celebrity i want to summarize: \n\n{data}'
    }

    messages = [
        system_message,
        user_message
    ]

    print(messages)

    # MODEL = "gpt-3.5-turbo-0301"
    MODEL = "gpt-4"
    for i in range(1,4):
        # try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
        )
        print("openai respones: ", response)
        en_result = response.choices[0].message["content"]
        return en_result
    
    

def main():
    celeb_name = input("Enter the celebrity name: ")
    link = get_celeb_networth_link(celeb_name)
    if link:
        info = extract_celeb_info(link, celeb_name)
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
        with open(f"celeb_output/{celeb_name.replace(' ', '_')}.json", 'w') as f:
            json.dump(info, f, indent=4)
        print(f"Information for {celeb_name} saved to celeb_output/{celeb_name.replace(' ', '_')}.json")
        biosum = bio_summary(info)
        # Open a file in write mode ('w')
        with open(f"celeb_output/generated_{celeb_name.replace(' ', '_')}.txt", "w") as f:
            # Write the string to the file
            f.write(biosum)
    else:
        print(f"No information found for {celeb_name}")
        
        
if __name__ == "__main__":
    main()