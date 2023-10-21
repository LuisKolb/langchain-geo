import sys
from requests.exceptions import ConnectionError
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

logger = logging.getLogger(__name__)

try:
    from chains.convqa import chain
except ConnectionError:
    logger.error('[ERROR] Docker container is not running or not reachable! exiting...')
    sys.exit(1)

app = FastAPI(title="Chain API Endpoints")

# this is required, as the 'no-cors' mode in js fetch() causes the request to fail with 422 😢
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

add_routes(app, chain)

# run the server simply by executing this python file
#
# documentation: `https://github.com/langchain-ai/langserve` 

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001)