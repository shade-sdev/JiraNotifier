# Jira Notifier

The **Jira Notifier** is a Python script that monitors a Jira RSS feed, extracts relevant information from new entries, and sends desktop notifications for those entries. This script is designed to help you stay updated on activities and changes in your Jira project.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Introduction

The **Jira Notifier** script fetches an RSS feed from a specified Jira project, extracts important information from new entries, and sends desktop notifications with relevant information and links to the Jira entries. It provides a convenient way to receive timely updates without constantly monitoring the project activity.

## Prerequisites

Before using the **Jira Notifier** script, make sure you have the following installed:

- Python 3.x
- Required Python packages (`pip install feedparser requests beautifulsoup4 winotify`):
  - `feedparser`
  - `requests`
  - `beautifulsoup4`
  - `winotify`

## Installation

1. Clone or download this repository to your local machine.
2. Open a terminal and navigate to the downloaded directory.

## Usage

To use the **Jira Notifier** script, follow these steps:

1. Configure the script by updating the values of the following constants in the script:
   - `PROJECT_NAME`: The key of the Jira project.
   - `RSS_FEED_URL`: The URL of the Jira RSS feed.
   - `JESSSION_ID`: Your Jira session ID.
   - `LINK_NUMBER`: The position of the link you want to extract from the entry title.
   - `FETCH_EVERY_SECOND`: The interval in seconds at which the script checks the RSS feed.

2. Run the script:
   ```bash
   python jira_notifier.py
   ```

3. The script will start monitoring the Jira RSS feed and sending notifications for new entries.

## Configuration

Before running the script, ensure you configure the following constants in the script:

- `PROJECT_NAME`: Replace this with the name of your Jira project.
- `RSS_FEED_URL`: Replace this with the URL of the Jira RSS feed.
- `JESSSION_ID`: Replace this with your Jira session ID.
- `LINK_NUMBER`: Set this to the position of the link you want to extract from the entry title.
- `FETCH_EVERY_SECOND`: Set the interval in seconds at which the script checks the RSS feed.