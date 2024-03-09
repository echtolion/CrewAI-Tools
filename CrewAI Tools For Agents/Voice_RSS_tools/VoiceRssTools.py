from langchain.tools import tool
import os
import requests

@tool("VoiceRSS_TTS", return_direct=False)
def voice_rss_text_to_speech(text: str, lang: str = "en-us", voice: str = "Linda", rate: int = 0, format: str = "mp3", ssml: str = "false", base64: str = "false") -> bytes:
    """
    Converts text to speech using the VoiceRSS API. Retrieves the API key from an environment variable.
    
    Parameters:
    - text (str): The text to be converted to speech.
    - lang (str, optional): The language code (default "en-us").
    - voice (str, optional): The voice selection (default "Linda").
    - rate (int, optional): The speech rate (default 0).
    - format (str, optional): The audio format (default "mp3").
    - ssml (str, optional): Specifies if the input text is SSML (default "false").
    - base64 (str, optional): Specifies if the output should be in Base64 encoding (default "false").

    Returns:
    - bytes: The speech audio content in binary format, or a Base64 encoded string if base64 is "true".
    """
    # Reads the API key from an environment variable
    api_key = os.getenv('Voice_RSS_API_KEY')
    if not api_key:
        raise ValueError("Voice_RSS_API_KEY environment variable not set.")
    
    base_url = "https://api.voicerss.org/"
    params = {
        'key': api_key,
        'src': text,
        'hl': lang,
        'v': voice,
        'r': rate,
        'c': format,
        'f': '44khz_16bit_stereo',
        'ssml': ssml,
        'b64': base64
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        if base64 == "false":
            # Return binary content
            return response.content
        else:
            # Return Base64 string
            return response.text
    else:
        raise Exception("Error: " + response.text)
    
@tool("VoiceRSS_TTS_Chunks", return_direct=False)
def voice_rss_tts_chunks(text: str, lang: str = "en-us", voice: str = "Linda", rate: int = 0, format: str = "mp3", ssml: str = "false", base64: str = "false") -> list:
    """
    Converts longer texts to speech by splitting into chunks and processing each with VoiceRSS API.
    
    Parameters are similar to the voice_rss_text_to_speech function.
    
    Returns a list of speech audio content for each chunk.
    """
    api_key = os.getenv('Voice_RSS_API_KEY')
    base_url = "https://api.voicerss.org/"
    chunk_size = 500  # Example chunk size, adjust based on testing and requirements
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    audio_contents = []

    for chunk in chunks:
        params = {
            'key': api_key,
            'src': chunk,
            'hl': lang,
            'v': voice,
            'r': rate,
            'c': format,
            'f': '44khz_16bit_stereo',
            'ssml': ssml,
            'b64': base64
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            audio_contents.append(response.content if base64 == "false" else response.text)
        else:
            raise Exception("Error processing chunk: " + response.text)

    return audio_contents