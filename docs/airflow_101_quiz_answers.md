# Airflow 101 Quiz And Clarification Notes

These are the questions and concepts that needed extra clarification during the course, rewritten in simple language.

## Basics

### What Does The Scheduler Do?

The scheduler decides which tasks need to run and when.

It does not execute the task code itself. It checks schedules, DAG runs, task dependencies, and task states.

Simple answer:

```text
The scheduler decides what should run next.
```

## What Does The Executor Do?

The executor decides how and where tasks are executed.

Simple answer:

```text
The scheduler decides what should run.
The executor decides how it should be run.
The worker actually runs it.
```

## Which Component Executes Task Logic?

The worker executes the task logic.

Simple answer:

```text
The worker runs the code inside the task.
```

## How Long Can It Take For A New DAG To Appear?

By default, it can take up to 5 minutes for the DAG file processor to detect a new DAG file.

In local development, it may appear sooner, but 5 minutes is the safe answer from the course.

## Do Workers Have Direct Access To The Metadata Database?

No.

Workers do not directly access the metadata database in the same way as the scheduler or API server.

The worker executes task code and reports task state back through Airflow's execution mechanisms.

## What Must You Do After Creating A DAG File?

Put the Python file in the `dags/` folder.

Airflow then has a chance to detect and parse it.

## Where Do You Define How Often A DAG Runs?

You define the schedule in the DAG object definition.

Example:

```python
@dag(
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
)
def my_dag():
    ...
```

## What Do These Imports Do?

```python
from airflow.sdk import dag
from airflow.providers.standard.operators.python import PythonOperator
```

Simple explanation:

```text
The first import lets you define an Airflow DAG.
The second import gives you an operator for running Python code as a task.
```

## Task Dependencies

### What Does This Mean?

```python
task_extract >> task_transform >> task_load
```

It means:

```text
task_extract runs first
task_transform runs second
task_load runs third
```

`task_transform` is downstream of `task_extract`.

`task_extract` is upstream of `task_transform`.

## DAG File Components

A DAG file normally contains:

| Part | Meaning |
|---|---|
| Imports | Bring in Airflow objects and Python packages |
| DAG definition | Defines the workflow settings |
| Tasks | Define the units of work |
| Dependencies | Define the order tasks run in |

## Local Development

### Why Did `code .` Fail?

Error:

```text
zsh: command not found: code
```

Reason:

```text
The Mac terminal did not know the VS Code command yet.
```

Fix:

```text
Open VS Code
Press Cmd + Shift + P
Run Shell Command: Install 'code' command in PATH
Restart terminal
```

## Scheduling

### What Happens With `catchup=False`?

If a DAG has an old `start_date` but `catchup=False`, Airflow does not create every old missed run.

It normally creates only the latest scheduled run.

Example:

```python
@dag(
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
)
```

If unpaused today, the answer is usually one latest run, not hundreds of backfilled runs.

## DAG Does Not Show In The UI

### Question

This DAG does not show up. Why?

```python
from airflow.decorators import dag, task
from pendulum import datetime

@dag(
    "test_dag",
    start_date=datetime(2023, 3, 1),
)
def test_dag():
    @task
    def test_task():
        return "Hello World"

    test_task()
```

### Answer

The DAG function is not called.

Fix:

```python
test_dag()
```

### Simple Explanation

Defining the function is not enough. You must call it so Airflow creates the DAG object.

## Manual Trigger With Future Start Date

### Question

Why do you not see task execution?

```python
@dag(
    "test_dag",
    start_date=datetime(3030, 3, 1),
)
```

### Answer

The `start_date` is in the future.

### Simple Explanation

Airflow sees the DAG as not logically ready yet.

## How Many DAG Runs With Catchup Disabled?

### Question

How many running DAG runs appear when this DAG is unpaused?

```python
@dag(
    "test_dag",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
)
```

### Answer

One.

### Simple Explanation

Because `catchup=False`, Airflow does not create all missed historical runs.

## How Long Until A DAG Appears In The UI?

Answer:

```text
By default, it may take up to 5 minutes or more.
```

Simple explanation:

```text
Airflow needs time for the DAG processor to scan, parse, and store the DAG.
```

## Can Tasks Use Different Python Versions In The Same DAG?

Yes.

Simple explanation:

```text
Different tasks can run in different isolated environments, such as containers or virtual environments.
```

This is more advanced than a basic Python task, but Airflow can support it.

## Connections

### Can You Create Two Connections With The Same ID?

No.

A connection ID must be unique.

### What Is An Airflow Connection?

A connection stores reusable credentials or configuration for an external system.

Examples:

- API
- Snowflake
- Postgres
- S3
- SSH

### Why Define A Connection?

To avoid hard-coding sensitive values in DAG files and to reuse the same connection across multiple DAGs.

## Variables

### Should Three DAGs Fetching From The Same API Use A Variable?

Yes, if the value is shared configuration, such as a base URL.

Example:

```json
{
  "url": "https://example.com"
}
```

### Where Can Variables Be Stored?

Variables can be stored in:

- Airflow metadata database
- Secrets backend
- Environment variable

Not in the metaverse.

### Does An Environment Variable Need A Database Connection?

No.

If a variable is created through an environment variable, Airflow can read it from the environment rather than fetching it from the metadata database.

## Secrets Backend

### What Is A Secrets Backend?

A secrets backend is an external place where Airflow can look up secrets such as connections and variables.

Examples:

- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- Google Secret Manager

### Is It Pre-Installed?

Airflow supports secrets backends, but you normally configure which one to use.

In a simple local Astro project, you may not be using a secrets backend unless you explicitly configure one.

### Why Use It?

It is better for production because secrets are not stored directly in the Airflow UI, Git, or local files.

## `airflow tasks test`

### What Does It Do?

It runs one task manually for a specific logical date.

Example:

```bash
astro dev run tasks test variable_dag print_api_config 2026-06-02
```

### Does It Run The Whole DAG?

No.

It tests one task.

### Why Is It Useful?

It gives fast feedback when developing and debugging a task.
