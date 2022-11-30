import dynaconf


settings = dynaconf.Dynaconf(
    envvar_prefix='ISIS',
    settings_files=[
        'settings.toml',
    ],
    environments=True,
    load_dotenv=True,
)
