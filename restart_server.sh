#!/bin/bash

# Kill any existing server process
pkill -f 'python3 server.py'

# Navigate to the project directory
cd /home/dynamic/psyde-quest3

# Pull the latest changes from GitHub
git pull

# Restart the server in the background
nohup python3 server.py &
