#!/bin/sh
chunk_size=24576
chunk="SS6Cqp3hVbl9HxvLhgAFlMlCcmpElsnevdxK1NpF"
ip="203.246.112.137"
port="9200"

curl -XPOST -H "Content-Type: application/json" "'$ip':'$port'/seclab/_search?pretty" -d '
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

