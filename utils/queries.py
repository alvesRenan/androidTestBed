########## DB creation ##########
CREATE_DB_CONTAINERS = """CREATE TABLE IF NOT EXISTS  containers (
  scenario_name text,
  container_name text,
  adb_connection text,
  memory text,
  network text,
  container_state text default 'CREATED',
  is_server integer default 0,
  cpus text default '---'
)"""

CREATE_DB_SCENARIOS = """CREATE TABLE IF NOT EXISTS scenarios (
  scenario_name text,
  scenario_state text default 'STOPPED'
)"""
####################

########## Scenario Queries ##########
SCENARIO_EXISTS = "SELECT 1 FROM scenarios WHERE scenario_name = :name"

INSET_SCENARIO = "INSERT INTO scenarios (scenario_name) VALUES ( :name )"

LIST_ALL_SCENARIOS = "SELECT * FROM scenarios"

DELETE_SCENARIO = "DELETE FROM scenarios WHERE scenario_name = :name"
####################

########## Container Queries ##########
CONTAINER_EXISTS = "SELECT 1 FROM containers WHERE container_name = :name"

INSET_CONTAINER = """INSERT INTO containers (
  scenario_name,
  container_name,
  adb_connection,
  memory,
  network) VALUES (?, ?, ?, ?, ?)"""

# LIST_ALL_SCENARIOS = "SELECT * FROM scenarios"

# DELETE_SCENARIO = "DELETE FROM scenarios WHERE scenario_name = :name"
####################