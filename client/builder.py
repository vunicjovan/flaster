import os


class Builder:
    def __init__(self, target_path, project, apps):
        # command line arguments
        self.target_path = target_path
        self.project = project
        self.apps = apps

        # class-specific arguments
        self.project_root = f"{self.target_path}/{self.project}"

        self.root_folder = dict(
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

        self.root_packages = dict(
            apps=self.apps,
            database={},
        )

        self.root_files = dict(
            app="py",
            config="py",
        )

    def _build_file(self, file_path, file_name, file_content):  # noqa
        with open(f"{file_path}/{file_name}", "w+") as infile:
            infile.write(file_content)

    def build_project(self):
        # Build project folder
        os.mkdir(self.project_root)

        # Build static directories and their respective files on the project root path
        for root_folder, subfolders in self.root_folder.items():
            # Build static directory on the project root path
            os.mkdir(f"{self.project_root}/{root_folder}")

            # If there are any subfolders of the previously built directory - build them, too
            if subfolders:
                for subfolder in subfolders:
                    # Build subfolder of static directory on the project root path
                    subfolder_path = f"{self.project_root}/{root_folder}/{subfolder}"
                    os.mkdir(subfolder_path)

                    sf = subfolders.get(subfolder)

                    # Build static files within subfolders - if any
                    if sf:
                        for item in sf:
                            self._build_file(
                                file_path=subfolder_path,
                                file_name=item,
                                file_content="<html><body>Hello, world!</body></html>",
                            )

        # Build Python packages on the project root path
        for root_package, subpackages in self.root_packages.items():
            # Build Python package on the project root path
            PACKAGE_ROOT = f"{self.project_root}/{root_package}"
            os.mkdir(PACKAGE_ROOT)

            # Build __init__.py file for current Python package
            self._build_file(
                file_path=PACKAGE_ROOT,
                file_name="__init__.py",
                file_content="\n",
            )

            # Build subpackage directories on the package root path
            [os.mkdir(f"{PACKAGE_ROOT}/{subpackage}") for subpackage in subpackages]

        # Build files on the project root path
        for root_file, file_extension in self.root_files.items():
            self._build_file(
                file_path=self.project_root,
                file_name=f"{root_file}.{file_extension}",
                file_content="",
            )
