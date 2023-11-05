# Data Directory

## How to download the required files to embed RDF data

This directory should contain `.rdf` files containing the geological data that should be embedded and used by the ConvQA chain as context.

These are the file names:

```
GeologicTimeScale.rdf 
GeologicUnit.rdf 
lithology.rdf 
mineral.rdf 
minres.rdf 
structure.rdf 
tectonicunit.rdf
```

They can be dowloaded individually from here: [https://thesaurus.geolba.ac.at/](https://thesaurus.geolba.ac.at/)

Or using these commands (requires bash):

```bash
cd src/data/rdf
bash download_data.sh
```

