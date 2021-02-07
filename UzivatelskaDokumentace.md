# Qournal uživatelská dokumentace
## Instalace
Máme nainstalovaný git a Python 3.8+ a pip.
Zadáme do příkazového prostředí.
````
git clone https://github.com/JanProvaznik/Qournal.git
cd Qournal
pip install -r requirements.txt
python main.py

````

## Funkce
Definujeme oblasti záznamu (area), ve kterých jsou položky (item). Ukládame po dnech, poté si záznamy můžeme vypsat.
## Ovládání
Aplikace se ovládá příkazy.

#### help
Vypíše příkazy a nápovědu

````
listas | args:  <> |  lists available areas
adda | args:  <name> <type> |  adds area and runs the change area subprogram types: 1-checklist, 2-structured data, 3-free text
rema | args:  <name> |  removes specified area
changea | args:  <name> |  runs the change area subprogram
dispa | args:  <name> |  displays specified area
addall | args:  <date> |  runs the add day subprogram for all areas
addspec | args:  <name> <date> |  runs the add day subprogram for specified area, date blank for today, in iso format or 'y' for yesterday
commit | args:  <path> |  commits data to json
recover | args:  <path> |  recovers data from json

````

### Příkazy v podprogramu změny
````
addi to add an item template
chai <name> to change an item template
exit to exit the change area subprogram
 ````
 
