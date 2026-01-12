from live_audio_capture import LiveAudioCapture

# Initialize the audio capture
capture = LiveAudioCapture(
    sampling_rate=16000,  # Sample rate in Hz
    chunk_duration=0.1,   # Duration of each audio chunk in seconds
    enable_noise_canceling=True,  # Enable noise reduction
    aggressiveness=2,     # VAD aggressiveness level (0-3)
)

# Start recording with VAD
capture.listen_and_record_with_vad(
    output_file="output.wav",  # Save the recording to this file
    silence_duration=2.0,      # Stop recording after 2 seconds of silence
    format="wav",              # Output format
)

# Stop the capture
capture.stop()