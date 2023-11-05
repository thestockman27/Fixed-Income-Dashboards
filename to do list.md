to do:

- looks like the Treasury databases are not updating properly
    - need to fix before continuing
    - something is wrong with the logic when updating diff and % diff databases
    -  need to write some logic that uses the second to last date so that old data is pulled for calculating diff and percent diff
    - will also need to add code to only add obs after the latest 



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

