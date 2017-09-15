# Epidemic propagation
> Based on Mesa [Game of Life](https://github.com/projectmesa/mesa/tree/master/examples/conways_game_of_life)

## Virtualenv

```
virutalenv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Run epidemic model

To run the model interactively, run ``run.py`` in this directory:

```
    python3 run.py
``` 

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press ``run``. 

## Files

* ``epidemic/cell.py``: Defines the behavior of an individual cell, which can be in two states: DEAD or ALIVE.
* ``epidemic/model.py``: Defines the model itself, initialized with a random configuration of alive and dead cells.
* ``epidemic/portrayal.py``: Describes for the front end how to render a cell.
* ``epidemic/server.py``: Defines an interactive visualization.
* ``run.py``: Launches the visualization 

