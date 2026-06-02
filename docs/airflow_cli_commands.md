# Airflow CLI Commands

This note summarises useful Airflow CLI commands from the Airflow 101 CLI module.

In this project, Airflow runs inside Astro and Docker. That means most commands are run through `astro dev run`, or by entering the Airflow container with `astro dev bash`.

## Quick Rule

Use `astro dev run` when you want to run a single Airflow command from your normal terminal.

Use `astro dev bash` when you want to enter the Airflow container and run several Airflow commands interactively.

## Group 1: Commands You Will Use Frequently

| Command | Description |
|---|---|
| `astro dev parse` | Checks whether DAG files can be imported and parsed successfully. Useful before committing changes. |
| `astro dev restart` | Restarts the local Astro Airflow environment. Useful after changing requirements, environment settings, or Airflow connections. |
| `astro dev bash` | Opens a shell inside the scheduler container so you can run Airflow CLI commands directly. |
| `astro dev run info` | Runs `airflow info` through Astro and shows details about the Airflow environment. |
| `astro dev run tasks test <dag_id> <task_id> <logical_date>` | Tests one task in isolation without running the whole DAG. |

## Frequently Used Examples

Check DAG parsing:

```zsh
astro dev parse
```

Restart the local Airflow environment:

```zsh
astro dev restart
```

Enter the scheduler container:

```zsh
astro dev bash
```

Show Airflow environment information:

```zsh
astro dev run info
```

Test one task:

```zsh
astro dev run tasks test local_file_sensor_dag process_file 2026-06-02
```

Test one sensor task:

```zsh
astro dev run tasks test local_file_sensor_dag wait_for_file 2026-06-02
```

## Group 2: Commands You Will Occasionally Use

These commands are useful when debugging or inspecting the Airflow environment.

| Command | Description |
|---|---|
| `airflow info` | Shows Airflow version, executor, database, paths, Python version, and installed providers. |
| `airflow version` | Shows the installed Airflow version. |
| `airflow config list` | Lists Airflow configuration settings. |
| `airflow config get-value <section> <key>` | Gets one specific Airflow configuration value. |
| `airflow dags list` | Lists DAGs known to Airflow. |
| `airflow dags list-import-errors` | Lists DAG import or parsing errors. Useful when a DAG is not appearing in the UI. |
| `airflow dags report` | Shows DAG parsing information and can help identify loading issues. |
| `airflow connections list` | Lists Airflow connections stored in the metadata database. |
| `airflow variables list` | Lists Airflow variables stored in the metadata database. |
| `airflow pools list` | Lists Airflow pools and their slot configuration. |
| `airflow db check` | Checks that Airflow can connect to its metadata database. |
| `airflow cheat-sheet` | Shows a summary of common Airflow CLI commands. |

## Occasionally Used Examples

Enter the container first:

```zsh
astro dev bash
```

Then run:

```zsh
airflow info
```

Check the Airflow version:

```zsh
airflow version
```

List configuration settings:

```zsh
airflow config list
```

Check a specific configuration value:

```zsh
airflow config get-value core max_active_runs_per_dag
```

Find parallelism settings:

```zsh
airflow config list | grep parallelism
```

List DAG import errors:

```zsh
airflow dags list-import-errors
```

List Airflow variables:

```zsh
airflow variables list
```

List Airflow pools:

```zsh
airflow pools list
```

Check the metadata database connection:

```zsh
airflow db check
```

## Group 3: Commands You Will Rarely Use

These commands are more administrative. They are useful to understand, but less common in day-to-day DAG development, especially when using Astro.

| Command | Description |
|---|---|
| `airflow db init` | Initialises the Airflow metadata database. Usually used when setting up Airflow for the first time. |
| `airflow users create` | Creates an Airflow user. Useful for local/admin setup or role-based access control testing. |
| `airflow users add-role` | Adds a role to an existing Airflow user. |
| `airflow standalone` | Starts an all-in-one Airflow environment for local development. Not for production use. |
| `airflow variables export <file>` | Exports Airflow metadata database variables to a JSON file. |
| `airflow variables import <file>` | Imports Airflow variables from a JSON file. |
| `airflow dags backfill <dag_id>` | Runs a DAG for historical logical dates. Used to fill missing historical runs. |

## Rarely Used Examples

Initialise the Airflow metadata database:

```zsh
airflow db init
```

Create an Admin user:

```zsh
airflow users create -e user@example.com -f Firstname -l Lastname -u admin -p admin -r Admin
```

Create a Viewer user:

```zsh
airflow users create -e viewer@example.com -f Firstname -l Lastname -u viewer -p viewer -r Viewer
```

Add a role to a user:

```zsh
airflow users add-role -e user@example.com -r Custom
```

Start standalone Airflow for local development:

```zsh
airflow standalone
```

Export variables:

```zsh
airflow variables export variables.json
```

Import variables:

```zsh
airflow variables import variables.json
```

Backfill a DAG:

```zsh
airflow dags backfill <dag_id> --start-date 2026-06-01 --end-date 2026-06-05
```

## Important Notes

`airflow tasks test` runs one task in isolation.

It does not run upstream dependencies first.

It does not create a normal DAG run.

It does not persist task metadata in the same way as a real DAG run.

It is useful for checking whether a task can execute successfully.

## Useful Mental Model

`astro dev parse` is like asking whether Airflow can load the project.

`airflow info` is like checking the environment.

`airflow config get-value` is like checking what setting Airflow is actually using.

`airflow tasks test` is like running one task directly for debugging.

`airflow dags list-import-errors` is what to use when a DAG is not showing in the UI.

`airflow dags backfill` is for filling in missing historical DAG runs.

## What To Remember

The CLI is useful for:

- checking environment details
- debugging DAG import errors
- testing individual tasks
- checking configuration values
- managing variables, connections, pools, and users
- running backfills

The Airflow UI is useful for viewing and operating DAGs.

The CLI is useful for inspecting, testing, and troubleshooting Airflow.