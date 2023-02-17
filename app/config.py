from pathlib import Path

from utils import create_directory, local_date

Root_path = Path.cwd().__str__()


class Config:
    @property
    def log_dir(self):
        path = Path(Root_path, "logs")
        create_directory(str(path))
        return path

    def log_name(self):
        return self.log_dir / f"{local_date()}.log"
