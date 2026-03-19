import json
import logging
from pathlib import Path
from typing import List

from ...domain.schemas.timeline import CanonicalTimeline

logger = logging.getLogger(__name__)

class TimelineExporter:
    """Exports CanonicalTimeline to various subtitle formats."""
    
    @staticmethod
    def _format_timestamp_srt(seconds: float) -> str:
        """Format seconds to SRT timestamp: HH:MM:SS,mmm"""
        ms = int((seconds % 1) * 1000)
        s = int(seconds)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    @staticmethod
    def _format_timestamp_vtt(seconds: float) -> str:
        """Format seconds to VTT timestamp: HH:MM:SS.mmm"""
        ms = int((seconds % 1) * 1000)
        s = int(seconds)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
    
    def export_all(self, timeline: CanonicalTimeline, base_output_path: Path):
        """Export the timeline to all supported formats."""
        self.export_json(timeline, base_output_path.with_suffix(".json"))
        self.export_srt(timeline, base_output_path.with_suffix(".srt"))
        self.export_vtt(timeline, base_output_path.with_suffix(".vtt"))
    
    def export_json(self, timeline: CanonicalTimeline, output_path: Path):
        """Export timeline to canonical JSON format."""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(timeline.model_dump_json(indent=2))
        logger.info(f"Exported JSON to {output_path}")

    def export_srt(self, timeline: CanonicalTimeline, output_path: Path):
        """Export timeline to SubRip (.srt) format."""
        lines = []
        for index, segment in enumerate(timeline.segments, start=1):
            start_str = self._format_timestamp_srt(segment.timing.start)
            end_str = self._format_timestamp_srt(segment.timing.end)
            lines.append(f"{index}")
            lines.append(f"{start_str} --> {end_str}")
            lines.append(segment.text)
            lines.append("")
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        logger.info(f"Exported SRT to {output_path}")

    def export_vtt(self, timeline: CanonicalTimeline, output_path: Path):
        """Export timeline to WebVTT (.vtt) format."""
        lines = ["WEBVTT", ""]
        for index, segment in enumerate(timeline.segments, start=1):
            start_str = self._format_timestamp_vtt(segment.timing.start)
            end_str = self._format_timestamp_vtt(segment.timing.end)
            lines.append(f"{index}")
            lines.append(f"{start_str} --> {end_str}")
            lines.append(segment.text)
            lines.append("")
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        logger.info(f"Exported VTT to {output_path}")
