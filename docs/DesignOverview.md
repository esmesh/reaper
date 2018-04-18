# Reaper (SE for Scientific Software fork) Design Overview

This document provides a rough overview of our understanding of the reaper project with specific attention on how we are using it.

## Files

| File | Purpose |
| --- | -----------|
| batch_score.py |This is the main script of the Reaper application. It is responsible for giving a score to repositories based on attributes. Each attribute has its own way of scoring a repository.  |
| config.json |It is the file which provides configuration to the batch_score.py script. This script can be configured with the credentials to the GHTorrent database as well as the list of attributes to be executed against the repositories. |
| manifest.json |List of attributes to be executed. |
| score_repo.py |Currently outdated. Do not use.  |
| attributes/... |Folder containing the attributes. Each attribute is represented as a folder which contains a main.py script representing the main script for the attribute.  |
| lib/... |Contains the source code for the Reaper program. |
| tests/... | Contains unit tests. |

### config.json

| Variable   | Purpose   |
| ------     | ------    |
| threshold  | Threshold for any of the dimensions/attribute. Example, for documentation dimension,set threshold for ratio of comment lines to source lines.   |
| database   | GHTorrent |
| user       |           |
| password   |           |
| host       |           |


### manifest.json

| Variable   | Purpose   |
| ------     | ------    |
|  name      | Attribute name |
|  weight    | Sets the relative importance of each dimension/attribute|
|  enabled   | Choose to enable/disable an attribute in customized search for repositories |
| requires_source |      |
| dependencies |         |
| timeout  | Sets the time until Reaper runs |
| cutoff  |   |


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
| `community`|double| To show evidence of collaboration and communication between developers during the development of the system. num_core_contributors - Number of core contributors should be more than 1. |
| `continuous_integration`|double| Evidence of developers integrating(building, running and testing) their code combined with code from other developers. Important for understanding the stability of code under continuous evolution for release. The source code looks for confguration files (CI) in the source code repo.|
| `documentation`|double| Documentations like code comments are important for maintenance.The source code for this attribute calculates comment ratio. Uses Perl utility cloc to calculate lines of code and comments.|
| `history`|double| Changes to source code such as bug fixes, feature addition, refactoring, acts as evidence towards practically usable software. For this, commit frequency is calculated by calculating num_commits and avg_commits.  |
| `license`|double| Licenses direct a users' right to use and modify software. It is considered good practice to include license in source code so as to avoid any legal issues under copyright laws as it clealy informs about the source code owner's rights to their code. GitHub License API searches for license availablity in source code repo  files such as LICENSE and COPYING. Does not search for License information in README.md or in source code. |
| `management`|double| Software engineered projects mostly utilize management tools for supporting management of requirements, schedules, tasks, defects, etc. GitHub has a feature called GitHub Issues within which developers can customize labels for their various activities which points towards management of lifecycle of the projects. |
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
- Create a folder with the name of the attribute
- Create a main.py file inside the folder
- Implement the run method
### Design for Attributes that do **require** access to the project source code
- Query the database to get the project URL
- Read the project files using this URL using any preferred library
