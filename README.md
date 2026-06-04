# Apache Airflow Learning Reference

A personal learning repository created while working through the Astronomer Airflow 101 course and exploring Apache Airflow concepts.

The purpose of this repository is to provide practical examples, notes, and reference material for understanding Airflow fundamentals, DAG development, scheduling, orchestration, debugging, testing, and task dependencies.

## Learning Objectives

- Understand Apache Airflow architecture
- Create DAGs using the TaskFlow API
- Define task dependencies
- Work with scheduling and catchup behaviour
- Use Variables, Connections, and XComs
- Debug DAG parsing and scheduling issues
- Test DAGs locally using Astronomer CLI
- Build a foundation for orchestrating modern data platforms

## Course Reference

This repository was created while working through the Astronomer Airflow 101 learning path:

- Airflow 101: https://academy.astronomer.io/path/airflow-101
- Lead Instructor: Marc Lamberti
- Airflow CLI Module: Faizan Qazi

All notes, examples, modifications, and explanations in this repository are my own learning exercises and interpretations of the course material.

## Repository Structure

```text
.
├── dags/
├── docs/
└── README.md
```

## Example DAGs

| DAG | Purpose |
|------|---------|
| `task_dependencies_dag.py` | Demonstrates task dependencies, branching, fan-out patterns, and the `chain()` helper |
| `bash_task_dag.py` | Demonstrates `@task.bash`, Bash task execution, file creation, validation, and task dependencies |
| `exampledag.py` | Astronomer example DAG generated during project initialisation. Demonstrates the TaskFlow API, API calls, Assets, XComs, and dynamic task mapping |

## Topics Covered

- Airflow Architecture
- DAG Fundamentals
- TaskFlow API
- Task Dependencies
- Scheduling
- Catchup
- Variables
- Connections
- XComs
- Sensors
- Dynamic Task Mapping
- DAG Parsing
- DAG Processor Logs
- Scheduler Debugging
- Connection Debugging
- Astronomer CLI

## Local Development

Validate DAGs:

```bash
astro dev parse
```

Test a specific task:

```bash
astro dev run tasks test <dag_id> <task_id> <logical_date>
```

Example:

```bash
astro dev run tasks test bash_task_dag create_file 2026-06-03
```

Start a local Airflow environment:

```bash
astro dev start
```

Stop a local Airflow environment:

```bash
astro dev stop
```

## GitHub Codespaces Setup

This project can also be run in GitHub Codespaces when Docker Desktop, WSL 2, or local administrator access is not available.

See [GitHub Codespaces Setup](docs/github_codespaces_setup.md).


## Notes

This repository focuses on learning Apache Airflow fundamentals through practical examples and experimentation.

The examples are intentionally simple and designed to demonstrate core Airflow concepts rather than production-ready pipelines.

The `exampledag.py` file was generated automatically by Astronomer project initialisation and has been intentionally retained as a reference example.