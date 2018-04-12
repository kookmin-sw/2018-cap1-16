#!/bin/sh
chunk_size=24576
chunk="SS6Cqp3hVbl9HxvLhgAFlMlCcmpElsnevdxK1NpF"

curl -XPOST -H "Content-Type: application/json" "203.246.112.133:9200/seclab/_search?pretty" -d '
{
"query":
	{
		"bool":{
			"must":[
				{
					"term":{
						"SSDeep_chunk_size": "'$chunk_size'"
					}
				},	
				{
					"bool":{
						"should":[
							{
								"match": {
									"SSDeep_chunk":{
									"query" : "'$chunk'"
									}
								}
							}
						]
					}
				}			
			]
		}
	}
}'

