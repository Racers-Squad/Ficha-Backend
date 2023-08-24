import json
import os

from app.utils.DotDict import DotDict


class Config(DotDict):

    def __init__(self) -> None:
        self.project_path, self.config_path = self._get_config_path()
        config_data = self._read_config(self.config_path)
        super().__init__(config_data)

    @staticmethod
    def _get_config_path() -> (str, str):
        project_root_path = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(project_root_path, "config.json")
        local_config_path = os.path.join(project_root_path, "config.local.json")
        for path in (local_config_path, config_path):
            if os.path.exists(path):
                return project_root_path, path

    @staticmethod
    def _read_config(file_path: str) -> dict:
        try:
            with open(file_path, encoding='utf-8') as file:
                config_data = json.load(file)
            return config_data
        except FileNotFoundError:
            raise FileNotFoundError("Создай файл конфига (config.json или config.local.json) в корне проекта !!!")

    def rewrite(self, data=None):
        with open(self.config_path, 'w') as file:
            file.write(json.dumps(self if not data else data))
