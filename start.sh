#!/bin/bash

echo "Starting Ollama..."

if ! pgrep -x ollama > /dev/null
then
    nohup ollama serve > ollama.log 2>&1 &
    sleep 10
fi


echo "Starting API..."

if ! pgrep -f "uvicorn app:app" > /dev/null
then
    nohup uvicorn app:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
fi


echo "READY"
