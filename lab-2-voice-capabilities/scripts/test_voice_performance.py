"""
Performance test for voice capabilities
Tests latency and throughput of speech services
"""
import os
import sys
import asyncio
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_handler import VoiceHandler


async def test_tts_performance(handler: VoiceHandler, num_tests: int = 5):
    """
    Test text-to-speech performance
    
    Args:
        handler: VoiceHandler instance
        num_tests: Number of test iterations
        
    Returns:
        Average latency in seconds
    """
    test_texts = [
        "Hello, how can I help you today?",
        "The quick brown fox jumps over the lazy dog.",
        "This is a test of the text-to-speech system.",
        "Welcome to our voice-enabled chatbot.",
        "Thank you for using our service."
    ]
    
    print(f"\n🔊 Testing TTS performance ({num_tests} iterations)...")
    latencies = []
    
    for i in range(num_tests):
        text = test_texts[i % len(test_texts)]
        
        start_time = time.time()
        try:
            await handler.synthesize_speech(text)
            latency = time.time() - start_time
            latencies.append(latency)
            print(f"  Test {i+1}/{num_tests}: {latency:.3f}s")
        except Exception as e:
            print(f"  Test {i+1}/{num_tests}: Failed - {e}")
    
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        
        print(f"\n📊 TTS Results:")
        print(f"   Average: {avg_latency:.3f}s")
        print(f"   Min: {min_latency:.3f}s")
        print(f"   Max: {max_latency:.3f}s")
        
        return avg_latency
    
    return 0.0


async def test_voice_performance():
    """
    Run performance tests for voice capabilities
    """
    print("⚡ Voice Performance Test")
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
    
    print("✅ Voice handler initialized\n")
    
    # Test TTS performance
    tts_avg = await test_tts_performance(handler, num_tests=5)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Performance Summary")
    print("=" * 50)
    print(f"Text-to-Speech Average Latency: {tts_avg:.3f}s")
    
    # Evaluation
    print("\n🎯 Target Latencies:")
    print("   TTS: < 1.0s (Good), < 2.0s (Acceptable)")
    
    if tts_avg < 1.0:
        print("   ✅ TTS performance: Excellent")
    elif tts_avg < 2.0:
        print("   ✅ TTS performance: Good")
    else:
        print("   ⚠️  TTS performance: Could be improved")
    
    print("\n✅ Performance test complete!")


def main():
    """Run the performance test"""
    try:
        asyncio.run(test_voice_performance())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
