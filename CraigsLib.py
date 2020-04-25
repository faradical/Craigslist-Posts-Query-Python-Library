'''
---------------------------------------------------------------------------------------------------------------------
Name:			CraigsLib.py
Version:		1.0-1
Author:			faradical
Usage:			import CraigsLib as cl
Description:	A library of functions for headless web scraping of Craigslist posts.
Functions:		get_post_details(url)
				
				get_cl_posts(url)

				get_post(url)
Comments:		4/25/2020 - Moved code into this file.
---------------------------------------------------------------------------------------------------------------------
'''
# Import Dependencies
import requests

# Functions
def get_post_details(url):
    # Retrieves only the available description and location data for a post.
    # Really just used as a part of the get_cl_posts() function.
    import requests, bs4

    response = requests.get(url)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        try:
            description = soup.find(id='postingbody').get_text()
        except:
            description = ''
        try:
            location = soup.find('div', class_="mapaddress").get_text()
        except:
            location = ''

        return description, location
    else:
        print(f'Error connecting to {url}. Status code: {response.status_code}')

def get_cl_posts(url):
    # Returns a list of all the postings for a given url.
    import requests, bs4

    response = requests.get(url)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        posts = []
        for i in soup.find_all('li', class_="result-row"):
            link = i.find('a', class_="result-title hdrlnk")['href']
            description, location = get_post_details(link)
            post = {'title': i.find('a', class_="result-title hdrlnk").get_text(),
                    'link': link,
                    'time': i.find('time')['datetime'],
                    'description': description,
                    'location': location}
            posts.append(post)

        return posts
    else:
        print(f'Error connecting to {url}. Status code: {response.status_code}')

def get_post(url):
    # Returns details on a single post.
    import requests, bs4

    response = requests.get(url)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        try:
            title = soup.find(id='titletextonly').get_text()
        except:
            title = ''
        try:
            time = soup.find('time')['datetime']
        except:
            time = ''
        try:
            description = soup.find(id='postingbody').get_text()
        except:
            description = ''
        try:
            location = soup.find('div', class_="mapaddress").get_text()
        except:
            location = ''

        return {'link': url, 'title': title, 'time': time, 'description': description, 'location': location}
    else:
        print(f'Error connecting to {url}. Status code: {response.status_code}')