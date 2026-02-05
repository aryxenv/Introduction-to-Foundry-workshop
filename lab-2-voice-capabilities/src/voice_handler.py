"""
Voice Handler for Speech Services
Handles speech-to-text and text-to-speech operations using Azure Speech Services
"""
import os
import logging
from typing import Optional, AsyncIterator
import azure.cognitiveservices.speech as speechsdk
from pathlib import Path

logger = logging.getLogger(__name__)


class VoiceHandler:
    """
    Handles voice interactions using Azure Speech Services
    
    Provides speech-to-text (STT) and text-to-speech (TTS) capabilities
    """
    
    def __init__(
        self,
        speech_key: str,
        speech_region: str,
        stt_language: str = "en-US",
        tts_voice: str = "en-US-JennyNeural"
    ):
        """
        Initialize voice handler
        
        Args:
            speech_key: Azure Speech Service API key
            speech_region: Azure region (e.g., 'eastus')
            stt_language: Language for speech recognition
            tts_voice: Voice name for speech synthesis
        """
        self.speech_key = speech_key
        self.speech_region = speech_region
        self.stt_language = stt_language
        self.tts_voice = tts_voice
        
        # Create speech config
        self.speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )
        
        # Configure STT
        self.speech_config.speech_recognition_language = stt_language
        
        # Configure TTS
        self.speech_config.speech_synthesis_voice_name = tts_voice
        
        logger.info(f"VoiceHandler initialized with voice: {tts_voice}")
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            # Create audio config from file
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
            
            # Create speech recognizer
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Perform recognition
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                logger.info(f"Transcribed: {result.text}")
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                logger.warning("No speech recognized")
                return ""
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"Recognition canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Error details: {cancellation.error_details}")
                return ""
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise
    
    async def synthesize_speech(
        self,
        text: str,
        output_file: Optional[str] = None
    ) -> bytes:
        """
        Convert text to speech
        
        Args:
            text: Text to convert to speech
            output_file: Optional file path to save audio
            
        Returns:
            Audio data as bytes
        """
        try:
            # Create audio config
            if output_file:
                audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            else:
                audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
            
            # Create speech synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Synthesize speech
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"Speech synthesized for text: {text[:50]}...")
                return result.audio_data
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"Synthesis canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Error details: {cancellation.error_details}")
                raise Exception("Speech synthesis failed")
                
        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            raise
    
    async def synthesize_with_ssml(
        self,
        ssml: str,
        output_file: Optional[str] = None
    ) -> bytes:
        """
        Convert SSML to speech for advanced control
        
        Args:
            ssml: SSML markup text
            output_file: Optional file path to save audio
            
        Returns:
            Audio data as bytes
        """
        try:
            # Create audio config
            if output_file:
                audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            else:
                audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
            
            # Create speech synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Synthesize from SSML
            result = synthesizer.speak_ssml_async(ssml).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info("SSML speech synthesized successfully")
                return result.audio_data
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"SSML synthesis canceled: {cancellation.reason}")
                raise Exception("SSML speech synthesis failed")
                
        except Exception as e:
            logger.error(f"Error synthesizing SSML: {e}")
            raise
    
    def start_continuous_recognition(self, callback):
        """
        Start continuous speech recognition
        
        Args:
            callback: Function to call with recognized text
        """
        # Create audio config from microphone
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        
        # Create speech recognizer
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        
        # Connect callbacks
        recognizer.recognized.connect(lambda evt: callback(evt.result.text))
        
        # Start continuous recognition
        recognizer.start_continuous_recognition()
        
        logger.info("Continuous recognition started")
        return recognizer


def demo():
    """
    Demonstrates voice handler capabilities
    
    This requires proper Azure Speech Service configuration
    """
    # Load configuration
    speech_key = os.getenv("AZURE_SPEECH_KEY", "")
    speech_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
    
    if not speech_key:
        print("⚠️  AZURE_SPEECH_KEY not configured")
        return
    
    # Initialize handler
    handler = VoiceHandler(
        speech_key=speech_key,
        speech_region=speech_region
    )
    
    print("🎤 Voice Handler Demo")
    print("This demonstrates the voice handler capabilities")
    print("\nNote: Requires Azure Speech Service to be configured")


if __name__ == "__main__":
    demo()
