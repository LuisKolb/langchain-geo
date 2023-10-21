# langchain-geo

Using LangChain, GPT-3 (for now) and semantic linked data to enable a question answering API.

## setup

create, activate and install the venv

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

additionally, these components are required: [link to GitHub issue](https://github.com/chroma-core/chroma/issues/189#issuecomment-1454418844)

## deployment

ensure the Chroma Docker container is up and running, or langserve connection will fail

then, to run langserve locally just execute the `src/server.py` file 

langcorn documentation: [github.com/langchain-ai/langserve](https://github.com/langchain-ai/langserve) 

the frontend component using the langserve endpoints lives in this repository: [github.com/LuisKolb/langchain-geo-frontend](https://github.com/LuisKolb/langchain-geo-frontend) 