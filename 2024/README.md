# Build your own search engine

## Quick start
1. You need to have an ElasticSearch instance running at localhost:9200 (see https://www.elastic.co/downloads/elasticsearch) with authentication disabled.

2. You need to install all the dependencies in requirements.txt.

You can create a virtual environment and install the dependencies inside the project folder as follow:
```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

3. Run

```
python3 readpandas.py output
```

4. Run

```
sh create-or-update-pandas.sh
```
to customize ElasticSearch analyzers for the index.

5. Run

```
python3 indexpandas.py output
``` 

Note: pandas folder is downloaded from https://pandas.pydata.org/docs/pandas.zip
