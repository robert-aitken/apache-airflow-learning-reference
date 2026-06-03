# Airflow 101 Notes

These notes summarise my learning from the Astronomer Airflow 101 learning path. They are written as my own reference notes rather than a copy of the course.

Course reference: https://academy.astronomer.io/path/airflow-101

## Module 1: Introduction to Orchestration and Airflow

### What I Learnt

Airflow is an orchestration tool. It is used to define, schedule, run, monitor, and troubleshoot workflows.

A workflow is normally made of multiple tasks. For a data pipeline, that might be:

```text
extract data
load data
transform data
run tests
publish output
```

Airflow is useful when tasks need to happen in a specific order, at a specific time, or only after other tasks have completed.

### Simple Explanation

Airflow does not usually do the heavy data processing itself. It tells other tools what to do, when to do it, and in what order.

For example, Airflow might tell Python to download a file, DuckDB to load it, dbt to transform it, and then run checks at the end.

### Key Point

Airflow is best for orchestration, not for storing data or replacing a database.

## Module 2: Airflow Basics

### What I Learnt

Airflow has several core components:

| Component | Simple Explanation |
|---|---|
| API Server | Serves the Airflow UI and API |
| Scheduler | Decides what needs to run and when |
| Metadata Database | Stores Airflow state, DAG runs, task status, users, variables, and connections |
| DAG Processor | Reads and parses DAG files |
| Executor | Decides how and where tasks are executed |
| Queue | Holds tasks waiting to run |
| Worker | Runs the actual task instructions |

### How Airflow Runs a DAG

```text
DAG file is placed in the dags folder
DAG processor parses the file
DAG is stored in the metadata database
Scheduler checks if the DAG should run
Executor queues the tasks
Worker runs the tasks
Task status is written back to Airflow
```

### DAG File Structure

A DAG file normally has four parts:

```python
from airflow.sdk import dag, task
from pendulum import datetime


@dag(
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
)
def example_dag():

    @task
    def first_task():
        print("First task")

    @task
    def second_task():
        print("Second task")

    first_task() >> second_task()


example_dag()
```

### Key Concepts

| Term | Meaning |
|---|---|
| DAG | Directed Acyclic Graph. A workflow with tasks and dependencies |
| Task | One unit of work |
| Upstream | A task that must run before another task |
| Downstream | A task that runs after another task |
| Dependency | The relationship between tasks |
| `>>` | Sets a left-to-right dependency |
| `<<` | Sets a right-to-left dependency |

### Example

```python
extract() >> transform() >> load()
```

This means:

```text
extract runs first
transform runs second
load runs third
```

## Module 3: Local Development Environment

### What I Learnt

There are different ways to run Airflow locally, but the course used the Astro CLI because it gives a quick Docker-based Airflow setup.

### Common Commands

Install Astro CLI on macOS:

```bash
brew install astro
```

Check the installed version:

```bash
astro version
```

Create a new Astro project:

```bash
mkdir local_airflow
cd local_airflow
astro dev init
```

Start Airflow locally:

```bash
astro dev start
```

Stop Airflow locally:

```bash
astro dev stop
```

Restart the environment:

```bash
astro dev restart
```

Validate DAGs:

```bash
astro dev parse
```

### Project Structure

| File Or Folder | Purpose |
|---|---|
| `dags/` | Python DAG files |
| `include/` | Extra files used by DAGs |
| `plugins/` | Custom Airflow plugins |
| `requirements.txt` | Python dependencies |
| `packages.txt` | OS-level dependencies |
| `Dockerfile` | Astro Runtime image setup |
| `airflow_settings.yaml` | Local Airflow variables, connections, and pools |

### VS Code Issue

When running:

```bash
code .
```

I got:

```text
zsh: command not found: code
```

The fix was to install the VS Code shell command from VS Code:

```text
Cmd + Shift + P
Shell Command: Install 'code' command in PATH
```

### Key Point

For local learning, Astro CLI and Docker make it much easier to run Airflow without manually installing every Airflow component.

## Module 4: Airflow UI

### What I Learnt

The Airflow UI is used to monitor and manage DAGs, DAG runs, and task runs.

### Main UI Views

| View | Use |
|---|---|
| DAGs View | See all DAGs, pause or unpause DAGs, trigger DAGs |
| Grid View | Best general view for checking DAG runs and task status |
| Graph View | Best for understanding task dependencies visually |
| Logs | Best for debugging why a task failed |
| Code View | Shows the DAG code parsed by Airflow |
| Details | Shows metadata about DAG runs and task runs |

### Common Task States

| State | Meaning |
|---|---|
| Success | Task completed |
| Failed | Task failed |
| Running | Task is currently running |
| Queued | Task is waiting to run |
| Scheduled | Scheduler has scheduled the task |
| Skipped | Task was skipped |
| Upstream Failed | A previous dependency failed |

### Simple Explanation

