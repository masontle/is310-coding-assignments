favorite_movies = [
    {"title": "The Lion King", "year": 1994},
    {"title": "The Matrix", "year": 1999},
    {"title": "Finding Nemo", "year": 2003},
    {"title": "The Dark Knight", "year": 2008},
    {"title": "Spider-Man: Into the Spider-Verse", "year": 2018},
]


def check_movie(movie):
    if movie["year"] < 2000:
        print("This movie was released before 2000")
    else:
        print("This movie was released after 2000")
        return movie["title"]


recent_movies = []

for movie in favorite_movies:
    recent_movie = check_movie(movie)
    if recent_movie is not None:
        recent_movies.append(recent_movie)

print(recent_movies)
