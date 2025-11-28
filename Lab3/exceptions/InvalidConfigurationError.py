class InvalidConfigurationError(Exception):
    """Вызывается, когда конфигурация системы содержит недопустимые значения."""

    def __init__(self, message: str, config_key: str = None, config_value: str = None):
        self.config_key = config_key
        self.config_value = config_value
        super().__init__(message)

