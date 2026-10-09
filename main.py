from fastapi import FastAPI
import router.auth
import router.movies
import router.theatres
import router.shows
import router.bookings

app = FastAPI()

app.include_router(router.auth.auth)
app.include_router(router.movies.movies)
app.include_router(router.theatres.theatres)
app.include_router(router.shows.shows)
app.include_router(router.bookings.bookings)