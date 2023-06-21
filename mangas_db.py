from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from chapter_checker import MangaChapter
from send_mail import MailSender

Base = declarative_base()


class Manga(Base):
    __tablename__ = 'manga'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    current_chapter = Column(Integer)
    page_link = Column(String)
    chapter_link = Column(String)


def create_database():
    engine = create_engine('sqlite:///manga.db')
    Base.metadata.create_all(engine)
    return engine


def get_manga_details():
    name = input("Enter manga name: ")
    current_chapter = int(input("Enter current chapter number: "))
    page_link = input("Enter manga page link: ")
    return name, current_chapter, page_link


def add_manga(session, name, current_chapter, page_link, chapter_link=None):
    manga = Manga(name=name,
                  current_chapter=current_chapter,
                  page_link=page_link,
                  chapter_link=chapter_link)
    session.add(manga)
    session.commit()


def check_manga_updates(session):
    # Retrieve manga data from the database
    manga_list = session.query(Manga).all()

    # Check for updates and update the links and chapter numbers
    for manga in manga_list:
        manga_checker = MangaChapter(manga.page_link, manga.current_chapter,
                                     manga.name)
        if manga_checker.get_chapter_number():
            manga.chapter_link = manga_checker.current_chap_link
            manga.current_chapter = manga_checker.new_chapter_no
            session.commit()

            # Send email notification with chapter link
            message = f"Subject:{manga.name} New Chapter\n\n"
            message += f'Chapter ({manga.current_chapter}) of {manga.name} has been released!\n'
            message += f"Chapter Link: {manga.chapter_link}"

            sender = MailSender()
            sender.send_mail(message)
            print(f"Email Sent for {manga.name}")
