import datetime
import json
import falcon
from dao.imdb_dao import DAO
from dao.imdb_dao import ModelOps
from dao.queries import Queries
from models.movie_models import MovieMaster, MovieGenre, MovieActors, Movies


class Data:
    def __init__(self, update=None):
        self.im = ModelOps()
        self.q = Queries()
        self.dao = DAO()
        self.genre_dict = {}
        self.group_by_query = ' group by mm.movie_id order by mm.movie_id desc'
        self.update_query_add_on = ''
        self.all_data = {}
        self.actors_dict = {}

    def on_post(self, req, res):
        try:
            if req.context == 'admin':
                self.genre_dict = self.get_all_genre()
                # self.actors_dict = self.get_all_movie_actors()
                data = json.dumps(req.media)
                data = json.loads(data)
                for d in data:
                    if d['movie_id'] == 0:
                        self.insert_data(d)
                    else:
                        self.update_data(d)
                res.body = json.dumps('Movie Successfully Added/Updated')
                res.status = falcon.HTTP_200
            else:
                raise falcon.HTTPUnauthorized("You do not have admin rights.")
        except Exception as e:
            res.body = json.dumps("Exception in inserting movie details \n " + str(e))
            res.status = falcon.HTTP_422

    def on_delete(self, req, res):
        try:
            if req.context == 'admin':
                movie_id = req.params['movieId']
                query = self.q.delete_movie.format(movie_id)
                self.dao.execute_non_query(query)
                res.body = json.dumps("Deleted Successfully")
                res.status = falcon.HTTP_200
            else:
                raise falcon.HTTPUnauthorized("You do not have admin rights.")
        except Exception as e:
            res.body = json.dumps("Exception occurred while deleting the movie \n " + str(e))
            res.status = falcon.HTTP_422

    def insert_data(self, d):
        genre_list = []
        actor_list = []
        date_time = datetime.datetime.now()
        ml = MovieMaster(d['movie_id'], d['name'], d['description'], d['date'], d['imdb_score'], d['director'],
                         d['99popularity'])
        movie_id = self.im.insert_model(ml)
        for genre in d['genre']:
            g_list = MovieGenre(movie_id, self.genre_dict[genre.strip()])
            genre_list.append(g_list)
        self.im.bulk_insert(genre_list)
        self.add_actors(d['actor'], movie_id)

    def update_data(self, data):
        self.update_query_add_on = ''
        self.all_data = self.get_all_data()
        movie_id = data['movie_id']
        old_genres = set(self.all_data[movie_id][0]['genre'].copy())
        self.all_data[movie_id][0]['genre'] = ''
        old_dict = self.all_data[movie_id][0].items()
        new_dict = {}
        temp_list = Movies(data['movie_id'], data['name'], data['description'], data['date'],
                           str(round(data['imdb_score'], 2)),
                           data['director'], str(round(data['99popularity'], 2)), '', '')
        new_dict[movie_id] = temp_list.__dict__
        new_genres = set(k.strip() for k in data['genre'])
        old_set = set(old_dict)
        new_set = set(new_dict[movie_id].items())
        differences = dict(new_set - old_set)
        genre_to_add = new_genres - old_genres
        genre_to_delete = old_genres - new_genres
        self.update_genre(genre_to_add, genre_to_delete, movie_id)
        self.update_master(differences, movie_id)
        self.update_actors(movie_id, data['actor'])

    def get_all_data(self):
        query = self.q.get_all_data.format('', self.group_by_query)
        data = self.dao.execute_query(query)
        data_dict = {}
        try:
            for row in data:
                temp_list = []
                genres = []
                if row[7]:
                    genres = row[7].split(',')
                a = Movies(row[0], row[1], row[2], str(row[3]), str(round(row[4], 1)), row[5], str(round(row[6], 1)),
                           genres, '')
                temp_list.append(a.__dict__)
                data_dict[row[0]] = temp_list
            return data_dict
        except Exception as e:
            raise e

    def get_all_movie_actors(self):
        actor_dict = {}
        try:
            data = self.dao.execute_query(self.q.all_movie_actors)
            for row in data:
                temp_list = {'id': row[1], 'name': [row[2]]}
                if row[0] in actor_dict:
                    actor_dict[row[0]].append(temp_list)
                else:
                    actor_dict[row[0]] = [temp_list]
        except Exception as e:
            raise e
        finally:
            return actor_dict

    def update_genre(self, added, deleted, movie_id):
        try:
            added_list = []
            for new in added:
                mg = MovieGenre(movie_id, self.genre_dict[new.strip()])
                added_list.append(mg)
            self.im.bulk_insert(added_list)
            if len(deleted) > 0:
                new_set = set()
                for delete in deleted:
                    new_set.add(self.genre_dict[delete.strip()])
                query = self.q.delete_genre_of_movie.format(movie_id, new_set)
                query = query.replace('{', '(')
                query = query.replace('}', ')')
                self.dao.execute_non_query(query)
        except Exception as e:
            raise e

    def update_master(self, differences, movie_id):
        try:
            #creating dynamic update query
            if bool(differences):
                if 'movie_name' in differences:
                    self.update_query_add_on += ",name = '{0}'".format(differences['movie_name'])
                if 'description' in differences:
                    self.update_query_add_on += ",description = '{0}'".format(differences['description'])
                if 'imdb_score' in differences:
                    self.update_query_add_on += ",score = '{0}'".format(differences['imdb_score'])
                if 'director' in differences:
                    self.update_query_add_on += ",director = '{0}'".format(differences['director'])
                if 'popularity' in differences:
                    self.update_query_add_on += ",popularity = '{0}'".format(differences['popularity'])
                query = self.q.update_master.format(self.update_query_add_on, movie_id)
                self.dao.execute_query(query)
        except Exception as e:
            raise e

    def update_actors(self, movie_id, new_actor_list):
        try:
            #delete all existing actors
            self.dao.execute_non_query(self.q.delete_actors.format(movie_id))
            # old_actor = self.actors_dict[movie_id]
            # pairs = zip(new_actor_list, old_actor)
            #a = [(x, y) for x, y in pairs if x != y]
            # updating all the actors
            self.add_actors(new_actor_list, movie_id)
        except Exception as e:
            raise e

    def add_actors(self, actors, movie_id):
        try:
            actor_list = []
            for a in actors:
                if isinstance(a['name'], list):
                    for name in a['name']:
                        al = MovieActors(movie_id, a['id'], name)
                        actor_list.append(al)
                else:
                    al = MovieActors(movie_id, a['id'], a['name'])
                    actor_list.append(al)
            self.im.bulk_insert(actor_list)
        except Exception as e:
            raise e

    def get_all_genre(self):
        genre_dict = {}
        try:
            data = self.dao.execute_query(self.q.get_genre)
            for row in data:
                genre_dict[row[1]] = row[0]
        except Exception as e:
            raise e
        finally:
            return genre_dict
