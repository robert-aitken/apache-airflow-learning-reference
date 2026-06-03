# Airflow 101 Troubleshooting Notes

These notes summarise common Airflow issues from the course and my local development.

## 1. DAG Does Not Show In The UI

### Common Causes

- DAG file is not in the `dags/` folder
- DAG function is not called
- Python syntax error
- Import error
- Duplicate `dag_id`
- File name or DAG file does not look like a DAG
- DAG processor has not picked it up yet
- DAG is hidden by permissions or UI filters

### Quick Checks

```bash
astro dev parse
```

Check Airflow UI import errors.

Check the DAG processor logs.

### Simple Fixes

Make sure the DAG file ends up in:

```text
dags/
```

Make sure the DAG function is called:

```python
my_dag()
```

Make sure the DAG ID is unique.

## 2. DAG Import Error

### Symptoms

- DAG does not show
- Airflow UI shows an import error
- `astro dev parse` fails

### Common Causes

- Syntax error
- Bad indentation
- Missing Python package
- Wrong import path
- Missing `__init__.py` in a package layout
- Code running at import time

### Example

```text
ModuleNotFoundError: No module named 'your_module'
```

### Fix

Install the dependency in:

```text
requirements.txt
```

Then restart or rebuild the Astro environment.

## 3. Slow DAG Import

### Problem

A DAG can be slow to appear or parse if heavy work happens at import time.

### Bad Pattern

```python
api_response = requests.get("https://example.com")
```

This runs when Airflow parses the DAG, not when the task runs.

### Better Pattern

```python
@task
def call_api():
    api_response = requests.get("https://example.com")
    return api_response.json()
```

### Simple Rule

Keep the top level of a DAG file lightweight. Put real work inside tasks.

## 4. DAG Shows But Does Not Schedule

### Common Causes

- DAG is paused
- `schedule=None`
- `start_date` is in the future
- `end_date` has passed
- `catchup` behaviour is misunderstood
- Existing active runs are blocking new runs
- Pool slots are unavailable
- `max_active_runs` or `max_active_tasks` limit has been reached

### Example

```python
@dag(
    schedule=None,
)
```

This means no automatic schedule. You must trigger it manually.

## 5. Future Start Date

### Problem

```python
start_date=datetime(3030, 3, 1)
```

The DAG is not logically ready to run.

### Fix

Use a realistic past or current start date.

```python
start_date=datetime(2025, 1, 1)
```

## 6. Catchup Confusion

### Problem

An old `start_date` can create many historical runs if `catchup=True`.

### Safer Learning Setup

```python
catchup=False
```

This avoids accidentally creating lots of backfill runs.

## 7. Task Fails

### What To Check

- Task logs
- Python exception
- Operator arguments
- Missing file or path
- Missing variable
- Missing connection
- Wrong connection ID
- Permission issue

### Useful Command

```bash
astro dev run tasks test <dag_id> <task_id> <logical_date>
```

Example:

```bash
astro dev run tasks test bash_task_dag read_file 2026-06-03
```

## 8. File Sensor Does Not Continue

### Common Causes

- File path is wrong
- File is in the host machine but not inside the container
- Sensor timeout is too short
- Sensor is checking the wrong directory
- Sensor mode is using resources inefficiently

### Simple Check

Use `astro dev bash` and check inside the Airflow container:

```bash
ls /tmp
```

## 9. Connection Not Found

### Common Causes

- Wrong `conn_id`
- Different capitalisation
- Connection was not created
- Provider package not installed
- Environment variable not loaded
- Airflow was not restarted after changing environment variables

### Connection Lookup Order

```text
secrets backend
environment variables
Airflow metadata database
```

### Important Point

If the same connection exists in multiple places, the higher priority source wins.

## 10. Provider Not Installed

### Problem

An operator or connection type may not be available.

### Example

Snowflake operators require the Snowflake provider.

### Fix

Add the provider package to:

```text
requirements.txt
```

Then restart or rebuild the environment.

## 11. Variables Not Found

### Common Causes

- Variable key is misspelt
- Variable only exists in the UI but environment was reset
- Environment variable was not loaded
- JSON variable is not valid JSON
- `deserialize_json=True` was not used for JSON values

### Example

```python
Variable.get("api", deserialize_json=True)
```

Use `deserialize_json=True` when the value is stored as JSON and you want a Python dictionary.

## 12. Sensitive Values Showing In UI

### Safer Options

- Use Connections for credentials
- Use a secrets backend for production
- Use environment variables for local learning
- Avoid committing secrets to Git

### Sensitive Key Names

Airflow can hide values when the variable name contains words such as:

```text
password
secret
api_key
token
```

This helps in the UI, but it is not a substitute for proper secret management.

## 13. DAG Processor Logs

### Why They Matter

DAG processor logs show whether Airflow is parsing a DAG file.

### Example Path

```bash
logs/dag_processor/latest/dags-folder/my_dag.py.log
```

### Example Command

```bash
cat logs/dag_processor/latest/dags-folder/my_dag.py.log
```

### Simple Explanation

If the DAG processor keeps logging that it is filling the DagBag from a file, it means Airflow is repeatedly parsing that DAG file.

## 14. `astro dev parse` Warning About Pytest Cache

### Example

```text
PytestCacheWarning: could not create cache path
```

### Meaning

This warning is usually not a DAG problem.

### What Matters

If the output says:

```text
No errors detected in your DAGs
```

then the DAG parse check passed.

## 15. DAG Still Appears After File Deletion Or Rename

### Why It Happens

Airflow stores DAG metadata. A deleted file may still leave metadata in the UI for a while.

### Fix Options

- Wait for refresh
- Restart the local environment
- Check DAGs in the UI
- In some cases, clear local metadata if safe to do so

## 16. Best Debugging Order

Use this order when something breaks:

```text
1. Run astro dev parse
2. Check the Airflow UI import errors
3. Check the DAG appears in the DAGs list
4. Check the Grid view
5. Check task logs
6. Test one task with airflow tasks test
7. Check variables and connections
8. Check DAG processor logs
9. Restart the local environment if needed
```