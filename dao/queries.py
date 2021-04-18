class Queries:
    get_all_data = """select mm.movie_id, mm.name, mm.description, mm.date_of_release,
                     mm.score, mm.director, mm.popularity,
                     ifnull(group_concat(distinct(gm.name)), '') as genres, 
                    ifnull(group_concat(distinct(ma.actor_name)), '') as actors, ifnull(group_concat(distinct mg.genre_id), '') as genre_id, ifnull(group_concat(distinct ma.actor_type_id),'') as actor_id from movies_master mm
                    left join movie_genre mg on mg.movie_id = mm.movie_id
                    left join movie_actors ma on ma.movie_id = mm.movie_id
                    left join genre_master gm on gm.genre_id = mg.genre_id
                    left join actor_master am on am.id = ma.actor_type_id
                    where 1=1 {0} {1}"""

    delete_movie = """delete from movies_master where movie_id = {0}"""

    update_master = """update movies_master set name=name {0} where movie_id = {1}"""

    delete_genre_of_movie = """delete from movie_genre where movie_id = {0} and genre_id in {1}"""

    all_movie_actors = """select movie_id,actor_type_id,actor_name from movie_actors"""

    delete_actors = """delete from movie_actors where movie_id = {0}"""

    get_genre = """select genre_id,name from genre_master"""

