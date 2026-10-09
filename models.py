from sqlalchemy import Boolean,Integer,Column,String,Float, ForeignKey, Date, Time
from .database import Base

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer,primary_key = True)
    title = Column(String(50))
    duration = Column(Float)
    rating = Column(Float)

class Theatre(Base):
    __tablename__ = 'theatres'
    id = Column(Integer, primary_key = True)
    theatre_name = Column(String(50))
    total_seats = Column(Integer)

class TheatreMovie(Base):
    __tablename__ = "theatre_movies"
    id = Column(Integer, primary_key = True)
    theatre_id = Column(Integer, ForeignKey("theatres.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))

class Show(Base):
    __tablename__ = 'show_timing'
    id = Column(Integer, primary_key = True)
    theatre_id = Column(Integer, ForeignKey("theatres.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    show_date = Column(Date)
    show_time = Column(Time)

class Seats(Base):
    __tablename__ = 'seat'
    id = Column(Integer, primary_key = True)
    seat_number = Column(Integer)
    theatre_id = Column(Integer,ForeignKey("theatres.id"))

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key = True)
    show_id = Column(Integer, ForeignKey("show_timing.id"))
    seat_id = Column(Integer, ForeignKey("seat.id"))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    name = Column(String(100))
    email = Column(String(100), unique = True, index = True)
    password = Column(String(255))
    role = Column(String(15))