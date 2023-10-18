# legendsofadventure

# Instalacja

Jesli jeszcze nie macie w global envie

    pip install poetry


Jezeli pullujecie maina i widzicie, ze ktos dodal nowe moduly:
    
    poetry install

### WAZNE! Robicie to w sciezce, gdzie jest pyproject.toml
#
Po tym jak zrobicie te kroki, to za kazdym razem przed developmentem:

    poetry shell

w sciezce, gdzie znajduje sie poetry.lock i pyproject.toml
#
Jak macie wybrany zly interpreter w VSCodzie, to klikacie na niego w prawym dolnym rogu i wybieracie z listy:


![interpreter](/Resources/README/interpreter.png?raw=true "interpreter")

#### Jezeli nie ma go na liscie to:

    poetry env info --path

- klikacie Enter interpreter path...
- i podajecie sciezke z gory i po niej /bin/python
