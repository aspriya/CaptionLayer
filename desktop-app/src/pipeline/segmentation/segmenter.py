import uuid
from typing import List, Optional
from src.domain.schemas.timeline import CanonicalTimeline, Segment, Word, Timing, SegmentStyle

class RuleBasedSegmenter:
    """
    Applies deterministic rules to group Word objects into display-friendly segments (captions).
    """
    
    def __init__(self, max_words: int = 6, max_chars: int = 40):
        self.max_words = max_words
        self.max_chars = max_chars
        # Punctuation to aggressively split on
        self.split_punctuation = {'.', '!', '?', ';' , ':'}
        
    def process(self, timeline: CanonicalTimeline) -> CanonicalTimeline:
        """
        Takes a CanonicalTimeline directly from ASR/Alignment, strips the words out 
        of the long segments, and reshuffles them into chunked read-friendly segments.
        """
        # Flatten all words from the current segments
        all_words: List[Word] = []
        for seg in timeline.segments:
            all_words.extend(seg.words)
            
        if not all_words:
            return timeline
            
        new_segments: List[Segment] = []
        
        current_chunk: List[Word] = []
        current_char_count = 0
        
        for w in all_words:
            current_chunk.append(w)
            current_char_count += len(w.text) + 1 # +1 for space approx
            
            # Check rules for splitting
            hit_max_words = len(current_chunk) >= self.max_words
            hit_max_chars = current_char_count >= self.max_chars
            hit_punctuation = any(p in w.text for p in self.split_punctuation)
            
            if hit_max_words or hit_max_chars or hit_punctuation:
                new_segments.append(self._build_segment(current_chunk))
                current_chunk = []
                current_char_count = 0
                
        # Catch any trailing words
        if current_chunk:
            new_segments.append(self._build_segment(current_chunk))
            
        # Update timeline state
        timeline.segments = new_segments
        timeline.provenance.segmentation_method = "rule_based_chunking"
        
        return timeline
        
    def _build_segment(self, words: List[Word]) -> Segment:
        """Helper to create a unified Segment from a list of Words."""
        start_time = words[0].timing.start
        end_time = words[-1].timing.end
        
        return Segment(
            id=str(uuid.uuid4()),
            text=" ".join(w.text for w in words),
            words=words,
            timing=Timing(
                start=start_time,
                end=end_time,
                duration=round(end_time - start_time, 3)
            ),
            style=SegmentStyle()
        )
