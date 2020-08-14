import sqlalchemy as sa 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bottle import HTTPError


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class AlbumDublicationError(Exception):
	pass
	
class Album(Base):
	__tablename__ = 'album'
	id = sa.Column(sa.INTEGER, primary_key = True)
	year = sa.Column(sa.INTEGER)
	artist = sa.Column(sa.TEXT)
	genre = sa.Column(sa.TEXT)
	album = sa.Column(sa.TEXT)

def connect_db():
	engine = sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)
	return session()

def find(artist):
	session = connect_db()
	albums = session.query(Album).filter(Album.artist == artist).all()
	return albums

def add_album(album):
	session = connect_db()
	if session.query(Album).filter(Album.album == album.album).count() > 0:
		return False
	else:
		session.add(album)
		session.commit()