The UI is like the control room for Airflow. The code defines the workflow, but the UI shows what happened when Airflow tried to run it.

## Module 5: DAGs 101

### What I Learnt

A DAG is a Python-defined workflow. It should describe tasks and dependencies clearly.

### Basic TaskFlow DAG

```python
from airflow.sdk import dag, task
from pendulum import datetime


@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
)
def simple_dag():

    @task
    def say_hello():
        print("Hello from Airflow")

    say_hello()


simple_dag()
```

### Dependencies

Simple dependency:

```python
task_a() >> task_b()
```

Chain of tasks:

```python
task_a() >> task_b() >> task_c()
```

Fan-out:

```python
task_a() >> [task_b(), task_c()]
```

Using `chain()`:

```python
from airflow.sdk import chain

chain(task_a(), [task_b(), task_d()], [task_c(), task_e()])
```

This represents:

```text
       task_b -> task_c
      /
task_a
      \
       task_d -> task_e
```

### Key Point

Airflow DAGs should be readable. The DAG should make the order of tasks obvious.

## Module 6: DAG Scheduling

### What I Learnt

Scheduling controls when a DAG runs.

### Important Scheduling Parameters

| Parameter | Meaning |
|---|---|
| `schedule` | How often the DAG should run |
| `start_date` | The earliest date Airflow can create runs from |
| `end_date` | Optional date when scheduling should stop |
| `catchup` | Whether Airflow should create historical missed runs |

### Example

```python
@dag(
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
)
def daily_dag():
    ...
```

### Common Schedule Values

```python
schedule=None
schedule="@daily"
schedule="@hourly"
schedule="0 9 * * *"
```

### Simple Explanation of `catchup`

If `catchup=True`, Airflow may create old DAG runs from the `start_date`.

If `catchup=False`, Airflow usually creates only the latest scheduled run.

### Example

```python
@dag(
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
)
```

If this DAG is unpaused today, Airflow will not run every missing day since 2023. It will only create the latest relevant run.

### Key Point

Scheduling in Airflow is logical-date based. A run date is not always the same thing as the time the task physically runs.

## Module 7: XComs 101

### What I Learnt

XCom means cross-communication. It allows tasks to pass small values to other tasks.

### TaskFlow Example

```python
from airflow.sdk import dag, task
from pendulum import datetime


@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
)
def xcom_dag():

    @task
    def extract_number():
        return 10

    @task
    def multiply_number(number):
        print(number * 2)

    multiply_number(extract_number())


xcom_dag()
```

### Manual XCom Push And Pull

```python
context["ti"].xcom_push(key="my_key", value="my_value")
```

```python
value = context["ti"].xcom_pull(key="my_key", task_ids="upstream_task")
```

### What XCom Is Good For

- Small values
- IDs
- Status values
- File paths
- Simple metadata

### What XCom Is Not Good For

- Large datasets
- Big DataFrames
- Large JSON objects
- Files

### Key Point

Use XCom for small messages between tasks, not for moving large data.

## Module 8: Sensors

### What I Learnt

A sensor waits for something to happen before allowing the DAG to continue.

### Examples

| Sensor Type | What It Waits For |
|---|---|
| File sensor | A file to exist |
| API sensor | An API condition to be true |
| SQL sensor | A database query condition |
| External task sensor | Another DAG or task to complete |

### Simple Local File Sensor Example

```python
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import dag, task
from pendulum import datetime


@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
)
def local_file_sensor_dag():

    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath="/tmp/example.csv",
        poke_interval=10,
        timeout=60,
    )

    @task
    def process_file():
        print("File is ready")

    wait_for_file >> process_file()


local_file_sensor_dag()
```

### Poke Mode vs Reschedule Mode

| Mode | Simple Explanation |
|---|---|
| `poke` | Sensor keeps occupying a worker slot while waiting |
| `reschedule` | Sensor frees the worker slot between checks |

### Key Point

Sensors are useful, but a badly configured sensor can waste resources.

## Module 9: Command Line Interface

### What I Learnt

The CLI is useful for local development, debugging, checking Airflow configuration, and testing tasks.

### Commands I Used Frequently

```bash
astro dev parse
```

Checks whether DAGs can be parsed successfully.

```bash
astro dev restart
```

Restarts the local Astro environment.

```bash
astro dev bash
```

Opens a shell inside the local Airflow environment.

```bash
astro dev run info
```

Runs an Airflow CLI command through Astro.

### Airflow CLI Examples

```bash
airflow info
```

Shows information about the Airflow installation.

```bash
airflow connections list
```

Lists configured Airflow connections.

```bash
airflow variables list
```

Lists configured Airflow variables.

```bash
airflow pools list
```

Lists Airflow pools.

```bash
airflow tasks test <dag_id> <task_id> <logical_date>
```

Tests a single task locally.

Example:

```bash
astro dev run tasks test bash_task_dag create_file 2026-06-03
```

