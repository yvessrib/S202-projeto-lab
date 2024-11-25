from neo4j import GraphDatabase

class MovieRecommendationDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Create a new user
    def create_user(self, user_id, name, favorite_genres=None):
        favorite_genres = favorite_genres or []
        with self.driver.session() as session:
            session.run(
                "CREATE (u:User {id: $user_id, name: $name, favorite_genres: $favorite_genres})",
                user_id=user_id, name=name, favorite_genres=favorite_genres
            )

    # Create a new movie
    def create_movie(self, movie_id, title, genre, year):
        with self.driver.session() as session:
            session.run(
                "CREATE (m:Movie {id: $movie_id, title: $title, genre: $genre, year: $year})",
                movie_id=movie_id, title=title, genre=genre, year=year
            )

    # Add a friend relationship between two users
    def add_friend(self, user_id_1, user_id_2):
        with self.driver.session() as session:
            session.run(
                "MATCH (u1:User {id: $user_id_1}), (u2:User {id: $user_id_2}) "
                "CREATE (u1)-[:FRIEND_OF]->(u2), (u2)-[:FRIEND_OF]->(u1)",
                user_id_1=user_id_1, user_id_2=user_id_2
            )

    # Mark a movie as watched
    def watch_movie(self, user_id, movie_id, liked):
        with self.driver.session() as session:
            session.run(
                "MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id}) "
                "CREATE (u)-[:WATCHED {liked: $liked}]->(m)",
                user_id=user_id, movie_id=movie_id, liked=liked
            )

    # Get movie recommendations for a user based on friends
    def get_recommendations(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})
                MATCH (u)-[:FRIEND_OF]->(friend)-[:WATCHED {liked: true}]->(m:Movie)
                WHERE NOT (u)-[:WATCHED]->(m) 
                  AND m.genre IN u.favorite_genres
                RETURN DISTINCT m.title AS title, m.genre AS genre, m.year AS year
                LIMIT 5
                """,
                user_id=user_id
            )
            return [{"title": record["title"], "genre": record["genre"], "year": record["year"]} for record in result]

    # Retrieve all users
    def get_all_users(self):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User) RETURN u.id AS id, u.name AS name, u.favorite_genres AS genres")
            return [{"id": record["id"], "name": record["name"], "genres": record["genres"]} for record in result]

    # Retrieve all movies
    def get_all_movies(self):
        with self.driver.session() as session:
            result = session.run("MATCH (m:Movie) RETURN m.id AS id, m.title AS title, m.genre AS genre, m.year AS year")
            return [{"id": record["id"], "title": record["title"], "genre": record["genre"], "year": record["year"]} for record in result]

    # Get friends of a user
    def get_friends(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User {id: $user_id})-[:FRIEND_OF]->(friend) RETURN friend.id AS id, friend.name AS name",
                user_id=user_id
            )
            return [{"id": record["id"], "name": record["name"]} for record in result]

    # Get movies watched by a user
    def get_movies_watched(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User {id: $user_id})-[:WATCHED]->(m:Movie) RETURN m.title AS title, m.genre AS genre, m.year AS year",
                user_id=user_id
            )
            return [{"title": record["title"], "genre": record["genre"], "year": record["year"]} for record in result]
