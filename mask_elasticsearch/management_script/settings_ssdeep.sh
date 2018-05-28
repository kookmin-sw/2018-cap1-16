ip="203.246.112.137"
port="9200"

curl -XPUT -H "Content-Type: application/json" "$ip:$port/ssdeep?pretty" -d '
{
	"settings": {
		"analysis" : {
			"analyzer":{
				"ssdeep_analyzer": {
					"tokenizer" : "ssdeep_ngram_tokenizer"
				}
			},
			"tokenizer":{
				"ssdeep_ngram_tokenizer": {
					"type" : "ngram",
					"min_gram" : "6",
					"max_gram" : "6"	
				}
			}
		}
	},
	"mappings" : {
		"analyzed_report" :{
			"properties":{
			    "md5" : {
			        "type" : "text",
			    },
				"chunk":{
					"type" : "text",
					"analyzer" : "ssdeep_analyzer"
				},
				"double_chunk":{
					"type" : "text",
					"analyzer" : "ssdeep_analyzer"
				},
				"chunk_size" :{
					"type" : "integer"
				},
				"ssdeep_hash" :{
					"type" : "text"
				}
			}
		}
	}
}'
