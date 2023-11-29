import sys
from requests.exceptions import ConnectionError
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

logger = logging.getLogger(__name__)

try:
    from chains.convqa import chain as convqa
    from chains.convqa import chain_stream as convqa_stream
except ConnectionError:
    logger.error('[ERROR] ChromaDB Docker container is not running or not reachable! exiting...')
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

add_routes(app, convqa, path="/convqa")
add_routes(app, convqa_stream, path="/convqa_stream")

# run the server simply by executing this python file
#
# documentation: `https://github.com/langchain-ai/langserve` 

if __name__ == "__main__":
    import uvicorn
    import os

    def is_docker():
        path = "/proc/self/cgroup"
        return (
            os.path.exists("/.dockerenv")
            or os.path.isfile(path)
            and any("docker" in line for line in open(path))
        )

    if is_docker():
        host = "0.0.0.0"
    else:
        host = "localhost"

    uvicorn.run(app, host=host, port=8001)