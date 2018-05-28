curl -XPOST -H "Content-Type: application/json" 'http://203.246.112.133:9200/test/_search?pretty' -d '
{
	"query":{
		"term": {
			"_id" : "7e02fc505b9b3f3d52cca5c350817278"
		}
	}
}'
