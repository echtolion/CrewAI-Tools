import requests
import json
import os
from langchain.tools import tool

class AssemblyAITools:
    
    def __init__(self, api_key, usage_file='transcription_usage.json'):
        self.api_key = api_key
        self.headers = {"Authorization": api_key}
        self.usage_file = usage_file
        self.total_hours_limit = 100  # Set the total hours limit for transcription usage.
    
    @tool("AudioTranscriber")
    def transcribe_audio(self, audio_url, **kwargs):
        """
        Transcribes audio to text using the AssemblyAI API. Supports additional parameters like speaker labels, 
        language code, etc., through **kwargs.
        
        Parameters:
            audio_url (str): URL of the audio file to transcribe.
            **kwargs: Additional parameters for the transcription request.

        Returns:
            dict: The response from the AssemblyAI API with transcription details or error information.
        """
        data = {"audio_url": audio_url, **kwargs}
        
        try:
            response = requests.post("https://api.assemblyai.com/v2/transcript", headers=self.headers, json=data)
            response.raise_for_status()  # This will raise an HTTPError if the response status code is 4XX or 5XX.
            transcript_response = response.json()

            if 'duration' in transcript_response:
                self.track_usage(transcript_response['duration'])
            return transcript_response

        except requests.HTTPError as e:
            return {"error": f"HTTP error occurred: {str(e)}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
    
    @tool("SpeakerIdentifier")
    def identify_speakers(self, transcript_id):
        """
        Identifies different speakers in a transcribed audio file. Requires a completed transcript ID.
        
        Parameters:
            transcript_id (str): The ID of the transcript to analyze for speaker identification.
        
        Returns:
            dict: The response from AssemblyAI with speaker identification details or error information.
        """
        url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        
        except requests.HTTPError as e:
            return {"error": f"HTTP error occurred: {str(e)}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    # The track_usage and find_highlights methods remain unchanged but should include similar error handling and documentation improvements.

    @tool("TranscriptionUsageTracker")
    def track_usage(self, audio_length_seconds):
        """
        Tracks and reports the cumulative transcription time used.
        - audio_length_seconds: Length of the audio file in seconds.
        """
        # Check if the usage file exists, otherwise initialize it
        if not os.path.exists(self.usage_file):
            with open(self.usage_file, 'w') as file:
                json.dump({"total_used_hours": 0}, file)
        
        # Load the current usage
        with open(self.usage_file, 'r') as file:
            usage_data = json.load(file)
        
        # Update the total used hours
        additional_hours = audio_length_seconds / 3600  # Convert seconds to hours
        usage_data["total_used_hours"] += additional_hours
        
        # Save the updated usage back to the file
        with open(self.usage_file, 'w') as file:
            json.dump(usage_data, file)
        
        # Calculate and report remaining hours
        remaining_hours = self.total_hours_limit - usage_data["total_used_hours"]
        print(f"Remaining transcription hours: {remaining_hours} out of {self.total_hours_limit}")
        
        return remaining_hours

    @tool("AudioHighlightFinder")
    def find_highlights(self, transcript_id):
        """
        Finds significant parts of an audio file based on the transcribed text. Requires a completed transcript ID.
        """
        # Utilize the 'auto_highlights' feature in the transcription request to enable this.
        # Then, parse the transcription result for highlighted sections.
