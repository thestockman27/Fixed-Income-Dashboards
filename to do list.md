to do:

- THE GOAL IS TO HAVE SOMETHING PRESENTABLE BY JANUARY 2024

- rebuild treasury and CoT databases

- add auction data (treasury direct)
    - ok so this dataset is highly discontinuous.
    - I can create a weekly timeseries dataset out of it by coercing variables as follows:
        - create columns for each tenor issued
            - this will have to be approximated as sometimes the issues are brought to market out of sync with tenor (ex. 9 year and 6 months for a 10 year note)
        - observations will have to be done weekly as categorical flag variables
            - make each observation coincide with week-end (whatever the other databases are)
            - was this tenor brought to market? results? discount rate? bid-to-cover?
    - updating would have to accommodate announcements of future issues that appear in the dataset


- update merge databases script to incorporate new databases

- really need to make sure that the variable selection is dialed in


- Re-run Backtests
    - noticed some missing dates in the final backtest results that arose from an issue with dropping rows with inf or -inf
        - re-train models

- code for forecasting off of new data
    - need to add back first date of the backtest dataframe so calcs are the same
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

- convert everything to .py files?
    - not sure if this is necessary


- add a README file to summarize the repository




Extra Credit:
- clean up repo...
    - organize with folders and delete unneccesary things
- copy everything over to a repo with a name that fits this project better
- LIME for model interpretability
- variable selection...yeah we are going to need this
    - rank correlation
        - review this
    - dtw
        - people are starting to use it
        - does this really make sense to use?
- model selection
    - investigate successive halving for future training
 
- pyspark?

- expand databases from FRED,
- roll out more models
- debugger
- unit tests

