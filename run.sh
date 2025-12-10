#!/bin/bash

if [ $1 == "-t" ]; then
    uv run pytest -s
    if [ $? -ne 0 ]; then
        echo "TESTING FAILED"
        exit 0
    fi
    echo "SUCCESSFULLY TESTED!"
    echo "STARTING SERVER"
fi


uv run uvicorn src.app.main:app --reload --port 8443 --ssl-certfile ../../Certs/myCA.pem --ssl-keyfile ../../Certs/myCA.key 
