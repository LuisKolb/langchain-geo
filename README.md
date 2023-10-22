# langchain-geo

Using LangChain, GPT-3 (for now) and semantic linked data to enable a question answering API.

## the whole package as a docker thingy

for a minimal setup, **in the same directory**:

1. download docker-compose.yaml
2. ensure the file `.env` exists and has a valid OpenAI API key as specified in `.env-example`
3. run this command: 

```bash
docker-compose up
```

on windows, docker volumes (like the ones created using docker-compose) are usually found at:

```
\\wsl.localhost\docker-desktop-data\version-pack-data\community\docker\volumes\<volume name>\_data
```

### running the stack manually

you can build your own image from this repo:

```bash
docker build . -t luiskolb/geo-agent:latest
```

to use it, you'll have to manually set up the chromadb/chroma image in addition. environment variables, volumes, ports will have to be provided manually, for example through the docker desktop interface seen in the image above, or using the following commands:

```bash
docker network create lc-geo-net
docker run --network lc-geo-net -p 8000 --env-file .env --name chromadb -v lc-geo_db-data:/chroma/chroma chromadb/chroma
docker run --network lc-geo-net -p 8001 --env-file .env --name agent luiskolb/geo-agent:latest
```

a custom network here is required for the containers to talk to each other. the endpoint will then both be available at a random port through docker. either click the port in docker desktop, or use this command to view the ports:

```bash
docker container ls --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}" -a
``` 

## local setup

create, activate and install the venv

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

additionally, these components are required: [link to GitHub issue](https://github.com/chroma-core/chroma/issues/189#issuecomment-1454418844)

create a `.env` file in the same directory as `.env-example` and fill in your key

### deployment

ensure the Chroma Docker container is up and running, or langserve connection will fail

then, to run langserve locally just execute the `src/server.py` file 

langserve documentation: [github.com/langchain-ai/langserve](https://github.com/langchain-ai/langserve) 

the frontend component using the langserve endpoints lives in this repository: [github.com/LuisKolb/langchain-geo-frontend](https://github.com/LuisKolb/langchain-geo-frontend) 

### chroma and the docker container - managing data

it's easiest to use docker desktop to set up the docker container running chroma. you can use the command above, or manually like this: 

pull the latest version of `chromadb/chroma` from dockerhub, and run it. below is an example configuration:
![docker desktop config example](media/docker-desktop-config.png) - add your environment variables here as well!

a custom network is not required when running the python files on the host, only when both services are running in separate containers.

binding a local folder (in this example `D:\lcgeo\chroma-data`) to the container path `/chroma/chroma` allows you to modify the `chroma.sqlite3` file easily from your own machine. this file is where the actual data is stored, and simply replacing it with your own `chroma.sqlite3` file allows you to transfer the database from one machine to another. you can also use volumes built into docker desktop.

you can also modify the port the container will be exposed on.

⚠️ be careful to use the same port number you specify here in the python chromaDB client, or the connection will fail (obviously).

⚠️ the collection_name string identifies the collection, and is saved to the `chroma.sqlite3` file. to access the collection later (after transferring the file to another machine) you need the same string.


