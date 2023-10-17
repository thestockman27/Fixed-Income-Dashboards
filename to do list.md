to do:

- publish final model stats
    - extract predictions from cv_results
        - may have to infer predictions from the split accuracy columns, 1 is correct 0 is incorrect
        - looks like the best way to do this is to define a custom scoring function that returns the predictions
    - create dataframe containing
        - date, actual (Y), forecast (ForY)
    - calculate
        - pos
        - turnover
        - ret = pos * actual - turnover (double check long and short logic here)
        - cumulative return of $1
        - static long
        - ratios (sharpe, sortino, information)
        - drawdowns
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
    - dtw?
    - maybe a future improvement...
- model selection
    - investigate successive halving for future training
 
- expand databases from FRED


