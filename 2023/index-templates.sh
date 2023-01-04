# to delete the index template run:
# curl -X DELETE "localhost:9200/_index_template/template_1"
curl -X PUT "localhost:9200/_index_template/template_1?pretty" -H 'Content-Type: application/json' -d'
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
        }
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
