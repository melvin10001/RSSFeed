#!/home/mtrojanowski/Projects/RssFeed/bin/python3

import sqlite3
import smtplib
from email.mime.text import MIMEText
import feedparser
from os import getenv

LOGIN = getenv('LOGIN')
PASSWORD = getenv('PASSWORD')
SERVER = getenv('SERVER')
TARGET = getenv('TARGET')


def article_is_not_in_db(article_title, article_date):
    """ Check if a given pair of article title and date
    is in the database.
    Args:
        article_title (str): The title of an article
        article_date (str): The publication date of an article
    Return:
        True if the article is not in the database
        False if the article is alread present in the database
    """
    db.execute("select * from magazine where title=? and date=?",
            (article_title, article_date))
    if not db.fetchall():
        return True
    else:
        return False

def add_article_to_db(article_title, article_date):
    """ Add an new article title and date to the database
    Args:
        article_title (str): The title of an article
        article_date (str): The publication date of an article
    """
    db.execute("insert into magazine values (?,?)",
            (article_title, article_date))
    db_connection.commit()

def send_notification(article_title, article_url):
    """ Add a new article title and date to the database

    Args:
        article_title (str): The title of an article
        article_url (str): The url to access the article
    
    """

    smtp_server = smtplib.SMTP(SERVER, 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(LOGIN,PASSWORD)
    msg = MIMEText(f'\nHi there is a new Fedora Magazine article: \n\
            {article_title}. \n You can read it here: {article_url}')
    msg['Subject'] = 'New Fedora Magazine Article Available'
    msg['From'] = LOGIN
    msg['To'] = TARGET
    smtp_server.send_message(msg)
    smtp_server.quit()

def read_article_feed():
    """ Get articles from RSS feed"""
    feed = feedparser.parse('https://fedoramagazine.org/feed')
    for article in feed['entries']:
        title = article['title']
        published = article['published']
        link = article['link']

        if article_is_not_in_db(title, published):
            send_notification(title, link)
            add_article_to_db(title, published)


def main():
       
    global db_connection
    db_connection = sqlite3.connect('/home/mtrojanowski/Projects/RssFeed/magazine_rss.db')
    global db
    db = db_connection.cursor()
    db.execute('create table if not exists magazine (title TEXT, date TEXT)')
    read_article_feed()
    db_connection.close()

if __name__ == '__main__':
    main()


