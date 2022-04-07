# polybar-vikunja

## cURL Commands:

`VIKUNJA_BASE_URL="https://vikunja.tld"`

### Login:
`VIKUNJA_TOKEN=$(curl -X POST  -H "Content-Type: application/json" $VIKUNJA_BASE_URL/api/v1/login -d '{"username": "xxxxx", "password": "xxxxx"}' | jq -r .token)`

### List Lists:
`curl -X GET -H "Authorization: Bearer $VIKUNJA_TOKEN" $VIKUNJA_BASE_URL/api/v1/lists | jq .`

### List List Contents:
`curl -X GET -H "Authorization: Bearer $VIKUNJA_TOKEN" $VIKUNJA_BASE_URL/api/v1/lists/12/tasks | jq .`

### List Not Done Tasks in List:
`curl -X GET -H "Authorization: Bearer $VIKUNJA_TOKEN" $VIKUNJA_BASE_URL/api/v1/lists/12/tasks\?filter_by\=done\&filter_value\=false\&filter_comparator\=equals | jq .`

### Mark Task as Done:
`curl -X POST -H "Authorization: Bearer $VIKUNJA_TOKEN" -H "Content-Type: application/json" $VIKUNJA_BASE_URL/api/v1/tasks/845 -d '{"done": true}' | jq .`
