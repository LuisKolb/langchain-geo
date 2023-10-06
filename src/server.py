from fastapi import FastAPI
from langcorn import create_service

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app:FastAPI = create_service('chains.example:chain',
                             'chains.convqa:chain',)

# this is required, as the 'no-cors' mode in js fetch() causes the request to fail with 422 😢
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# run this using this command from inside this dir:
# `uvicorn server:app --host 127.0.0.1 --port 8718`
#
# documentation: `https://github.com/msoedov/langcorn` 