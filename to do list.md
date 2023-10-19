to do:

- publish final model stats
    - create dataframe containing
        - date, actual (Y), lead Y (Y1), forecast for the lead (ForY1)
        - ensure dates line up
        - insamp, outsamp, fullsamp
    - write one calculate_performance function
        - calculate
            - pos
            - turnover
            - ret = pos * actual - turnover (double check long and short logic here)
                - verify total return calculation
            - cumulative return of $1
            - static long
            - ratios (sharpe, sortino, information)
            - drawdowns
        - run it for each sample period
    - export as table or something nice looking with graphs

- code for forecasting off of new data
    - import latest observations from SQL databases and model
    - some sort of visualization?
    - track forecasts separate from backtest
    - add live-performance to backtest


- automate everything using airflow or prefect
    - # https://www.prefect.io/
    - install linux Virtual machine
    - install airflow


Extra Credit:
- LIME for model interpretability
- variable selection...yeah we are going to need this
    - rank correlation
        - review this
    - dtw?
- model selection
    - investigate successive halving for future training
 
- expand databases from FRED
- roll out more models
- debugger
- unit tests

