"""
Test script for speech synthesis (TTS)
Tests Azure Speech Service text-to-speech capabilities
"""
import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_handler import VoiceHandler


async def test_speech_synthesis():
    """
    Interactive test for speech synthesis
    """
    print("🔊 Speech Synthesis Test")
    print("=" * 50)
    
    # Load configuration
    speech_key = os.getenv("AZURE_SPEECH_KEY", "")
    speech_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
    tts_voice = os.getenv("TTS_VOICE_NAME", "en-US-JennyNeural")
    
    if not speech_key:
        print("❌ Error: AZURE_SPEECH_KEY not configured")
        print("Please set your Azure Speech Service key in .env file")
        return
    
    # Initialize voice handler
    print(f"Initializing voice handler...")
    print(f"  Region: {speech_region}")
    print(f"  Voice: {tts_voice}")
    
    handler = VoiceHandler(
        speech_key=speech_key,
        speech_region=speech_region,
        tts_voice=tts_voice
    )
    
    print("\n✅ Voice handler initialized")
    print("\nEnter text to speak (or 'quit' to exit):")
    print("-" * 50)
    
    synthesis_count = 0
    
    while True:
        try:
            # Get user input
            text = input("\n> ")
            
            if not text or text.lower() in ['quit', 'exit', 'q']:
                break
            
            # Synthesize speech
            print(f"🔊 Synthesizing: \"{text}\"...")
            
            try:
                audio_data = await handler.synthesize_speech(text)
                synthesis_count += 1
                print("✅ Speech synthesis complete")
                print(f"   Audio data size: {len(audio_data)} bytes")
                
            except Exception as e:
                print(f"❌ Error synthesizing speech: {e}")
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopping...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n📊 Test Summary:")
    print(f"   Synthesized {synthesis_count} speech outputs")
    print("\n✅ Test complete!")


def main():
    """Run the test"""
    try:
        asyncio.run(test_speech_synthesis())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
