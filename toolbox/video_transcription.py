from tools import BaseTool
import os
import subprocess
import json
import requests
from typing import Dict, Any
import time

class VideoTranscriptionTool(BaseTool):
    def name(self) -> str:
        return "video_transcription_tool"

    def description(self) -> str:
        return "Transcribes video audio using AssemblyAI."

    def execute(self, upload_url: str) -> str:
        headers = {"authorization": os.getenv("ASSEMBLYAI_API_KEY")}
        response = requests.post("https://api.assemblyai.com/v2/transcript", headers=headers, json={"audio_url": upload_url})
        response.raise_for_status()
        transcript_id = response.json()["id"]
        return self._poll_transcription_result(transcript_id)

    def _poll_transcription_result(self, transcript_id: str) -> str:
        headers = {"authorization": os.getenv("ASSEMBLYAI_API_KEY")}
        polling_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        while True:
            response = requests.get(polling_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            if result["status"] == "completed":
                return result["text"]
            elif result["status"] == "failed":
                raise RuntimeError(f"Transcription failed: {result['error']}")
            time.sleep(5)