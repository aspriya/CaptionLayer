from typing import Dict, Any, List
import uuid
import datetime

from src.domain.schemas.timeline import (
    CanonicalTimeline, ProjectMetadata, SourceAssetMetadata, 
    ProcessingProvenance, Segment, Word, Timing, WordStyle, SegmentStyle
)

def whisperx_to_canonical(
    project_id: str,
    project_name: str,
    audio_filename: str,
    whisperx_result: Dict[str, Any]
) -> CanonicalTimeline:
    """
    Transforms WhisperX result dictionary into the Canonical Timeline schema.
    """
    segments: List[Segment] = []
    full_transcript_parts = []
    
    for w_seg in whisperx_result.get("segments", []):
        seg_text = w_seg.get("text", "").strip()
        full_transcript_parts.append(seg_text)
        
        words: List[Word] = []
        for w_dict in w_seg.get("words", []):
            if "start" not in w_dict or "end" not in w_dict:
                # Sometimes alignment fails for silent or overlapping words, giving no timing. 
                # We skip or approximate, but standard strict alignment requires timings.
                continue
                
            word_start = w_dict["start"]
            word_end = w_dict["end"]
            words.append(
                Word(
                    text=w_dict["word"],
                    timing=Timing(
                        start=word_start,
                        end=word_end,
                        duration=round(word_end - word_start, 3)
                    ),
                    confidence=w_dict.get("score"),
                    style=WordStyle()
                )
            )

        # Fallback for segment start/end if words array is empty or partial
        seg_start = w_seg.get("start", 0.0)
        seg_end = w_seg.get("end", 0.0)
        
        if words:
            seg_start = words[0].timing.start
            seg_end = words[-1].timing.end

        segments.append(
            Segment(
                id=str(uuid.uuid4()),
                text=seg_text,
                words=words,
                timing=Timing(
                    start=seg_start,
                    end=seg_end,
                    duration=round(seg_end - seg_start, 3)
                ),
                style=SegmentStyle()
            )
        )

    return CanonicalTimeline(
        project_metadata=ProjectMetadata(
            project_id=project_id,
            name=project_name
        ),
        source_metadata=SourceAssetMetadata(
            filename=audio_filename
        ),
        transcript=" ".join(full_transcript_parts),
        segments=segments,
        provenance=ProcessingProvenance(
            asr_model="whisperx",
            alignment_model="whisperx"
        )
    )
