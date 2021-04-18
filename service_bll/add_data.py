import json
import falcon
from models.movie_models import ActorMaster, GenreMaster
from dao.imdb_dao import DAO
from dao.imdb_dao import ModelOps
from dao.queries import Queries


class AddMasterActor:
    def __init__(self):
        self.im = ModelOps()
        self.q = Queries()
        self.dao = DAO()

    def on_post(self, req, res):
        try:
            if req.context == 'admin':
                data = json.dumps(req.media)
                data = json.loads(data)
                list_to_add = []
                for d in data:
                    temp_list = ActorMaster(d['id'], d['name'])
                    list_to_add.append(temp_list)
                self.im.bulk_insert(list_to_add)
        except Exception as e:
            res.body = json.dumps("Exception in adding Actor Master \n " + str(e))
            res.status = falcon.HTTP_422


class AddMasterGenre:
    def __init__(self):
        self.im = ModelOps()
        self.q = Queries()
        self.dao = DAO()

    def on_post(self, req, res):
        try:
            if req.context == 'admin':
                data = json.dumps(req.media)
                data = json.loads(data)
                list_to_add = []
                for d in data:
                    temp_list = GenreMaster(data['id'], data['name'])
                    list_to_add.append(temp_list)
                self.im.bulk_insert(list_to_add)
        except Exception as e:
            res.body = json.dumps("Exception in adding Actor Master \n " + str(e))
            res.status = falcon.HTTP_422
