import pandas as pd
import json

def get_tuples(db):
    """
    Gets "tuple" (movie_name, clusters) for a given database

    Parameters:
    -----------
    db : list

    Returns:
    --------
    name_clust : list
    """

    df = pd.DataFrame(db)

    #get names
    names = df.columns
    #get clusters
    aux = df[:1].values
    clusters = aux[0]

    name_clust = []
    for i in range(len(names)):
        name_clust.append((names[i], clusters[i]))

    return name_clust

def cluster_list(name_clust, cluster_number):
    """
    Returns list of movies in same cluster.

    Parameters:
    -----------
    name_clust : list
            (movie_name, cluster) list

    Returns:
    --------
    mv_clus : list
            list of movies in the same cluster
    """
    size = len(name_clust)

    mv_clus = []

    for i in range(size):
        for j in name_clust[i][1]:
            if j == cluster_number:
                mv_clus.append(name_clust[i][0])

    return mv_clus

def get_sinopses(mv_clus):
    """
    Returns sinopses as text of a given movies

    Parameters:
    -----------
    mv_clus : list
            list of movies

    Returns:
    --------
    sinopse : list
            sinopse (text)
    """

    movie_sinopse_list = []
    clustered_movies = mv_clus

    with open(os.path.join('', 'tmdb_5000_movies.json')) as file:
        movies_data = json.load(file)

        for movies in movies_data:
            for selected in clustered_movies:
                if movies['name'] == selected:
                    movie_sinopse_list.append((movies['name'], movies['overview']))

    sinopse = [x[1] for x in movie_sinopse_list]
    return sinopse
