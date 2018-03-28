# Reaper (SE for Scientific Software fork) Design Overview

This document provides a rough overview of our understanding of the reaper project with specific attention on how we are using it.

## Files

| File | Purpose |
| --- | -----------|
| batch_score.py | |
| config.json | |
| manifest.json | |
| score_repo.py | |
| attributes/... | |
| lib/... | |
| tests/... | |

## GHTorrent Source Data

[GHTorrent](http://ghtorrent.org/) is a research project that aims to collect
and store information produced by the public GitHub events feed. The initial
implementation of `score_repo.py` relies on this information being accessible. Below is a summary of each of the tables loaded into our `GH_Python` database via the March 1, 2018 data dump from [GHTorrent downloads](http://ghtorrent.org/downloads.html).

| Table | Primary Key | Purpose |
| --- | ---------- | -----------|
| | | |
| | | |
| | | |


## `reaper_results` table in GH_Python

If persist results is enabled a database table needs to exist to which reaper can 
write results. This table is named `reaper_results`. A summary of the table is below.

| Column | Type | Purpose |
| --- | ---------- | -----------|
| `project_id` (primary key) | int(11)| |
| `architecture`|double| |
| `community`|double| |
| `continuous_integration`|double| |
| `documentation`|double| |
| `history`|double| |
| `license`|double| |
| `management`|double| |
| `project_size`|double| |
| `repository_size`|double| |
| `state`|varchar(255)| |
| `stars`|double| |
| `unit_test`|double| |
| `score`|double| |

## Attribute Development

### Overview
> This section was taken verbatim from the original README.

In order to add your own attribute plugin to the system, there are few things
that must be done. First, add an attribute entry as described in the above
section that refers to your specific attribute.

Secondly, create the appropriately named directory under `attributes/` along
with a `main.py`. Inside of this, the following function signature should be
used to kickoff the execution of the plugin:

```python
def run(project_id, repo_path, cursor, **options):
  # Implementation goes here.
```

Check the doc block for details on what each parameter provides in terms of
functionality. Attribute implementations should return a tuple of two values:
the binary result of execution and the raw result of execution. The binary
result should be True or False and the raw result should be a real number that
is the raw calculation made by the plugin. In the case of purely binary results,
do something like `return result, int(result)`.

Additionally, there is the option of initializing the plugin. To take advantage
of initialization, add the following function signature to `main.py`:

```python
def init(cursor, **options):
  # Implementation goes here.
```

### Design for Attributes that do **not** require access to the project source code

### Design for Attributes that do **require** access to the project source code
