import csv
from datetime import datetime
from flask import Flask,render_template,request
import math

class MovieWatchingSimulation:
    def __init__(self, users,playing_movie,reviews,ratings):
        self.__users = users
        self.__playing_movie = playing_movie
        self.__reviews = reviews
        self.__ratings = ratings

    def simulate(self):
        for i in range(0,len(self.__users)):
            self.__users[i].watch_movie(self.__playing_movie)
            self.__users[i].add_review(Review(self.__playing_movie,self.__reviews[i],self.__ratings[i]))





class WatchList:
    def __init__(self, movies):
        self.__movies = movies

    @property
    def movies(self):
        return self.__movies

    @movies.setter
    def director(self, value):
        self.__movies = []
        for movie in value:
            if isinstance(movie, Movie):
                self.__movies.append(movie)

class User:
    def __init__(self, name, password):
        if name != "" and type(name) == str:
            self.__user_name = name.strip().lower()

        if password != "" and type(password) == str:
            self.__Password = password.strip()

        self.__watched_movies = []
        self.__reviews = []
        self.__watch_list=[]
        self.__time_spent_watching_movies_minutes = 0

    def __repr__(self):
        return "<User " + self.__user_name + ">"

    def __eq__(self, other):
        return self.__user_name == other.user_name

    def __lt__(self, other):
        return self.__user_name < other.user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie):
        self.__watched_movies.append(movie)
        self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        self.__reviews.append(review)

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def watch_list(self):
        return self.__watch_list

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    @property
    def user_name(self):
        return self.__user_name

class Review:
    def __init__(self, movie, text, rating):
        self.__movie = movie
        self.__review_text = text.strip()
        if 1 <= rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None
        self.__timestamp = datetime.today()

    def __repr__(self):
        return"<Movie " + self.__movie.title + "," + str(self.__timestamp) + '>'

    def __eq__(self, other):
        return (self.__movie == other.movie) and (self.__review_text == other.review_text) and (self.__rating == other.rating) and (self.__timestamp == other.timestamp)

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp


class MovieFileCSVReader:
    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_movies = [Movie("zzzzzzzz", 1900)]
        self.__dataset_of_actors = [Actor("aaaaaaaa")]
        self.__dataset_of_directors = [Director("llllll")]
        self.__dataset_of_genres = [Genre("kkkkkk")]

    def read_csv_file(self):
        csvFile = open(self.__filename, mode="r", encoding="utf-8-sig")
        reader = csv.DictReader(csvFile)
        for row in reader:
            title = row['Title'].strip()
            release_year = int(row['Year'].strip())
            actors = sorted(row['Actors'].strip().split(','))
            director = row['Director']
            genres = sorted(row['Genre'].strip().split(','))
            description = row['Description'].strip()
            runtime = int(row['Runtime (Minutes)'].strip())
            movie = Movie(title, release_year)
            movie.description = description
            movie.runtime_minutes = runtime
            movie.description = description
            movie.director = director
            for a in actors:
                movie.add_actor(a)
            for g in genres:
                movie.add_genre(g)

            new_director = Director(director)
            if new_director not in self.__dataset_of_directors:
                check_director = 0
                movie.director = new_director
                for index in range(len(self.__dataset_of_directors)):
                    if new_director < self.__dataset_of_directors[index]:
                        self.__dataset_of_directors.insert(index, new_director)
                        check_director += 1
                        break
                if check_director == 0:
                    self.__dataset_of_directors.append(new_director)
            for d in self.__dataset_of_directors:
                if d == Director("llllll"):
                    index = self.__dataset_of_directors.index(d)
                    self.__dataset_of_directors.pop(index)

            for i in actors:
                new_actor = Actor(i)
                if new_actor not in self.__dataset_of_actors:
                    movie.actors.append(new_actor)
                    check_actor = 0
                    for index in range(len(self.__dataset_of_actors)):
                        if new_actor < self.__dataset_of_actors[index]:
                            self.__dataset_of_actors.insert(index, new_actor)
                            check_actor += 1
                            break
                    if check_actor == 0:
                        self.__dataset_of_actors.append(new_actor)
            for a in self.__dataset_of_actors:
                if a == Actor("aaaaaaaa"):
                    index = self.__dataset_of_actors.index(a)
                    self.__dataset_of_actors.pop(index)

            for i in genres:
                new_genre = Genre(i)
                if new_genre not in self.__dataset_of_genres:
                    movie.genres.append(new_genre)
                    check_genre = 0
                    for index in range(len(self.__dataset_of_genres)):
                        if new_genre < self.__dataset_of_genres[index]:
                            self.__dataset_of_genres.insert(index, new_genre)
                            check_genre += 1
                            break
                    if check_genre == 0:
                        self.__dataset_of_genres.append(new_genre)
            for g in self.__dataset_of_genres:
                if g == Genre("kkkkkk"):
                    index = self.__dataset_of_genres.index(g)
                    self.__dataset_of_genres.pop(index)

            check_movie = 0
            for index in range(len(self.__dataset_of_movies)):
                if movie < self.__dataset_of_movies[index]:
                    self.__dataset_of_movies.insert(index, movie)
                    check_movie += 1
                    break
            if check_movie == 0:
                self.__dataset_of_movies.append(movie)
            for m in self.__dataset_of_movies:
                if m == Movie("zzzzzzzz", 1900):
                    index = self.__dataset_of_movies.index(m)
                    self.__dataset_of_movies.pop(index)
        csvFile.close()
        #print(str(self.__dataset_of_movies))

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies


