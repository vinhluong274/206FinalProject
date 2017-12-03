from imdb import IMDb
import requests


ia = imdb.IMDb()
the_matrix = ia.get_movie('0133093')
print(the_matrix['director'])
