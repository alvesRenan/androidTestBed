########## DB creation ##########
CREATE_DB_CONTAINERS = """CREATE TABLE IF NOT EXISTS  containers (
  scenario_name text,
  container_name text,
  memory text,
  is_server integer,
  adb_connection text DEFAULT NULL,
  network text DEFAULT NULL,
  container_state text DEFAULT 'CREATED',
  cpus text DEFAULT NULL
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

DELETE_CONTAINERS_FROM_SCENARIO = "DELETE FROM containers WHERE scenario_name = :name"
####################

########## Container Queries ##########
CONTAINER_EXISTS = "SELECT 1 FROM containers WHERE container_name = :name"

INSET_CONTAINER = """INSERT INTO containers (
  scenario_name,
  container_name,
  memory,
  network,
  is_server,
  cpus,
  adb_connection) VALUES (?, ?, ?, ?, ?, ?, ?)"""

LIST_CONTAINERS = """SELECT container_name, adb_connection, memory, network, cpus, container_state
FROM  containers 
WHERE scenario_name = :name
"""

# DELETE_SCENARIO = "DELETE FROM scenarios WHERE scenario_name = :name"
####################