# Local File Sensor DAG

This note explains how to run and test `local_file_sensor_dag.py`.

The DAG waits for a local file called `data_1.csv`. When the file exists, the sensor succeeds and the downstream task runs.

## Files Used

```text
dags/local_file_sensor_dag.py
include/data_1.csv
airflow_settings.yaml
```

`include/data_1.csv` is only a temporary test file. It does not need to contain any data.

The sensor only checks whether the file exists.

## Airflow Connection

The DAG uses this connection:

```text
fs_default
```

In local Astro development, this connection should point to:

```text
/usr/local/airflow/include/
```

Add this to `airflow_settings.yaml`:

```yaml
airflow:
  connections:
    - conn_id: fs_default
      conn_type: File (path)
      conn_host:
      conn_schema:
      conn_login:
      conn_password:
      conn_port:
      conn_extra:
        path: /usr/local/airflow/include/
```

Do not commit `airflow_settings.yaml` if it is ignored by Git. It may contain local settings or secrets later.

## Restart Astro

After changing `airflow_settings.yaml`, restart Astro:

```zsh
astro dev restart
```

You should see:

```text
Added Connection: fs_default
```

## Parse the DAGs

Run:

```zsh
astro dev parse
```

Expected result:

```text
No errors detected in your DAGs
```

## Test Immediate Success

Create the test file:

```zsh
touch include/data_1.csv
```

Trigger `local_file_sensor_dag` in the Airflow UI.

Expected result:

```text
wait_for_file -> Success
process_file -> Success
DAG run -> Success
```

## Test the Sensor Waiting

Remove the test file:

```zsh
rm -f include/data_1.csv
```

Trigger `local_file_sensor_dag` again.

Expected result:

```text
wait_for_file -> Running or Up For Reschedule
process_file -> No Status
```

The sensor checks for the file every 60 seconds because the DAG uses:

```python
poke_interval=60
```

## Create the File While the Sensor Is Waiting

Run:

```zsh
touch include/data_1.csv
```

Within about 60 seconds, the sensor should detect the file.

Expected result:

```text
wait_for_file -> Success
process_file -> Success
DAG run -> Success
```

## Check the Logs

Open the `wait_for_file` task and check the logs.

You should see lines similar to:

```text
Poking for file /usr/local/airflow/include/data_1.csv
Found File /usr/local/airflow/include/data_1.csv
Success criteria met
```

## Check the Pool

Go to:

```text
Admin > Pools
```

or open:

```text
http://local-airflow.localhost:6563/pools
```

This shows how many worker slots are being used.

With `mode="reschedule"`, the sensor should not hold a worker slot between checks.

## Why This Example Matters

This is a local training example.

In real data engineering work, the same sensor idea is often used for cloud or external systems, such as:

- waiting for a file in S3
- waiting for a file in Azure Blob Storage
- waiting for another DAG to finish
- waiting for an API to become available
- waiting for data to appear in a table

The core idea is the same:

```text
Wait until a condition is true, then continue the pipeline.
```

## Git Notes

Commit these files:

```text
dags/local_file_sensor_dag.py
docs/local_file_sensor_dag.md
include/.gitkeep
```

Do not commit this test file:

```text
include/data_1.csv
```

`data_1.csv` is runtime test data. It is better to create it manually when testing.
