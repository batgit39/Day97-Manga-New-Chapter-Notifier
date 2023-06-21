from sqlalchemy.orm import sessionmaker
from mangas_db import create_database, get_manga_details, add_manga, check_manga_updates


def print_info():
    print("This program allows you to track manga chapters.")
    print("You can check for updates on existing mangas and add new mangas to track.")
    print("When a new chapter is released for a tracked manga,\nyou will receive an email notification.")
    print("NOTE: This currently only supports VIZ")


def main():
    engine = create_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\n1. Check existing mangas")
        print("2. Add a new manga")
        print("3. Info")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            check_manga_updates(session)
        elif choice == "2":
            name, current_chapter, page_link = get_manga_details()
            add_manga(session, name, current_chapter, page_link)
        elif choice == "3":
            print_info()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

    session.close()


if __name__ == '__main__':
    main()