### Key Point

The CLI is useful when you want fast feedback without clicking around the UI.

## Module 10: Connections and Variables

### What I Learnt About Connections

A connection stores credentials or configuration for an external system.

Examples:

- API host
- Snowflake account details
- Postgres connection
- S3 connection
- Login and password
- Extra JSON configuration

### Simple Explanation

A connection lets DAG code say:

```text
use this saved connection
```

instead of hard-coding usernames, passwords, hosts, and keys inside the DAG.

### Connection ID

A connection must have one unique `conn_id`.

Example:

```python
conn_id="snowflake"
```

The operator uses that ID to find the connection.

### Ways To Create Connections

| Method | Notes |
|---|---|
| Airflow UI | Easy for learning and local testing |
| Environment variable | Better for code-like local setup |
| `airflow_settings.yaml` | Useful in Astro local development |
| Secrets backend | Better for production |
| CLI or REST API | Useful for automation |

### Environment Variable Pattern

```bash
AIRFLOW_CONN_SNOWFLAKE='snowflake://user:password@account/db-schema?account=account_name'
```

After changing connection environment variables, restart Airflow:

```bash
astro dev restart
```

### What I Learnt About Variables

A variable stores reusable configuration values.

Examples:

- API base URL
- File path
- Environment name
- Simple JSON config

### Variable Example

```python
from airflow.sdk import dag, task, Variable
from pendulum import datetime


@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
)
def variable_dag():

    @task
    def print_api_config():
        api_config = Variable.get("api", deserialize_json=True)
        print(api_config)

    print_api_config()


variable_dag()
```

### Example Variable Value

```json
{
  "url": "https://jsonplaceholder.typicode.com",
  "endpoint": "/todos/1"
}
```

### Environment Variable Pattern

```bash
AIRFLOW_VAR_MY_VAR='my value'
```

For JSON:

```bash
AIRFLOW_VAR_API='{"url": "https://example.com", "endpoint": "/v1"}'
```

### Sensitive Variable Names

Airflow can hide variable values in the UI when the key contains sensitive words such as:

```text
password
secret
api_key
token
```

### Key Point

Use Connections for external systems and credentials. Use Variables for simple reusable configuration.

## Module 11: Debug DAGs

### What I Learnt

Debugging in Airflow is about narrowing down where the problem is:

```text
DAG not discovered
DAG import error
DAG shows but does not schedule
Task fails
Connection fails
Sensor waits forever
```

### DAG Does Not Show Up

Possible causes:

- File is not inside the `dags/` folder
- File does not contain a DAG object
- DAG function was not called
- Python syntax error
- Import error
- Duplicate DAG ID
- DAG parsing is delayed

### Example Issue

```python
@dag(
    "test_dag",
    start_date=datetime(2023, 3, 1),
)
def test_dag():
    ...
```

If the function is not called, Airflow will not register it.

Fix:

```python
test_dag()
```

### Start Date In The Future

If `start_date` is in the future, manual or scheduled behaviour may be confusing.

Example:

```python
start_date=datetime(3030, 3, 1)
```

This is a problem because the DAG is not logically ready to run.

### Debugging DAG Processor Logs

Inside the Airflow environment, DAG processor logs can be checked.

Example path:

```bash
logs/dag_processor/latest/dags-folder/my_dag.py.log
```

This helps confirm whether Airflow is parsing a DAG file.

### Connection Debugging

Things to check:

- Is the `conn_id` spelt exactly the same?
- Is the connection type correct?
- Is the provider installed?
- Is the value coming from a secrets backend, environment variable, or metadata database?
- Is the connection being fetched inside a task rather than at import time?

### Lookup Order For Connections

Highest priority first:

```text
secrets backend
environment variables
Airflow metadata database
```

### Key Point

Do not fetch connections or variables at DAG import time if you can avoid it. Fetch them inside tasks so DAG parsing stays fast and reliable.

## Repository DAG Examples

### task_dependencies_dag.py

Demonstrates:

- TaskFlow API
- Task dependencies
- `chain()`
- Branching
- Fan-out patterns

### bash_task_dag.py

Demonstrates:

- `@task.bash`
- Bash command execution
- Creating a local file
- Checking a file exists
- Reading a file in a Python task

### exampledag.py

This was generated during Astronomer project initialisation and retained as a reference example.

It demonstrates:

- TaskFlow API
- API call
- Assets
- XCom
- Dynamic task mapping

## High-Level Takeaways

Airflow is useful when:

- A process has multiple ordered steps
- Some tasks depend on other tasks
- A process needs to run on a schedule
- Failures need to be visible and recoverable
- Workflows need to be version controlled
- Data pipelines need to be monitored

Airflow is less suitable when:

- You only need a simple one-off script
- You need a database
- You need a data transformation framework
- You need a streaming engine
- You want the tool itself to process massive datasets directly
