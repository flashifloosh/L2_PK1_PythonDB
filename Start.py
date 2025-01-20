from Core import Core
from database_util.Database import Database


def main():
    try:
        # Ensure the database is initialized
        Database.create_db()
        # Start the main application
        Core()
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
