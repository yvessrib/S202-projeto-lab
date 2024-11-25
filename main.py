from database import MovieRecommendationDatabase


class MovieCLI:
    def __init__(self, movie_db):
        self.movie_db = movie_db

    def menu(self):
        print("\n-- Movie Recommendation CLI --")
        print("1. Create User")
        print("2. Create Movie")
        print("3. Add Friend")
        print("4. Watch Movie")
        print("5. Get Recommendations")
        print("6. View All Users")
        print("7. View All Movies")
        print("8. Exit")

    def run(self):
        while True:
            self.menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                user_id = input("Enter user ID: ")
                name = input("Enter user name: ")
                favorite_genres = input("Enter favorite genres (comma-separated): ").split(",")
                self.movie_db.create_user(user_id, name, [genre.strip() for genre in favorite_genres])
                print(f"User '{name}' created successfully.")

            elif choice == "2":
                movie_id = input("Enter movie ID: ")
                title = input("Enter movie title: ")
                genre = input("Enter movie genre: ")
                year = int(input("Enter movie release year: "))
                self.movie_db.create_movie(movie_id, title, genre, year)
                print(f"Movie '{title}' created successfully.")

            elif choice == "3":
                user_id_1 = input("Enter first user ID: ")
                user_id_2 = input("Enter second user ID: ")
                self.movie_db.add_friend(user_id_1, user_id_2)
                print(f"Friendship created between users '{user_id_1}' and '{user_id_2}'.")

            elif choice == "4":
                user_id = input("Enter user ID: ")
                movie_id = input("Enter movie ID: ")
                liked = input("Did the user like the movie? (yes/no): ").lower() == "yes"
                self.movie_db.watch_movie(user_id, movie_id, liked)
                print(f"User '{user_id}' watched movie '{movie_id}'.")

            elif choice == "5":
                user_id = input("Enter user ID: ")
                recommendations = self.movie_db.get_recommendations(user_id)
                print(f"\nRecommendations for User '{user_id}':")
                for movie in recommendations:
                    print(f" - {movie['title']} ({movie['genre']}, {movie['year']})")

            elif choice == "6":
                users = self.movie_db.get_all_users()
                print("\nAll Users:")
                for user in users:
                    print(f" - ID: {user['id']}, Name: {user['name']}, Favorite Genres: {', '.join(user['genres'])}")

            elif choice == "7":
                movies = self.movie_db.get_all_movies()
                print("\nAll Movies:")
                for movie in movies:
                    print(
                        f" - ID: {movie['id']}, Title: {movie['title']}, Genre: {movie['genre']}, Year: {movie['year']}")

            elif choice == "8":
                print("Exiting CLI.")
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    uri = "bolt://44.203.64.16"  # Substitua pelo URI do seu Neo4j
    user = "neo4j"  # Substitua pelo nome de usuário do Neo4j
    password = "pressure-lee-photos"  # Substitua pela senha do Neo4j

    # Instancia o banco de dados
    movie_db = MovieRecommendationDatabase(uri, user, password)

    # Inicia a CLI
    cli = MovieCLI(movie_db)
    try:
        cli.run()
    finally:
        movie_db.close()
