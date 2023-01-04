# Build your own search engine

## Quick start
1. You need to have an ElasticSearch instance running at localhost:9200 (see https://www.elastic.co/downloads/elasticsearch)

2. You need to install all the dependencies in requirements.txt.

You can create a virtual environment and install the dependencies inside the project folder as follow:
```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

3. Run

```
python3 phase1.py
```

4. Run

```
sh index-template.sh
```
to customize ElasticSearch analyzers for the index.

5. Run

```
python3 phase2.py
``` 

You can experiment with querying the index by opening query-fe.html in your web browser (you need to adjust CORS configurations in ElasticSearch for this to work as below).

```
...
http.cors.enabled : true
http.cors.allow-origin : "*"
http.cors.allow-methods : GET, POST
http.cors.allow-headers : Authorization,X-Requested-With,X-Auth-Token,Content-Type, Content-Length
```

Note: pandas folder is downloaded from https://pandas.pydata.org/docs/pandas.zip
