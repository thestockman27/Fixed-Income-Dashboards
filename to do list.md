to do:
- publish final model stats
    - extract predictions from cv_results
        - may have to infer predictions from the split accuracy columns, 1 is correct 0 is incorrect
    - date, actual (Y), forecast (ForY)
    - pos
    - turnover
    - ret = pos * actual - turnover (double check long and short logic here)
    - cumulative return of $1
    - static long
    - ratios ()

- code for forecasting off of new data

- LIME for model interpretability

- automate everything using airflow


Extra Credit:
- variable selection...yeah we are going to need this
    - rank correlation
    - dtw?
    - maybe a future improvement...
- model selection
    - investigate successive halving for future training
 
- expand databases from FRED


