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

ensure the Chroma Docker container is up and running, or langcorn connection will fail

then, to run langcorn locally

```bash
cd src
uvicorn server:app --host 127.0.0.1 --port 8718
```

langcorn documentation: [github.com/msoedov/langcorn](https://github.com/msoedov/langcorn) 

the frontend component using the langcorn endpoints lives in this repository: [github.com/LuisKolb/langchain-geo-frontend](https://github.com/LuisKolb/langchain-geo-frontend) 