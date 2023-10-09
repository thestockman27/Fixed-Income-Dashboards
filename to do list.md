to do:

- train gbm
    - rolling one period ahead cross validation backtest
        - weekly dates are all recorded as sundays so we can do a simple one period ahead
        - create lead for independent target variable
    - across 50ish hyperparameter combinations
    - run performance stats
        - just the basic ones at this point
        
- model selection
    - plot distributions by hyperparameter
    - plot master performance distribution

- publish final model stats
    - cumulative return of $1
        - static long all that shit...

- automate everything using airflow


- variable selection?
    - rank correlation
    - dtw?
    - maybe a future improvement...
 


