from toolbox.tools import BaseTool
import os
import subprocess
import json
import requests
from typing import Dict, Any


class VideoMetadataExtractor(BaseTool):
    def name(self) -> str:
        return "video_metadata_extractor"

    def description(self) -> str:
        return "Extracts metadata from a video file using FFmpeg and the path of the folder is  /home/mayank/Documents/gen-aut/agent_lib/agents_hf/video/video.mp4"

    def execute(self, video_path: str) -> Dict:
        command = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            metadata = json.loads(result.stdout)
            return metadata
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFprobe error: {e.stderr}")