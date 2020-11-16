# importing required libraries for project
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint


# tells for loop how to go about scraping each page
pages = np.arange(1,1001,50)

# translates any movie titles not in english to english
headers = {"Accept-Language": "en-US, en;q=0.5"}

# initianlize empty lists to store data
titles = []
years = []
age_ratings = []
time = []
genres = []
imdb_ratings = []
metascores = []
directors = []
votes = []
us_gross = []

# loop to grab each page
for page in pages:
	
	# target URL to scrape
	page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&start=" + str(page) + "&ref_=adv_nxt", headers=headers)

	# parse contnets of results
	soup = BeautifulSoup(page.text, "html.parser")

	# Grabs each movie to be searched
	movie_div = soup.findAll('div', class_='lister-item mode-advanced')
	container = movie_div[0]

	# controls the flow of how often the webpage is scaped
	sleep(randint(2,6))

	# Iterate over each item to be stored
	for container in movie_div:

		# Grabs the title of each movie
		title = container.h3.a.text
		titles.append(title)

		# Grabs the year each movie
		year = container.h3.find('span', class_='lister-item-year').text
		years.append(year)

		# Grbas the rating of each movie
		age = container.find('span', class_='certificate').text if container.p.find('span', class_='certificate') else 'N/A'
		age_ratings.append(age)

		# Grabs the length of each movie
		length = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else 'N/A'
		time.append(length)

		#grabs the genre of each movie
		genre = container.p.find('span', class_='genre').text
		genres.append(genre)

		# Grabs the rating of each movie
		rating = float(container.strong.text)
		imdb_ratings.append(rating)

		# Grabs metascore
		score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else 'N/A'
		metascores.append(score)

		# grabs the director of each movie
		director = container.find('p', class_='').find_all('a')[0].text
		directors.append(director)

		# Holds votes/gross
		nv = container.findAll('span', attrs={'name':'nv'})

		# Grabs votes from nv of each movie
		vote = nv[0].text
		votes.append(vote)

		# Grabs gross earning from nv for movies with field else leave blank
		grosses = nv[1].text if len(nv) > 1 else 'N/A'
		us_gross.append(grosses)

# Building dataframe to be stored as a table
movies = pd.DataFrame({
	'movie': titles,
	'year': years,
	'rating': age_ratings,
	'timeMin': time,
	'genre': genres,
	'imdb': imdb_ratings,
	'metascore': metascores,
	'director': directors,
	'votes': votes,
	'us_grossMillions': us_gross,
	})

# cleaning the data
# cleaning year and converting to an int type
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)

# cleaning time and converting to an int type
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)

# cleans genre
movies['genre'] = movies['genre'].apply(lambda x: x.replace("\n", ""))
movies['genre'] = movies['genre'].apply(lambda x: x.rstrip())
#movies['genre'] = movies['genre'].str.split(",")


# cleaning metascore and converting to an int type
movies['metascore'] = movies['metascore'].str.extract('(\d+)')
movies['metascore'] = pd.to_numeric(movies['metascore'], errors='coerce')
movies.metascore = movies.metascore.fillna("None Given")

# cleaning votes and converting to an int type
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)

# cleaning gross and converting to a float type
# removing '$' and 'M' - cleaning
movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
# convert gross to a floating point number - converting
movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')
movies.us_grossMillions = movies.us_grossMillions.fillna("")

print(movies)

# copys table to a CSV file to be used in Excel
movies.to_csv('moviesDB.csv')
