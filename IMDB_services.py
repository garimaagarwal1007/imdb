from wsgiref import simple_server
import falcon
from service_bll.add_data import AddMasterGenre, AddMasterActor
from service_bll.get_data import GetData
from service_bll.insert_data import Data
from service_bll.middleware import MiddlewareFacade


def get_app():
    api = falcon.API(middleware=MiddlewareFacade())
    api.add_route('/getData', GetData())
    api.add_route('/insertData', Data(update=True))
    api.add_route('/deleteMovie', Data())
    api.add_route('/addGenre', AddMasterGenre())
    api.add_route('/addActors', AddMasterActor())
    print("hi")
    return api


if __name__ == "__main__":
    httpd = simple_server.make_server('localhost', 8011, get_app())
    httpd.serve_forever()