from client.builder import Builder
from client.commander import Commander

if __name__ == "__main__":
    commander = Commander()

    TARGET_PATH = commander.args.target_path
    PROJECT_NAME = commander.args.project
    APPS = commander.args.apps

    builder = Builder(target_path=TARGET_PATH, project=PROJECT_NAME, apps=APPS)

    builder.build_project()
