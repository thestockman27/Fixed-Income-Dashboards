to do:

- THE GOAL IS TO HAVE SOMETHING PRESENTABLE BY JANUARY 2024


- automate everything using airflow or prefect
    - # https://www.prefect.io/
                or
    - docker
    - install airflow

- finish README.md

- start trading on IBKR using futures
    - once it actually performs well...

- feature engineering
    -  longer run averages
    - 


Extra Credit:
- clean up repo...
    - organize with folders and delete unneccesary things
- copy everything over to a repo with a name that fits this project better
- convert everything to .py files?
    - not sure if this is necessary
- add auction data (treasury direct)
    - ok so this dataset is highly discontinuous.
    - I can create a weekly timeseries dataset out of it by coercing variables as follows:
        - create columns for each tenor issued
            - this will have to be approximated as sometimes the issues are brought to market out of sync with tenor (ex. 9 year and 6 months for a 10 year note)
        - observations will have to be done weekly as categorical flag variables
            - make each observation coincide with week-end (whatever the other databases are)
            - was this tenor brought to market? results? discount rate? bid-to-cover?
    - updating would have to accommodate announcements of future issues that appear in the dataset
- add currency data
- add foreign yield data
    - 
- LIME for model interpretability
- dtw
    - people are starting to use it
    - does this really make sense to use?
- model selection
    - investigate successive halving for future training
 
- xgBoost? pyspark? pytorch? AWS EC2 instance?

- expand databases from FRED, repo facility?,
- roll out more models
- debugger
- unit tests
- transfer learning, new datasets? different tenors? new data of the same y?
    - gbm has a 'partial_fit' feature that sounds similar to transfer learning