import json
import falcon
from dao.db_connection import DAO
from dao.queries import Queries
from models.movie_models import Movies


class GetData:
    def __init__(self):
        self.dao = DAO()
        self.filter_query = ''
        self.q = Queries()
        self.group_by_query = ' group by mm.movie_id order by mm.movie_id desc'
        self.genre_dict = {}

    def on_get(self, req, res):
        try:
            self.filter_query = ''
            self.prepare_filter(req.params)
            query = self.q.get_all_data.format(self.filter_query, self.group_by_query)
            data = self.dao.execute_query(query)
            parsed_data = self.parse_data(data)
            res.body = json.dumps(parsed_data)
            res.status = falcon.HTTP_200
        except Exception as e:
            res.body = json.dumps("Exception in getting movie details \n " + str(e))
            res.status = falcon.HTTP_422

    def parse_data(self, data):
        data_dict = {}
        try:
            temp_list = []
            for row in data:
                genre_dict, actor_dict = {}, {}
                genres, actor = [], []
                genre_id, actor_id =[], []
                if row[7]:
                    genres = row[7].split(',')
                    if row[9]:
                        genre_id = row[9].split(',')
                for i in range(len(genres)):
                    genre_dict[genre_id[i]] = genres[i]
                if row[8]:
                    actor = row[8].split(',')
                    if row[10]:
                        actor_id = row[10].split(',')
                for i in range(len(actor)):
                    actor_dict[actor_id[i]] = actor[i]
                a = Movies(row[0], row[1], row[2], str(row[3]), str(row[4]), row[5], str(row[6]),
                           genre_dict, actor_dict)
                temp_list.append(a.__dict__)
            data_dict["total"] = len(data)
            data_dict["data"] = temp_list
        except Exception as e:
            raise e
        return data_dict

    def prepare_filter(self, params):
        if 'name' in params:
            self.filter_query += "and mm.name regexp '{0}'".format(params['name'])
        if 'actor' in params:
            self.filter_query += "and ma.actor_name regexp '{0}'".format(params['actor'])
        if 'genre' in params:
            genre_list = params['genre']
            self.filter_query += "and mg.genre_id in ({0})".format(genre_list).replace('[','(').replace(']',')')
        if 'director' in params:
            self.filter_query += "and mm.director regexp '{0}'".format(params['director'])
        if 'startDate' in params:
            self.filter_query += "and mm.date_of_release >= str_to_date('{0}','%Y-%m-%d')".format(params['startDate'])
        if 'endDate' in params:
            self.filter_query += "and mm.date_of_release <= str_to_date('{0}','%Y-%m-%d')".format(params['endDate'])
        return
