# token-document-feature size calculations

## all features

```
embedding 1085681 tokens would cost $0.1085681

average document len: 247.98560986751943
min document len: 31, meta: {'source': 'http://resource.geolba.ac.at/ref/1242'}
max document len: 10816, meta: {'source': 'http://resource.geolba.ac.at/tectonicunit/112'}
```

## downsizing 1

- remove `http://resource.geolba.ac.at/ref/*`

```
embedding 901514 tokens would cost $0.0901514

average document len: 294.13181076672106
min document len: 34, meta: {'source': 'http://resource.geolba.ac.at/minres/33'}
max document len: 10816, meta: {'source': 'http://resource.geolba.ac.at/tectonicunit/112'}
```

## downsizing 2

- remove dcterms:bibliographicCitation 
- remove dbpo:colourHexCode
- remove dcterms:references

```
embedding 811572 tokens would cost $0.0811572

average document len: 185.37505710370033
min document len: 27, meta: http://resource.geolba.ac.at/ref/919
max document len: 10804, meta: http://resource.geolba.ac.at/tectonicunit/112
```

## downsizing 1 && 2

- remove `http://resource.geolba.ac.at/ref/*`
- remove dcterms:bibliographicCitation 
- remove dbpo:colourHexCode
- remove dcterms:references

```
embedding 722925 tokens would cost $0.0722925

average document len: 235.86460032626428
min document len: 30, meta: http://resource.geolba.ac.at/GeologicUnit/3
max document len: 10804, meta: http://resource.geolba.ac.at/tectonicunit/112
```

## downsizing 1 && 2 && leave out map data

- remove `http://resource.geolba.ac.at/ref/*`
- remove dcterms:bibliographicCitation 
- remove dbpo:colourHexCode
- remove dcterms:references
- exclude data from the file `query-result-gk50.tsv`

```
embedding 514746 tokens would cost $0.0514746

average document len: 167.9432300163132
min document len: 30, meta: http://resource.geolba.ac.at/GeologicUnit/3
max document len: 1341, meta: http://resource.geolba.ac.at/GeologicUnit/247
```