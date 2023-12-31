# **Welcome!**
This project provides an end-to-end pipeline for forecasting financial securities. It is not yet complete, as I have been recreating and refining the process completely from scratch and across languages (from R to Python). It is very similar to the process that I was responsible for in my previous role but I have made several adjustments and improvements to the methodology.

Realistically, this project will be constrained by the data and compute resources freely available to me. Therefore, it is mainly intended to demonstrate capability.

## Data Ingestion
Data is collected from various sources via APIs and urls to JSON files. After cleaning and transforming the raw data, it is stored with SQLite databases in tables specific to the source and other defining factors. These tables are updated programatically, however, this has yet to be automated. Data integrity tests are performed upon appending the tables.
```python
conn = sqlite3.connect('Treasury_Yields_data.db')
cursor = conn.cursor()

# Fetch data and create tables for each frequency
for series_code in series_codes:
    for frequency in frequencies:
        full_series_code = prefix + series_code
        # Adjust the frequency in the Quandl request
        data = quandl.get(full_series_code, collapse=frequency)
        # Remove any observations that represent "accrued" observations
        data = data[data.index <= pd.to_datetime(current_date)]
        # Create a table for the original series
        table_name = f"{series_codes[series_code]}_{frequency}"
        # Create a table for the original series
        data.to_sql(table_name, conn, if_exists='replace', index=True)
        # Create a table for the period-to-period difference
        diff_data = data.diff()
        diff_table_name = f"{table_name}_diff"
        diff_data.to_sql(diff_table_name, conn, if_exists='replace', index=True)
        # Create a table for the percent change
        percent_change_data = data.pct_change()
        percent_change_table_name = f"{table_name}_percent_change"
        percent_change_data.to_sql(percent_change_table_name, conn, if_exists='replace', index=True)

# Commit changes and close connection
conn.commit()
conn.close()

print("Databases created successfully.")
```

## Variable Selection
Databases are first merged to create a comprehensive dataset of over 1800 observations of greater than 500 unique variables. This larger data contains variables of various reporting histories and levels of completeness. An ideal trade-off between depth and breadth of the dataset is presumed by calculating the percentage of complete variables over time and eye-balling the best cut-off.

![pic from merge databases script](https://github.com/thestockman27/Fixed-Income-Dashboards/blob/main/merged_databases_output.png)


Due to constraints in compute resources the remainging dataset is reduced further via statistical tests. We first assess the correlation of each variable with the lead of the target variable. After selecting the top variables, they are subject to a test of multicollinearity which further reduces the pool of potential independent variables.
```python
correlated_variables = select_top_variables(df3.loc[df3.index[:InSamp_length]], 'YIELD_weekly_percent_change_10 YR_lead', 200)

vif_results = calculate_vif(df3.loc[df3.index[:InSamp_length], correlated_variables['Variable']])
```
The third step of the variable selection procedure is a Granger Causality test. This involves first running the variables through a process of fitting an Ordinary Least Squares regression of increasing order to determine the ideal number of lags for each remaining series based on Akaike Information Criterion (AIC). From there, we are able to determine which independent variables granger-cause the target variable.


```python
def select_lag_aic(target_series, var_series, max_lag=50):
    lags = range(1, max_lag + 1)
    aic_values = []

    for lag in lags:
        X = lagmat2ds(var_series, lag, trim='both', dropex=1)
        X = sm.add_constant(X)
        model = sm.OLS(target_series[lag:], X)
        result = model.fit()
        aic_values.append(result.aic)

    return lags[np.argmin(aic_values)]

def granger_causality_test(target_series, var_series, max_lag):
    X = lagmat2ds(var_series, max_lag, trim='both', dropex=1)
    X = sm.add_constant(X)
    y = target_series[max_lag:]
    model = sm.OLS(y, X)
    result = model.fit()

    return result.f_pvalue
```

## Training the Model
A Gradient Boosting Machine was selected for training due to the size and nature of the dataset. The target variable was transformed into a categorical variable represent LONG or SHORT values. 

We specify a one-step-ahead time-series cross-validation and specify proposed hyperparameter values prior to conducting the gridsearch. Performance is measured using the Accuracy metric. Lastly, training is not done in parallel so that the predictions of each model can be stored and later retrieved.
```python
gbm = GradientBoostingClassifier(random_state=248)

param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.01, 0.1],
    'subsample': [0.75, 1.0],
    'max_depth': [15, 35],
    'min_samples_leaf': [1]
}

grid_search = GridSearchCV(gbm, param_grid, cv=tscv, scoring=scorer(), verbose=1)

grid_search.fit(X, y)
```
Performance is compared across hyperparameter values and the best performing model is saved.

![Hyperparameter Histogram picture](https://github.com/thestockman27/Fixed-Income-Dashboards/blob/main/Hyperparameter%20Histogram.png)


## Back-test Performance Calculation
We import the back-test object and retrieve the predictions made by the best estimator. A dataframe is constructed using these predictions, the accompanying dates, and the original values of the target variable. For interest rates, [total return is calculated](https://datarepository.eur.nl/articles/dataset/Data_Treasury_Bond_Return_Data_Starting_in_1962/8152748?file=38737083) as this value was not publicly accessible.
```python
merged_data['ret'] = 0
# Calculate 'ret' for each row
for i in range(1, len(merged_data)):
    merged_data['ret'].iloc[i] = (-merged_data['Approx. Duration'].iloc[i] * (
            (merged_data['10 YR Lvl'].iloc[i] / 100) - (merged_data['10 YR Lvl'].iloc[i - 1] / 100)
        )) + (0.5 * merged_data['Approx. Convexity'].iloc[i] * (
            (merged_data['10 YR Lvl'].iloc[i] / 100) - (merged_data['10 YR Lvl'].iloc[i - 1] / 100)
        )**2) + (
            (1 + (merged_data['10 YR Lvl'].iloc[i - 1] / 100))**(1 / 52) - 1
        )
```

Performance is calculated for our model with consideration given to transaction costs. For the purpose of comparison, static long and static short performance is also calculated.
- #### [Back-test Performance](https://github.com/thestockman27/Fixed-Income-Dashboards/blob/main/Backtest%20Performance%20Calculation.ipynb)

![OOS performance chart](https://github.com/thestockman27/Fixed-Income-Dashboards/blob/main/Backtest%20Chart.png)

## Updating of Live-performance
Once the model has been brought into production the live performance is tracked.

*To Do*
- OOS vs Live
    - add a table here
    - 

## Automation
- Portions of the project are intended to be automated using [Apache Airflow](https://airflow.apache.org/) and [Docker](https://www.docker.com/)

- Must identify how to create a custom docker image of airflow that contains the modules necessary to run this project

-  Here is an example of the code that will be used once the new docker image is created:
```python
# Update Treasury Yields Database DAG
from datetime import datetime, timedelta
from airflow import DAG
#from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.providers.papermill.operators.papermill import PapermillOperator 

default_args = {
    'owner':'Derek',
    'retries':1,
    'retry_delay':timedelta(minutes=2) 
}


with DAG(
    dag_id='Update Treasury Yields Database',
    default_args=default_args,
    schedule_interval='@Weekly',
    start_date=datetime(2023,12,16,2)
) as dag:
    run_this = PapermillOperator(
        task_id="Update Database",
        input_nb="C:/Users/dstoc/Documents/Python Scripts/Fixed Income Dashboards/Treasury Yields db update.ipynb",
        output_nb="C:/Users/dstoc/Documents/Python Scripts/Fixed Income Dashboards/Treasury Yields db update out-{{ execution_date }}.ipynb"
    )

```