import Constants


class MovieMaster:
    def __init__(self, movie_id=None, name=None, description=None, date_of_release=None, score=None, director=None,
                 popularity=None):
        self.movie_id = movie_id
        self.name = name
        self.description = description
        self.date_of_release = date_of_release
        self.score = score
        self.director = director
        self.popularity = popularity

    def get_insert_identity_header(self):
        return Constants.movie_master_get_insert_identity_header

    def get_values(self):
        self.description = 'Movie' if self.description is None else self.description
        values = """("{0}", "{1}", "{2}", {3}, "{4}", "{5}")""".format(self.name, self.description,
                                                                       self.date_of_release, self.score,
                                                                       self.director, self.popularity)
        return values


class MovieGenre:
    def __init__(self, movie_id, name):
        self.movie_id = movie_id
        self.name = name

    def get_insert_header(self):
        return Constants.movie_genre_get_header

    def get_values(self):
        values = """({0}, {1})""".format(self.movie_id, self.name)
        return values


class MovieActors:
    def __init__(self, movie_id, type_id, name):
        self.movie_id = movie_id
        self.type_id = type_id
        self.name = name

    def get_insert_header(self):
        return Constants.actor_type_get_header

    def get_values(self):
        values = """({0}, {1}, "{2}")""".format(self.movie_id, self.type_id, self.name)
        return values


class Movies:
    def __init__(self, movie_id=None, movie_name=None, description=None, date_of_release=None, imdb_score=None,
                 director=None, popularity=None, genre=None,
                 actor=None):
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.description = description
        self.date = date_of_release
        self.score = imdb_score
        self.director = director
        self.popularity = popularity
        self.genre = genre
        self.actor = actor


class ActorMaster:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_insert_header(self):
        return Constants.actor_type

    def get_values(self):
        values = """({0}, "{1}")""".format(self.id, self.name)
        return values


class GenreMaster:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_insert_header(self):
        return Constants.genre_type

    def get_values(self):
        values = """({0}, "{1}")""".format(self.id, self.name)
        return values
