import json
import os

if __name__ == "__main__":
    db_env_vars = ["RDS_DB_USER", "RDS_DB_PASSWORD", "DB_HOST", "SQS_ACCESS_SECRET"]
    misc_env_vars = ["OPENAI_API_KEY", "DJANGO_SECRET_KEY"]
    auth0_env_vars = ["AUTH0_DOMAIN", "AUTH0_CLIENT_ID", "AUTH0_CLIENT_SECRET"]
    environment_json = []
    for env_var in [*auth0_env_vars, *db_env_vars, *misc_env_vars]:
        env_dict = {"name": env_var, "value": os.environ.get(env_var)}
        environment_json.append(env_dict)
    with open("infrastructure/task-definition.json") as task_definition_file:
        task_definition = json.load(task_definition_file)
        task_definition["containerDefinitions"][0]["environment"] = environment_json
    with open("infrastructure/task-definition.json", "w") as task_definition_file:
        json.dump(task_definition, task_definition_file, indent=4)
