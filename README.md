# Qournal
CLI structured journal. 

## Idea
The user defines areas with journal items. There are three types of areas: Free Text, Structured Data, and Checklist. Each item contains a question that is asked when recording. Each day the user records answers for all defined areas. The user can then display recorded days in each area.

## Interface
Command names can be edited in the code.
Type "help" to list available commands with descriptions. 
The change area subprogram gives instructions on how to enter items.

    listas ; args:  <> ; lists available areas
    adda ; args:  <name> <type> ; adds area and runs the change area subprogram
    rema ; args:  <name> ; removes specified area
    changea ; args:  <name> ; runs the change area subprogram
    dispa ; args:  <name> ; displays specified area
    addall ; args:  <date> ; runs the add day subprogram for all areas
    commit ; args:  <path> ; commits data to json
    recover ; args:  <path> ; recovers data from json

## Running Qournal
Make sure you have Python 3.8+, pip and git installed.
Run these commands.
```console
git clone https://github.com/JanProvaznik/Qournal.git
cd Qournal/
pip install -r requirements.txt
python -m main.py
```
