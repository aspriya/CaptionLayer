import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

class ProjectManager:
    def __init__(self, base_workspace_dir: str):
        self.base_workspace_dir = Path(base_workspace_dir)
        self.current_project_dir: Optional[Path] = None
        
        # Ensure base workspace exists
        self.base_workspace_dir.mkdir(parents=True, exist_ok=True)

    def create_project(self, project_name: str) -> Path:
        """Create a new local project structure."""
        safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_').lower()
        
        project_dir = self.base_workspace_dir / safe_name
        if project_dir.exists():
            raise FileExistsError(f"Project directory {project_dir} already exists.")
            
        # Create folder structure
        project_dir.mkdir(parents=True)
        (project_dir / "assets" / "audio").mkdir(parents=True)
        (project_dir / "intermediate").mkdir(parents=True)
        (project_dir / "timelines").mkdir(parents=True)
        (project_dir / "exports").mkdir(parents=True)
        (project_dir / "logs").mkdir(parents=True)
        
        # Create project metadata
        metadata = {
            "project_id": safe_name,
            "name": project_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        with open(project_dir / "project.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)
            
        self.current_project_dir = project_dir
        return project_dir
        
    def load_project(self, project_dir: str) -> Dict:
        """Load an existing project."""
        p_dir = Path(project_dir)
        if not p_dir.exists() or not (p_dir / "project.json").exists():
            raise FileNotFoundError("Valid project directory not found.")
            
        with open(p_dir / "project.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)
            
        self.current_project_dir = p_dir
        return metadata

    def import_audio(self, source_audio_path: str) -> Path:
        """Import an audio file into the current project."""
        if not self.current_project_dir:
            raise ValueError("No active project. Create or load a project first.")
            
        src_path = Path(source_audio_path)
        if not src_path.exists():
            raise FileNotFoundError(f"Source audio file not found: {source_audio_path}")
            
        dest_dir = self.current_project_dir / "assets" / "audio"
        dest_path = dest_dir / src_path.name
        
        # Copy the file
        shutil.copy2(src_path, dest_path)
        
        # Update project data
        metadata_path = self.current_project_dir / "project.json"
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            
        metadata["updated_at"] = datetime.now().isoformat()
        metadata["audio_asset"] = str(dest_path.relative_to(self.current_project_dir))
        
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)
            
        return dest_path
