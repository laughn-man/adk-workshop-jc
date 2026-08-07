# adk-workshop-jc

This guide explains how to setup and run the Jupyter notebooks in this project. They are intended to be ran locally as opposed to in Google Collab. There are several module with code that they share.

# Setup

Two things are required to run the notebooks in this project.

## uv

uv package manager is used to manage the project dependencies. To install it go to https://docs.astral.sh/uv/getting-started/installation/ to download and install it for your OS.

## .env

A .env file needs to created at the root of the project. This is file is git ignored so it will not be committed. The file needs to have the following variables:

* PROJECT_ID: The GCP project id.
* LOCATION: The GCP location. 
* STAGING_BUCKET: The name of the staging bucket for app deployments.
* GOOGLE_MAPS_KEY: API key to allow access to the Google Maps APIs. Make sure to enable them.
* GEMINI_API_KEY: API key for making GEMINI calls. Make sure to enable the API.

# Modules

The following modules are shared between the notebooks and contain common functionality used through out.

* agent_tester: Contains logic for running the agents.
* callbacks: Agent call back functions.
* config: Shared config values used throughout the project.
* instructions: Code for getting instructions from the resources/instructions folder.
* tools: Tool functions.

# Notebooks

These are the notebooks for each challenge:

* [challenge-1-weather-agent.ipynb](./challenge-1-weather-agent.ipynb)
* [challenge-2-callbacks.ipynb](./challenge-2-callbacks.ipynb)
* [challenge-3-multi-agent.ipynb](./challenge-3-multi-agent.ipynb)
* [challenge-4-agent-workflow.ipynb](./challenge-4-agent-workflow.ipynb)
* [challenge-5-agent-platform.ipynb](./challenge-5-agent-platform.ipynb)
* [challenge-6-fema.ipynb](./challenge-6-fema.ipynb)