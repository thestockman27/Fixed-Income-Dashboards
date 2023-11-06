to do:

- rebuild the databases
    - Treasury databases is adding an observation for the current unfinished period for some reason
    - may be able to solve using some sort of logic that removes future dates

- code for forecasting off of new data
    - some sort of visualization?
    - track forecasts separate from backtest
    - add live-performance to backtest results
        - import backtest performance calculation file
        - add new preds, and obs of Y
        - update calcs


- automate everything using airflow or prefect
    - # https://www.prefect.io/
    - install linux Virtual machine
    - install airflow


Extra Credit:
- LIME for model interpretability
- variable selection...yeah we are going to need this
    - rank correlation
        - review this
    - dtw
        - people are starting to use it
- model selection
    - investigate successive halving for future training
 
- expand databases from FRED
- roll out more models
- debugger
- unit tests

