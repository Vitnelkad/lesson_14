# type — фильм или сериал
# title — название
# director — режиссер
# cast — основные актеры
# country — страна производства
# date_added — когда добавлен на Нетфликс
# release_year — когда выпущен в прокат
# rating — возрастной рейтинг
# duration — длительность
# duration_type — минуты или сезоны
# listed_in — список жанров и подборок
# description — краткое описание

import collections
import sqlite3


class DbConnect:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()

def execute_query(query):
    with sqlite3.connect('netflix.db') as con:
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
    return result


def movie_by_title(title):
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, country, release_year, listed_in, description
        from netflix 
        where title like '%{title}%'
        order by release_year desc
        limit 1""")
    result = db_connect.cur.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4],
    }


def movies_by_years(year1, year2):
    db_connect = DbConnect('netflix.db')
    query = f"select title, release_year from netflix where release_year between {year1} and {year2} limit 100;"
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "release_year": movie[1]})
    return result_list

def movies_by_rating(rating):
    rating_parameters = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    if rating not in rating_parameters:
        return "Переданной группы не существует"
    query = f"select title, rating, description from netflix where rating in ({rating_parameters[rating]})"
    result = execute_query(query)
    result_list = []
    for movie in result:
        result_list.append({
            "title": movie[0],
            "rating": movie[1],
            "description": movie[2]
        })
    return result_list

def movies_by_genre(genre):
    result = execute_query(f""" select title, description
    from netflix
    where listed_in like '%{genre}%'
    order by  release_year desc
    limit 10;""")
    result_list = []
    for movie in result:
        result_list.append({
            "title": movie[0],
            "description": movie[1]
        })
        return result_list


def cast_parttners(actor1, actor2):
    query = f"select 'cast' from netflix where 'cast' like '%{actor1}%' and 'cast' like '%{actor2}%';"
    result = execute_query(query)
    actors_list = []
    for cast in result:
        actors_list.extend(cast[0].split(', '))
    counter = collections.Counter(actors_list)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count > 2:
            result_list.append(actor)
    return result_list

def search_movie_by_param(movie_type, release_year, genre):
    query = f"""select title, description
    from netflix
    where type = '{movie_type}' 
    and release_year = {release_year}
    and listed_in like '%{genre}%'"""
    result = execute_query(query)
    result_list = []
    for movie in result:
        result_list.append({'title': movie[0],
                           'description': movie[1]})
    return result_list

print(search_movie_by_param('TV Show', 2005, 'Drama'))
    