class Director:
    def __init__(self, name):
        if name == "" and type(name) != str:
            self.__name = None
        else:
            self.__name = name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__name

    def __repr__(self):
        return '<Director ' + str(self.__name) + '>'

    def __eq__(self, other):
        return self.__name == other.__name

    def __lt__(self, other):
        return self.__name < other.__name

    def __hash__(self):
        return hash(self.__name)


class Genre:
    def __init__(self, movie_genre):
        if movie_genre == "" and type(movie_genre) != str:
            self.__genrename = None
        else:
            self.__genrename = movie_genre.strip()

    @property
    def genre_name(self) -> str:
        return self.__genrename

    def __repr__(self):
        return '<Genre ' + str(self.__genrename) + '>'

    def __eq__(self, other):
        return self.__genrename == other.__genrename

    def __lt__(self, other):
        return self.__genrename < other.__genrename

    def __hash__(self):
        return hash(self.__genrename)


class Actor:

    def __init__(self, name):
        self.__colleaguelist = []
        if name == '' or type(name) != str:
            self.__actorname = None
        else:
            self.__actorname = name.strip()

    def __repr__(self):
        return '<Actor ' + str(self.__actorname) + '>'

    @property
    def actor_full_name(self) -> str:
        return self.__actorname

    def __eq__(self, other):
        return self.__actorname == other.__actorname

    def __lt__(self, other):
        return self.__actorname < other.__actorname

    def __hash__(self):
        return hash(self.__actorname)

    def add_actor_colleague(self, other):
        if isinstance(other, Actor):
            self.__colleaguelist.append(other)

    def check_if_this_actor_worked_with(self, other_actor):
        if isinstance(other_actor, Actor):
            if other_actor in self.__colleaguelist:
                return True
            else:
                return False

