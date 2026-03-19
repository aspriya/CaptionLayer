import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QListWidget, QFrame, QSplitter,
    QFileDialog, QMessageBox, QInputDialog, QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor
from pathlib import Path
import json

from src.infrastructure.storage.project_manager import ProjectManager
from src.infrastructure.settings.settings_manager import SettingsManager
from src.workers.transcription_worker import TranscriptionWorker
from src.infrastructure.environment import EnvironmentChecker
from src.domain.schemas.timeline import CanonicalTimeline
from src.pipeline.export.exporter import TimelineExporter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CaptionLayer Workflow")
        self.resize(1000, 700)
        
        # Core states
        self.pm = ProjectManager(str(Path.home() / "CaptionLayerProjects"))
        self.settings = SettingsManager()
        self.worker = None
        self.current_timeline_path = None
        self.exporter = TimelineExporter()

        # Apply dark theme
        self.apply_dark_theme()
        
        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter to divide Sidebar and Main Content
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # --- Sidebar ---
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setStyleSheet("QFrame#Sidebar { background-color: #1e1e1e; border-right: 1px solid #333; }")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)
        
        app_title = QLabel("CaptionLayer")
        app_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        app_title.setStyleSheet("color: white;")
        sidebar_layout.addWidget(app_title)

        self.project_name_label = QLabel("No Project Active")
        self.project_name_label.setFont(QFont("Segoe UI", 10))
        self.project_name_label.setStyleSheet("color: #aaaaaa; margin-bottom: 10px;")
        self.project_name_label.setWordWrap(True)
        sidebar_layout.addWidget(self.project_name_label)
        
        self.btn_new_project = QPushButton("New Project")
        self.btn_new_project.setStyleSheet(self.btn_style(primary=True))
        sidebar_layout.addWidget(self.btn_new_project)
        
        self.btn_new_project.clicked.connect(self.handle_new_project)

        self.btn_import_audio = QPushButton("Import Audio")
        self.btn_import_audio.setStyleSheet(self.btn_style())
        self.btn_import_audio.setEnabled(False)
        self.btn_import_audio.clicked.connect(self.handle_import_audio)
        sidebar_layout.addWidget(self.btn_import_audio)

        
        self.btn_export = QPushButton("Export Subtitles")
        self.btn_export.setStyleSheet(self.btn_style())
        self.btn_export.clicked.connect(self.handle_export)
        self.btn_export.setEnabled(False)
        sidebar_layout.addWidget(self.btn_export)
        
        sidebar_layout.addStretch()

        self.btn_workspace = QPushButton("Workspace")
        self.btn_workspace.setStyleSheet(self.btn_style())
        self.btn_workspace.clicked.connect(lambda: self.main_stack.setCurrentIndex(0))
        sidebar_layout.addWidget(self.btn_workspace)

        self.btn_code_view = QPushButton("Code / JSON View")
        self.btn_code_view.setStyleSheet(self.btn_style())
        self.btn_code_view.setEnabled(False)
        self.btn_code_view.clicked.connect(self.show_code_view)
        sidebar_layout.addWidget(self.btn_code_view)

        self.btn_config = QPushButton("Configuration")
        self.btn_config.setStyleSheet(self.btn_style())
        self.btn_config.clicked.connect(self.show_configuration)
        sidebar_layout.addWidget(self.btn_config)
        
        # --- Main Content Area (Stacked Widget) ---
        self.main_stack = QStackedWidget()
        
        # --- Workspace Screen (Index 0) ---
        self.workspace_widget = QWidget()
        self.workspace_widget.setStyleSheet("background-color: #252526;")
        main_layout_inner = QVBoxLayout(self.workspace_widget)
        main_layout_inner.setContentsMargins(20, 20, 20, 20)
        
        header_label = QLabel("Project Workspace")
        header_label.setFont(QFont("Segoe UI", 14))
        header_label.setStyleSheet("color: white;")
        main_layout_inner.addWidget(header_label)
        
        # Timeline Table Editor
        self.timeline_table = QTableWidget()
        self.timeline_table.setColumnCount(3)
        self.timeline_table.setHorizontalHeaderLabels(["Start (s)", "End (s)", "Segment Text"])
        self.timeline_table.horizontalHeader().setStretchLastSection(True)
        self.timeline_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.timeline_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        
        self.timeline_table.setStyleSheet(
            "QTableWidget { background-color: #1e1e1e; color: white; border: 1px solid #333; gridline-color: #333; }"
            "QHeaderView::section { background-color: #2d2d30; color: white; padding: 4px; border: 1px solid #333; }"
            "QTableWidget::item:selected { background-color: #007acc; }"
        )
        main_layout_inner.addWidget(self.timeline_table)
        
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: #aaaaaa;")
        main_layout_inner.addWidget(self.status_label)
        
        self.main_stack.addWidget(self.workspace_widget)

        # --- Configuration Screen (Index 1) ---
        self.config_widget = QWidget()
        self.config_widget.setStyleSheet("background-color: #252526;")
        config_layout = QVBoxLayout(self.config_widget)
        config_layout.setContentsMargins(20, 20, 20, 20)

        config_header = QLabel("Configuration & Environment")
        config_header.setFont(QFont("Segoe UI", 14))
        config_header.setStyleSheet("color: white;")
        config_layout.addWidget(config_header)

        # API Keys Section
        api_frame = QFrame()
        api_frame.setStyleSheet("QFrame { background-color: #1e1e1e; border: 1px solid #333; border-radius: 5px; }")
        api_layout = QVBoxLayout(api_frame)
        
        api_label = QLabel("Integrations")
        api_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        api_label.setStyleSheet("color: white; border: none;")
        api_layout.addWidget(api_label)

        gemini_layout = QHBoxLayout()
        gemini_label = QLabel("Gemini API Key:")
        gemini_label.setStyleSheet("color: white; border: none;")
        self.gemini_input = QLineEdit()
        self.gemini_input.setEchoMode(QLineEdit.Password)
        self.gemini_input.setStyleSheet("background-color: #333; color: white; border: 1px solid #555; padding: 4px;")
        
        # Load existing key if any
        existing_key = self.settings.get("GEMINI_API_KEY", "")
        if existing_key:
            self.gemini_input.setText(existing_key)
            
        btn_save_key = QPushButton("Save")
        btn_save_key.setStyleSheet(self.btn_style(primary=True))
        btn_save_key.clicked.connect(self.save_api_key)
        
        gemini_layout.addWidget(gemini_label)
        gemini_layout.addWidget(self.gemini_input)
        gemini_layout.addWidget(btn_save_key)
        
        api_layout.addLayout(gemini_layout)
        
        api_desc = QLabel("<i>(Requires restart of transcription to take effect. If left blank, processing skips LLM refinement.)</i>")
        api_desc.setStyleSheet("color: #aaaaaa; border: none;")
        api_layout.addWidget(api_desc)

        config_layout.addWidget(api_frame)

        # Environment Status Area
        status_frame = QFrame()
        status_frame.setStyleSheet("QFrame { background-color: #1e1e1e; border: 1px solid #333; border-radius: 5px; }")
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(15, 15, 15, 15)
        status_layout.setSpacing(15)

        # FFmpeg Section
        self.ffmpeg_label = QLabel("FFmpeg Installed: Checking...")
        self.ffmpeg_label.setFont(QFont("Segoe UI", 11))
        self.ffmpeg_label.setStyleSheet("color: white; border: none;")
        status_layout.addWidget(self.ffmpeg_label)
        
        # Whisper Models Section
        self.models_label = QLabel("Whisper/PyTorch Models: Checking...")
        self.models_label.setFont(QFont("Segoe UI", 11))
        self.models_label.setStyleSheet("color: white; border: none;")
        status_layout.addWidget(self.models_label)

        models_disclaimer = QLabel("<i>(Note: Base models are automatically downloaded to your user cache folder on the first run of the app. This may take a while.)</i>")
        models_disclaimer.setStyleSheet("color: #aaaaaa; border: none;")
        models_disclaimer.setWordWrap(True)
        status_layout.addWidget(models_disclaimer)

        config_layout.addWidget(status_frame)
        
        # Refresh Config Button
        btn_refresh = QPushButton("Refresh Status")
        btn_refresh.setStyleSheet(self.btn_style(primary=True))
        btn_refresh.setMaximumWidth(150)
        btn_refresh.clicked.connect(self.refresh_environment_status)
        config_layout.addWidget(btn_refresh)

        config_layout.addStretch()

        self.main_stack.addWidget(self.config_widget)

        # --- Code / JSON View Screen (Index 2) ---
        self.code_widget = QWidget()
        self.code_widget.setStyleSheet("background-color: #252526;")
        code_layout = QVBoxLayout(self.code_widget)
        code_layout.setContentsMargins(20, 20, 20, 20)

        code_header_layout = QHBoxLayout()
        code_header = QLabel("Code / JSON View")
        code_header.setFont(QFont("Segoe UI", 14))
        code_header.setStyleSheet("color: white;")
        code_header_layout.addWidget(code_header)
        
        btn_export_from_code = QPushButton("Export from here...")
        btn_export_from_code.setStyleSheet(self.btn_style(primary=True))
        btn_export_from_code.clicked.connect(self.handle_export)
        code_header_layout.addWidget(btn_export_from_code)
        code_header_layout.addStretch()
        
        code_layout.addLayout(code_header_layout)

        self.json_text_edit = QTextEdit()
        self.json_text_edit.setReadOnly(True)
        self.json_text_edit.setStyleSheet(
            "QTextEdit { background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas, monospace; font-size: 13px; border: 1px solid #333; padding: 10px; }"
        )
        code_layout.addWidget(self.json_text_edit)
        
        self.main_stack.addWidget(self.code_widget)

        # Add to splitter
        splitter.addWidget(sidebar)
        splitter.addWidget(self.main_stack)
        
        # Set splitter proportions (approx 20% sidebar, 80% content)
        splitter.setSizes([200, 800])

    def btn_style(self, primary=False):
        bg_color = "#007acc" if primary else "#333333"
        hover_color = "#005f9e" if primary else "#444444"
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    def apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(37, 37, 38))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

    def show_configuration(self):
        self.main_stack.setCurrentIndex(1)
        self.refresh_environment_status()

    def show_code_view(self):
        # Update JSON view before showing
        if self.current_timeline_path and self.current_timeline_path.exists():
            try:
                with open(self.current_timeline_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                # Update text changes from workspace before showing JSON
                for row in range(self.timeline_table.rowCount()):
                    if row < len(data.get("segments", [])):
                        edited_text = self.timeline_table.item(row, 2).text()
                        data["segments"][row]["text"] = edited_text
                
                formatted_json = json.dumps(data, indent=2)
                self.json_text_edit.setText(formatted_json)
            except Exception as e:
                self.json_text_edit.setText(f"Error loading JSON: {e}")
        else:
            self.json_text_edit.setText("No timeline generated yet.")
            
        self.main_stack.setCurrentIndex(2)

    def refresh_environment_status(self):
        has_ffmpeg = EnvironmentChecker.check_ffmpeg()
        has_models = EnvironmentChecker.check_models_downloaded()

        # Update text with checkmarks
        if has_ffmpeg:
            self.ffmpeg_label.setText("✅ FFmpeg Installed and found in system PATH")
            self.ffmpeg_label.setStyleSheet("color: #4CAF50; border: none;") # Green
        else:
            self.ffmpeg_label.setText("❌ FFmpeg NOT found. Please install FFmpeg and add it to your system PATH.")
            self.ffmpeg_label.setStyleSheet("color: #F44336; border: none;") # Red

        if has_models:
            self.models_label.setText("✅ Whisper Base / PyTorch Models found in Cache")
            self.models_label.setStyleSheet("color: #4CAF50; border: none;")
        else:
            self.models_label.setText("❌ Models not found in cache (Will download automatically on first run)")
            self.models_label.setStyleSheet("color: #FFC107; border: none;") # Amber warning

    def save_api_key(self):
        key = self.gemini_input.text().strip()
        self.settings.set("GEMINI_API_KEY", key)
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Success", "API Key saved successfully.")

    def handle_new_project(self):
        name, ok = QInputDialog.getText(self, "New Project", "Enter Project Name:")
        if ok and name:
            # Let user choose parent directory
            parent_dir = QFileDialog.getExistingDirectory(
                self, 
                "Select Project Location", 
                str(self.pm.base_workspace_dir),
                QFileDialog.ShowDirsOnly
            )
            
            if parent_dir:
                try:
                    p_dir = self.pm.create_project(name, parent_dir=parent_dir)
                    self.status_label.setText(f"Status: Project '{name}' created at {p_dir}")
                    self.project_name_label.setText(f"Active Project:\n{name}")
                    self.project_name_label.setStyleSheet("color: #4CAF50; margin-bottom: 10px; font-weight: bold;")
                    self.btn_import_audio.setEnabled(True)
                    self.btn_export.setEnabled(False)
                    self.btn_code_view.setEnabled(False)
                    self.timeline_table.setRowCount(0)
                    self.current_timeline_path = None
                    self.setWindowTitle(f"CaptionLayer Workflow - {name}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not create project:\n{e}")

    def handle_import_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.m4a *.mp4)")
        if file_path:
            self.status_label.setText(f"Status: Selected {Path(file_path).name}")
            
            # Start Background worker
            self.btn_import_audio.setEnabled(False)
            self.worker = TranscriptionWorker(self.pm, self.settings, Path(file_path))
            self.worker.progress_signal.connect(self.update_status)
            self.worker.error_signal.connect(self.handle_error)
            self.worker.finished_signal.connect(self.handle_transcription_finished)
            self.worker.start()

    def update_status(self, text):
        self.status_label.setText(f"Status: {text}")

    def handle_error(self, err):
        self.btn_import_audio.setEnabled(True)
        QMessageBox.critical(self, "Processing Error", f"An error occurred:\n{err}")
        self.status_label.setText("Status: Error during processing")

    def handle_transcription_finished(self, timeline_path):
        self.btn_import_audio.setEnabled(True)
        self.btn_export.setEnabled(True)
        self.btn_code_view.setEnabled(True)
        self.current_timeline_path = Path(timeline_path)
        self.status_label.setText("Status: Transcription and Alignment complete.")

        # Load and display timeline segments
        self.timeline_table.setRowCount(0)
        try:
            with open(timeline_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            segments = data.get("segments", [])
            self.timeline_table.setRowCount(len(segments))
            
            for idx, seg in enumerate(segments):
                text = seg.get("text", "")
                start = seg.get("timing", {}).get("start", 0.0)
                end = seg.get("timing", {}).get("end", 0.0)
                
                # Start Time Item
                start_item = QTableWidgetItem(f"{start:.2f}")
                start_item.setFlags(start_item.flags() & ~Qt.ItemIsEditable) 
                self.timeline_table.setItem(idx, 0, start_item)
                
                # End Time Item
                end_item = QTableWidgetItem(f"{end:.2f}")
                end_item.setFlags(end_item.flags() & ~Qt.ItemIsEditable)
                self.timeline_table.setItem(idx, 1, end_item)
                
                # Text Item (Editable)
                text_item = QTableWidgetItem(text)
                self.timeline_table.setItem(idx, 2, text_item)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read timeline: {e}")

    def handle_export(self):
        if not self.current_timeline_path or not getattr(self.pm, 'current_project_dir', None):
            QMessageBox.warning(self, "Export", "No complete timeline to export.")
            return

        try:
            # Reconstruct CanonicalTimeline from the saved path
            with open(self.current_timeline_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            timeline = CanonicalTimeline(**data)
            
            # Update segments text with any edits made in the QTableWidget
            for row in range(self.timeline_table.rowCount()):
                if row < len(timeline.segments):
                    edited_text = self.timeline_table.item(row, 2).text()
                    timeline.segments[row].text = edited_text
            
            # Export to the project directory
            base_export_name = f"{timeline.project_metadata.name}_export"
            default_path = str(self.pm.current_project_dir / "exports" / base_export_name)
            
            export_path, selected_filter = QFileDialog.getSaveFileName(
                self, 
                "Export Subtitles",
                default_path,
                "All Formats (*.*);;JSON (*.json);;SubRip (*.srt);;WebVTT (*.vtt)"
            )
            
            if export_path:
                export_path_obj = Path(export_path)
                
                # Determine which exporter method to call based on filter
                if "JSON" in selected_filter:
                    self.exporter.export_json(timeline, export_path_obj.with_suffix('.json'))
                elif "SubRip" in selected_filter:
                    self.exporter.export_srt(timeline, export_path_obj.with_suffix('.srt'))
                elif "WebVTT" in selected_filter:
                    self.exporter.export_vtt(timeline, export_path_obj.with_suffix('.vtt'))
                else:
                    self.exporter.export_all(timeline, export_path_obj)

                QMessageBox.information(
                    self, 
                    "Export Successful", 
                    f"Successfully exported to:\n{export_path_obj.parent}"
                )
                
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export timeline: {e}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
