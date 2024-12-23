import typer
import os
import os
import importlib
import typer


def load_and_register_commands(
    app: typer.Typer,
    dir_abspath: str,
    common_file_name: str = "run.py",
):
    """
    Import functions from the directories inside <dir_abspath> (subdirectories) and add them as commands to the given typer <app>.
    The subdirectory must contain a file called <common_file_name>.
    The <common_file_name> file must contain a function with the same name as the subdirectory.
    """

    # Iterate over the subdirectories
    for dir_name in os.listdir(dir_abspath):
        dir_path = os.path.join(dir_abspath, dir_name)

        # Check if the subdirectory contains a file called <common_file_name>
        if os.path.isdir(dir_path) and os.path.exists(
            os.path.join(dir_path, common_file_name)
        ):
            # Dynamically import the module
            module_name = f"{dir_name}.{common_file_name.replace('.py', '')}"
            module = importlib.import_module(module_name)

            # Get the function by the same name as the directory
            function = getattr(module, dir_name, None)

            # If the function exists, add it as a command to the typer app
            if function and callable(function):
                app.command(name=dir_name)(function)


app = typer.Typer()
dir_abspath = os.path.abspath(os.path.dirname(__file__))
load_and_register_commands(app, dir_abspath)


if __name__ == "__main__":
    app()
