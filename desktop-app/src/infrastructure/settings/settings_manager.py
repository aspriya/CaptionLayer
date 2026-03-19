import json
from pathlib import Path
from typing import Dict, Any

class SettingsManager:
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            self.config_dir = Path.home() / ".config" / "captionlayer"
        else:
            self.config_dir = Path(config_dir)
            
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = self.config_dir / "settings.json"
        
        self.settings = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        self.settings[key] = value
        self._save()
