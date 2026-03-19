# Phase 5: UX Improvements & Advanced Export Implementation Log

## Overview
In Phase 5, we addressed user feedback regarding project management, workspace layout, and export flows. We made it possible to specify exact save locations per project, drastically improved currently active project visibility, enabled advanced multi-format subtitle exports natively, and implemented a brand new raw JSON viewer right in the app.

## What We Did
1. **Directory Targeting (`src/infrastructure/storage/project_manager.py`)**: 
   - Refactored `create_project` to accept a custom `parent_dir` argument, overriding the hardcoded `C:\Users\...\CaptionLayerProjects` pathway. It now natively defaults to whichever folder the user picks via the File Dialog.
   
2. **Project Visibility & Layout (`src/ui/windows/main_window.py`)**:
   - Injected a new prominent `project_name_label` in the sidebar directly beneath the Application Title.
   - Updated the main `QMainWindow.setWindowTitle` to dynamically bind to `{App Name} - {Active Project}`.
   
3. **Advanced Export Parsing (`src/ui/windows/main_window.py`)**:
   - Refactored the `QFileDialog.getSaveFileName` usage within `handle_export` to return both the chosen path *and* the `selected_filter`. 
   - Wired the filter string evaluation natively into `TimelineExporter`'s dedicated sub-methods (`export_srt()`, `export_vtt()`, `export_json()`) avoiding blindly exporting *all* formats when a user specifically just wants a single `.srt` iteration.

4. **Code / JSON View Implementation (`src/ui/windows/main_window.py`)**:
   - Expanded the `QStackedWidget` to include a 3rd panel (`self.code_widget`).
   - Wired a read-only `QTextEdit` that parses the actively loaded `CanonicalTimeline` via standard json dumping (`json.dumps()`), injecting the real-time content back to the UI.
   - Built a hook into the `show_code_view` function that iterates through the active UI `QTableWidget` to save any uncommitted typed string changes before dropping it into the JSON view, ensuring the JSON accurately reflects user corrections right before export.

## Difficulties & Complexities
1. **PySide6 Native Formatting Defaults:** The most significant UI issue involved matching the user's workspace UI edits with strictly dumping the base file JSON layout. Because users can change the text within the `QTableWidget` natively, that state is decoupled from the `CanonicalTimeline` backing variable. We had to ensure that clicking "Code / JSON View" loops through the QTableWidget, patches any changes back into the internal Python dictionary state, and explicitly dumps *that* freshly state-aligned model back to the newly rendered UI string buffer.

## Learnings for Future Phases
- PySide6 maintains state beautifully as long as UI objects are correctly updated ahead of function callbacks. 
- While our exporter handles individual types gracefully now based on file dialog filters, Phase 6 or 7 could further streamline this process with checkboxes or multiselect models, decoupling native export pathways further from basic Windows File Dialog string parsing.