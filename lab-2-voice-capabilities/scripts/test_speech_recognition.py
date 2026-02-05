"""
Test script for speech recognition (STT)
Tests Azure Speech Service speech-to-text capabilities
"""
import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_handler import VoiceHandler


async def test_speech_recognition():
    """
    Interactive test for speech recognition
    """
    print("🎤 Speech Recognition Test")
    print("=" * 50)
    
    # Load configuration
    speech_key = os.getenv("AZURE_SPEECH_KEY", "")
    speech_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
    
    if not speech_key:
        print("❌ Error: AZURE_SPEECH_KEY not configured")
        print("Please set your Azure Speech Service key in .env file")
        return
    
    # Initialize voice handler
    print(f"Initializing voice handler (region: {speech_region})...")
    handler = VoiceHandler(
        speech_key=speech_key,
        speech_region=speech_region
    )
    
    print("\n✅ Voice handler initialized")
    print("\nThis test will recognize speech from your microphone.")
    print("Speak clearly and wait for the results.")
    print("\nNote: This requires Azure Speech Service to be properly configured.")
    print("\nPress Ctrl+C to stop\n")
    
    # Continuous recognition demo
    recognized_count = 0
    
    def on_recognized(text):
        nonlocal recognized_count
        if text.strip():
            recognized_count += 1
            print(f"\n> You said: \"{text}\"")
            
            if "stop" in text.lower() or "quit" in text.lower():
                print("\n✅ Stopping recognition...")
                return False
        return True
    
    try:
        print("🎤 Speak now... (say 'stop' to quit)")
        recognizer = handler.start_continuous_recognition(on_recognized)
        
        # Keep running until interrupted
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping...")
    finally:
        # Stop recognition
        if recognizer:
            recognizer.stop_continuous_recognition()
        
        print(f"\n📊 Test Summary:")
        print(f"   Recognized {recognized_count} speech inputs")
        print("\n✅ Test complete!")


def main():
    """Run the test"""
    try:
        asyncio.run(test_speech_recognition())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
