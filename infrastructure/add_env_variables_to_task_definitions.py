import json
import os

if __name__ == "__main__":
    google_env_vars = ["JWT_SECRET_KEY", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"]
    db_env_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST"]
    misc_env_vars = ["OPENAI_API_KEY", "DJANGO_SECRET_KEY"]

    environment_json = []
    for env_var in [*google_env_vars, *db_env_vars, *misc_env_vars]:
        env_dict = {"name": env_var, "value": os.environ.get(env_var)}
        environment_json.append(env_dict)
    with open("infrastructure/task-definition.json") as task_definition_file:
        task_definition = json.load(task_definition_file)
        task_definition["containerDefinitions"][0]["environment"] = environment_json
    with open("infrastructure/task-definition.json", "w") as task_definition_file:
        json.dump(task_definition, task_definition_file, indent=4)
