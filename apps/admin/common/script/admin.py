from flask.cli import AppGroup

admin_cli = AppGroup("admin")


@admin_cli.command("init")
def init_db():
    pass
