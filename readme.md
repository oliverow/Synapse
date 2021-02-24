# Intro
This app called Synapse is a tool for helping with memorization by leveraging graph database and brain imagination.

I currently use it to memorize vocabulary for GRE exam.

How this app works is that you can enter entries that you want to memorize and review them in multiple modes. You need manually enter things that are hard to memorize but have reminiscent hints or multiple things that are mingled and confuses you. Then you can review the entered entries by relations or clusters.

# Requisites

## Graph Database

### Install neo4j
at https://neo4j.com/download/

### Start server
Once an empty database is created, you need to start a server on bolt://localhost:7687 (which is the default port). You also need to create a user with username "synapse" and password "1129" (hard coded) to access the database.

# Start the app

## From CLI
With the correct environment configured, run `python src/main.py` 

## From built app
run `pyinstaller --windowed --onefile --name Synapse src/main.py`

# Note
The app is very preliminary for now because I need to PREPARE FOR GRE. I'll try to make it to a commercialize-ready state in the future. 