class Movie:
    def __init__(self, name, year1):
        if type(name) == str and name != '':
            self.__title = name.strip()
        else:
            self.__title = None

        if type(year1) == int and year1 >= 1900:
            self.__year = year1
        else:
            self.__year = None

        self.__description = ""
        self.__director = None
        self.__actors = []

        self.__genres = []
        self.__runtime_minutes = None

    def __repr__(self):
        return '<Movie ' + self.__title + ', ' + str(self.__year) + '>'

    def __eq__(self, other):
        return self.__title == other.__title and self.__year == other.__year

    def __lt__(self, other):
        if self.__title == other.__title:
            return self.__year < other.__year
        else:
            return self.__title < other.__title

    def __hash__(self):
        return hash((self.__title, self.__year))

    @property
    def runtime_minutes(self):
        return self.__runtime_minutes

    @property
    def title(self):
        return self.__title

    @property
    def year(self):
        return self.__year

    @property
    def description(self):
        return self.__description

    @property
    def director(self):
        return self.__director

    @property
    def actors(self):
        return self.__actors

    @property
    def genres(self):
        return self.__genres

    @description.setter
    def description(self, value):
        if type(value) == str and value != '':
            self.__description = value.strip()

    @director.setter
    def director(self, value):
        if isinstance(value, Director):
            self.__director = value

    @runtime_minutes.setter
    def runtime_minutes(self, value):
        if type(value) == int and value > 0:
            self.__runtime_minutes = value
        else:
            raise ValueError

    def add_actor(self, actor):
        if isinstance(actor, Actor):
            if actor not in self.__actors:
                self.__actors.append(actor)

    def remove_actor(self, actor):
        if isinstance(actor, Actor):
            if actor in self.__actors:
                index = self.__actors.index(actor)
                del self.__actors[index]

    def add_genre(self, g):
        if isinstance(g, Genre):
            if g not in self.__genres:
                self.__genres.append(g)

    def remove_genre(self, g1):
        if isinstance(g1, Genre):
            if g1 in self.__genres:
                index = self.__genres.index(g1)
                del self.__genres[index]


def getAllMovie():
    filename = 'datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()
    return movie_file_reader.dataset_of_movies
    #print(str(movieList[0].actors))
    #print(str(movie_file_reader))


app = Flask(__name__)
@app.route('/')
def index():
    numsInPage = 5;
    movieList = []
    param_dict = {}
    page = int(request.args.get("pagenum",1))
    searchKey = request.args.get("search",'')
    for m in getAllMovie():
        thisTitle = str(m.title)
        thisYear = str(m.year)
        thisDescription = str(m.description)
        #thisRuntime = str(m.runtime_minutes)
        if searchKey in thisTitle or searchKey == thisYear or searchKey in thisDescription:
            movieList.append(m)
    param_dict['page'] = page
    param_dict['searchKey'] = searchKey
    param_dict['pageAll'] = math.ceil(len(movieList)/numsInPage)
    param_dict['movie'] = ''
    movieBegin = (page-1)*numsInPage
    movieEnd = page*numsInPage
    if movieBegin > len(movieList)-1:
        movieBegin = len(movieList)-numsInPage
        movieEnd = len(movieList)
    elif movieEnd > len(movieList)-1:
        movieEnd = len(movieList)
    for m in range(movieBegin,movieEnd):
        thisTitle = str(movieList[m].title)
        thisYear = str(movieList[m].year)
        thisDescription = str(movieList[m].description)
        thisRuntime = str(movieList[m].runtime_minutes)
        thisText = thisTitle+';;'+thisYear+';;'+thisRuntime+';;'+thisDescription+';;;'
        param_dict['movie'] = param_dict['movie']+thisText
    return render_template('index.html', param_dict=param_dict)

@app.route('/search/')
def search():
    numsInPage = 5;
    movieList = []
    param_dict = {}
    page = int(request.args.get("pagenum",1))
    searchKey = request.args.get("search",'')
    for m in getAllMovie():
        thisTitle = str(m.title)
        thisYear = str(m.year)
        thisDescription = str(m.description)
        #thisRuntime = str(m.runtime_minutes)
        if searchKey in thisTitle or searchKey in thisYear or searchKey in thisDescription:
            movieList.append(m)
    param_dict['page'] = page
    param_dict['searchKey'] = searchKey
    param_dict['pageAll'] = math.ceil(len(movieList)/numsInPage)
    param_dict['movie'] = ''
    movieBegin = (page-1)*numsInPage
    movieEnd = page*numsInPage
    if movieBegin > len(movieList)-1:
        movieBegin = len(movieList)-numsInPage
        movieEnd = len(movieList)
    elif movieEnd > len(movieList)-1:
        movieEnd = len(movieList)
    for m in range(movieBegin,movieEnd):
        thisTitle = str(movieList[m].title)
        thisYear = str(movieList[m].year)
        thisDescription = str(movieList[m].description)
        thisRuntime = str(movieList[m].runtime_minutes)
        thisText = thisTitle+';;'+thisYear+';;'+thisRuntime+';;'+thisDescription+';;;'
        param_dict['movie'] = param_dict['movie']+thisText
    return render_template('index.html', param_dict=param_dict)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')