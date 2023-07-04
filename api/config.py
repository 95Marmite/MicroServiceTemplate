from pydantic import BaseSettings


class _LoggingConfig(BaseSettings):
    logdir: str = "./"
    logdestinations: str = "console, file"
    consoledebuglevel: str = "DEBUG"
    filedebuglevel: str = "DEBUG"


class Config(BaseSettings):
    """A configuration class for the application.

    This class defines various settings for the application, such as the application name,
    logging configuration, Redis configuration, and the task package.

    Attributes:
        appname (str): The name of the application.
        logging (_LoggingConfig): The logging configuration object.

    Configurations:
        env_prefix (str): The prefix used for environment variables. Default is "inference_".
        env_nested_delimiter (str): The delimiter used for nested environment variables. Default is "__".
    """
    appname: str = "test"
    host: str = "127.0.0.1"
    port: int = 8000
    logging: _LoggingConfig = _LoggingConfig()


config = Config()
