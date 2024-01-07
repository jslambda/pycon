curl -X PUT "localhost:9200/_index_template/template_pandas?pretty" -H 'Content-Type: application/json' -d'
{
  "index_patterns": ["panda*"],
  "template": {
    "mappings": {
      "properties": {
        "before": {
          "type": "text",
          "analyzer":"english"
        },
        "functions": {
          "type": "text",
          "analyzer": "english"
        },
        "after": {
          "type": "text",
          "analyzer": "english"
        },
        "prev_after": {
          "type": "text",
          "analyzer": "english"
        },
        "block": {
          "type": "text",
          "analyzer": "standard"
        },
        "chapter": {
          "type": "text",
          "analyzer": "english",
          "fields": {
            "keyword": {"type": "keyword"}
          }
        },
        "embed_vector": {
                  "type": "dense_vector",
                  "dims": 384,
                  "index": true,
                  "similarity": "cosine"
        },
        "permalink": {"type": "keyword"}
      }
    }
  },
  "priority": 500, 
  "version": 3,
  "_meta": {
    "description": "analyzers for Pandas metadata"
  }
}
'
