from dao.db_connection import DAO


class ModelOps:
    def __init__(self):
        self.__dao = DAO()
        self.__bulk_size = 1000
        return

    def insert_model(self, model):
        id = None
        query = model.get_insert_identity_header()
        query = query + model.get_values()
        queryList = [query, "SELECT LAST_INSERT_ID()"]
        for row in self.__dao.execute_query(queryList):
            id = row[0]
        return id

    def bulk_insert(self, models):
        models_inserted = 0
        if len(models) > 0:
            query = models[0].get_insert_header()
            model_count = 0
            executed = False
            for model in models:
                executed = False
                query = query + model.get_values() + ","
                model_count += 1
                if model_count == self.__bulk_size:
                    # [:-1] is to remove the last char ',' from query
                    models_inserted += self.__dao.execute_non_query(query[:-1])
                    query = models[0].get_insert_header()
                    model_count = 0
                    executed = True
            if not executed:
                models_inserted += self.__dao.execute_non_query(query[:-1])
        return models_inserted
