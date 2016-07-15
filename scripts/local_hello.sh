#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
curl -X POST -H 'Content-Type: application/json' -d "@$DIR/hello.json" http://localhost:5000/webhook
