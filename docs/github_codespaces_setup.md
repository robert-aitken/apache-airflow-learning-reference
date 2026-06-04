# GitHub Codespaces Setup

## Official Documentation References

This guide is based on the following official documentation:

* [GitHub Codespaces Port Forwarding](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace)
* [Astro CLI Installation](https://www.astronomer.io/docs/astro/cli/install-cli)

## Purpose

This document explains how to run this Apache Airflow learning project in GitHub Codespaces.

Codespaces is useful when a local machine cannot run Docker Desktop, WSL 2, or the Astro CLI directly. This can happen on managed Windows devices where administrator access, Microsoft Store, `winget`, WSL 2, or Docker virtualisation are restricted.

Using Codespaces provides a cloud-based Linux development environment where the project can be run without changing the local machine.

## When To Use This Setup

Use this setup if:

* Docker Desktop cannot start locally
* WSL 2 is not installed or cannot be enabled
* Administrator permissions are not available
* `winget` or Microsoft Store access is blocked
* You want a clean browser-based environment for learning Airflow

For a personal Mac or unrestricted development machine, the standard local Astro CLI setup may be simpler.

## Prerequisites

You need:

* A GitHub account
* Access to this repository
* GitHub Codespaces enabled for your account
* Available Codespaces usage allowance

Do not use this environment for sensitive data, internal organisational data, credentials, or production secrets.

## Start A Codespace

Open the repository in GitHub.

Select:

```text
Code > Codespaces > Create codespace on main
```

Wait for the browser-based VS Code environment to start.

The terminal should open inside the repository directory, similar to:

```bash
/workspaces/apache-airflow-learning-reference
```

## Install The Astro CLI

Install the Astro CLI inside the Codespaces terminal:

```bash
curl -sSL https://install.astronomer.io | sudo bash
```

Check the installation:

```bash
astro version
```

Expected result:

```text
Astro CLI Version: <version-number>
```

Optional: disable anonymous Astro CLI telemetry for the environment:

```bash
astro telemetry disable
```

## Check Docker

Codespaces should provide Docker support.

Check the Docker client and server:

```bash
docker version
```

Then check Docker engine details:

```bash
docker info
```

If both commands return server information, Docker is available and the Astro project can be started.

## Start Airflow

From the repository root, run:

```bash
astro dev start
```

This builds the local Airflow image and starts the Airflow containers.

To check the running containers, open a second terminal and run:

```bash
docker ps
```

You should see containers for Airflow components such as:

```text
api-server
scheduler
dag-processor
triggerer
postgres
```

## Open Airflow In The Browser

After `astro dev start` completes, open the forwarded Airflow port from the Codespaces UI:

```text
VS Code > Panel > Ports > 8080 > Open in Browser
```

The correct URL should look similar to:

```text
https://<codespace-name>-8080.app.github.dev
```

Use the GitHub forwarded URL from the **Ports** tab.

Do not use a `.localhost` proxy URL such as:

```text
http://apache-airflow-learning-reference.localhost:<port>
```

That URL may work inside some local environments, but from a restricted Windows machine it can point back to the local device rather than the Codespaces environment.

## Login To Airflow

Use the default local Airflow credentials:

```text
Username: admin
Password: admin
```

After logging in, the DAGs from the `dags` directory should be visible in the Airflow UI.

## Example: Airflow Variables

Some DAGs may require Airflow Variables before they run successfully.

For example, a DAG that contains:

```python
Variable.get("api", deserialize_json=True)
```

requires an Airflow Variable with the key:

```text
api
```

Example value:

```json
{
  "base_url": "https://example.com",
  "timeout_seconds": 30
}
```

This can be added in the Airflow UI:

```text
Airflow UI > Admin > Variables > +
```

Use fake example values only. Do not store real API keys, tokens, passwords, or internal work URLs in this learning environment.

## Useful Commands

Show running containers:

```bash
docker ps
```

View Astro logs:

```bash
astro dev logs
```

Restart the local Airflow environment:

```bash
astro dev restart
```

Stop the local Airflow environment:

```bash
astro dev stop
```

Check DAG parsing:

```bash
astro dev parse
```

## Stop The Codespace

When finished, stop Airflow:

```bash
astro dev stop
```

Then stop the Codespace from GitHub:

```text
GitHub > Your profile > Codespaces > Stop codespace
```

Stopping the Codespace helps avoid unnecessary Codespaces usage.

## Troubleshooting

### Astro CLI Is Not Installed

If this command fails:

```bash
astro version
```

Re-run the installer:

```bash
curl -sSL https://install.astronomer.io | sudo bash
```

Then check again:

```bash
astro version
```

### Docker Is Not Running

Check Docker:

```bash
docker version
docker info
```

If Docker server details are missing, the Codespace may not have Docker support enabled.

### Airflow Page Does Not Open

Check that the containers are running:

```bash
docker ps
```

Then open the forwarded Airflow port:

```text
VS Code > Panel > Ports > 8080 > Open in Browser
```

The correct browser URL should use:

```text
github.dev
```

or:

```text
app.github.dev
```

Avoid opening the `.localhost` proxy URL from the Astro Dev Proxy page.

### Port 8080 Is Not Listed

Open the Ports tab and manually add port `8080`:

```text
VS Code > Panel > Ports > Add Port > 8080
```

Then open the forwarded port in the browser.

### DAG Fails With VARIABLE_NOT_FOUND

The DAG is trying to read an Airflow Variable that has not been created.

Create the missing variable in the Airflow UI:

```text
Airflow UI > Admin > Variables > +
```

For example, if the error says:

```text
Variable api not found
```

create a variable with:

```text
Key: api
```

If the DAG uses `deserialize_json=True`, the value must be valid JSON.

### Codespace Usage

Codespaces uses GitHub-hosted compute and storage.

Stop the Codespace when it is not being used.
