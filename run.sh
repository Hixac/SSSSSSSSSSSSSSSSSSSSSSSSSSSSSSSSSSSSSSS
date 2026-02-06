#!/bin/bash

if [ "$1" == "-t" ]; then
    uv run pytest -s
    if [ $? -ne 0 ]; then
        echo "TESTING FAILED"
        exit 0
    fi
    echo "SUCCESSFULLY TESTED!"
    exit 0
fi

echo "STARTING SERVER"
uv run uvicorn src.server.main:app --reload --port 8443
