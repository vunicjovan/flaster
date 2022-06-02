import os

INIT_FILE = "__init__.py"


class Builder:
    def __init__(self, target_path, project, apps):
        # command line arguments
        self.target_path = target_path
        self.project = project
        self.apps = apps

        # class-specific arguments
        self.PROJECT_ROOT = f"{self.target_path}/{self.project}"

        self.STATIC_AND_TEMPLATES = dict(
            static=dict(
                css=[],
                js=[],
                img=[],
            ),
            templates=dict(
                layouts=[
                    "app.html",
                    "header.html",
                    "footer.html",
                ],
            ),
        )

        self.APPS_AND_DATABASE = dict(
            apps=self.apps,
            database={},
        )

        self.MAIN_AND_CONFIG = dict(
            app="py",
            config="py",
        )

    def _build_file(self, file_path, file_name, file_content):  # noqa
        os.makedirs(file_path, exist_ok=True)

        with open(f"{file_path}/{file_name}", "w+") as infile:
            infile.write(file_content)

    def _build_blueprint_app(self, app):
        APP_PATH = f"{self.PROJECT_ROOT}/apps/{app}"
        app_files = [INIT_FILE, "views.py", "models.py"]

        # Build views and models for each blueprint application
        for app_file in app_files:
            self._build_file(
                file_path=APP_PATH,
                file_name=app_file,
                file_content="\n",
            )

        # Build directory for HTML templates for each blueprint application
        templates_path = f"{APP_PATH}/templates/{app}"

        self._build_file(
            file_path=templates_path,
            file_name="index.html",
            # TODO: Change HTMLs to accordingly designed ones
            file_content="<html><body>Hello, world!</body></html>",
        )

    def build_project(self):
        # Build project folder
        os.mkdir(self.PROJECT_ROOT)

        # Build static directories and their respective files on the project root path
        for root_folder, subfolders in self.STATIC_AND_TEMPLATES.items():
            # Build static directory on the project root path
            os.mkdir(f"{self.PROJECT_ROOT}/{root_folder}")

            # If there are any subfolders of the previously built directory - build them, too
            if subfolders:
                for subfolder in subfolders:
                    # Build subfolder of static directory on the project root path
                    subfolder_path = f"{self.PROJECT_ROOT}/{root_folder}/{subfolder}"
                    os.mkdir(subfolder_path)

                    sf = subfolders.get(subfolder)

                    # Build static files within subfolders - if any
                    if sf:
                        for item in sf:
                            self._build_file(
                                file_path=subfolder_path,
                                file_name=item,
                                # TODO: Change HTMLs to accordingly designed ones
                                file_content="<html><body>Hello, world!</body></html>",
                            )

        # Build Python packages on the project root path
        for root_package, subpackages in self.APPS_AND_DATABASE.items():
            # Build Python package on the project root path
            PACKAGE_ROOT = f"{self.PROJECT_ROOT}/{root_package}"
            os.mkdir(PACKAGE_ROOT)

            # Build __init__.py file for current Python package
            self._build_file(
                file_path=PACKAGE_ROOT,
                file_name=INIT_FILE,
                file_content="\n",
            )

            # Build subpackage directories on the package root path
            [os.mkdir(f"{PACKAGE_ROOT}/{subpackage}") for subpackage in subpackages]

        # Build basic inner structure for each blueprint application
        for app in self.apps:
            self._build_blueprint_app(app)

        # Build basic inner structure for database connection
        db_path = f"{self.PROJECT_ROOT}/database"
        db_files = [INIT_FILE, "database.py"]

        [
            self._build_file(file_path=db_path, file_name=db_file, file_content="\n")
            for db_file in db_files
        ]

        # Build files on the project root path
        for root_file, file_extension in self.MAIN_AND_CONFIG.items():
            self._build_file(
                file_path=self.PROJECT_ROOT,
                file_name=f"{root_file}.{file_extension}",
                file_content="",
            )
