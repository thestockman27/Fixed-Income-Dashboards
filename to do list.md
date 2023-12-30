to do:

- THE GOAL IS TO HAVE SOMETHING PRESENTABLE BY JANUARY 2024


- convert data download files to .py files and create a simple DAG
    -  need to create my own docker image of airflow that contains the necessary modules to run my code
    - base image does not come with everything
    - additional PIP requirements is apparently not a safe method as updates can ruin the image...

- feature engineering
    - longer run averages of target variable
        - I'll need to code up the inclusion of the y0 value of the target variable in the final batch of variables
        - rolling cumprod (4,13,26)
    - volatility

- finish README.md

- start trading on IBKR using futures
    - once it actually performs well...




Extra Credit:
- clean up repo...
    - organize with folders and delete unneccesary things
- copy everything over to a repo with a name that fits this project better
- convert everything to .py files?
    - not sure if this is necessary
- expand databases
    - FRED 
    - repo facility?
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
    
- LIME for model interpretability
- dtw
    - people are starting to use it
    - does this really make sense to use?
- model selection
    - investigate successive halving for future training
- xgBoost? pyspark? pytorch? AWS EC2 instance?
- roll out more models
- debugger
- unit tests
- transfer learning, new datasets? different tenors? new data of the same y?
    - gbm has a 'partial_fit' feature that sounds similar to transfer learning

- git ignore file for airflow repo
