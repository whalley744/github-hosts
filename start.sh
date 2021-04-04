#!/bin/bash

project_path=$(
  cd $(dirname "$0")
  pwd
)

export FLASK_APP=$project_path/main.py

nohup flask run --host=0.0.0.0 >hosts.log 2>&1 &
