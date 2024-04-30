#!/bin/bash

# Check operating system
if [[ "$OSTYPE" == "darwin"* ]]; then
  # For macOS
  OPEN=open
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  # For Linux
  OPEN=xdg-open
elif [[ "$OSTYPE" == "msys"* ]]; then
  # For Windows using Git Bash
  OPEN=start
else
  echo "Unsupported operating system."
  OPEN=xdg-open
fi

if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
fi

source env/bin/activate

pip install -r API/requirements.txt

cd API
python3 api.py &
backend_PID=$!

cd ../vue-project
npm i
npm run dev &
frontend_PID=$!

sleep 10 # Wait for the server to start
$OPEN http://localhost:5173

read -n 1 -s -r -p "Press any key to kill backend and frontend processes"

kill $backend_PID
kill $frontend_PID