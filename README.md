
# 🎙️ VLLM Audio Transcription Server

Quick show of a high-performance audio transcription service using VLLM with OpenAI Whisper models, designed for scalable speech-to-text processing


## 📋 Prerequisites

- NVIDIA driver supporting CUDA 12.8 (`nvidia-smi` should show CUDA 12.8 or higher). Used in the video  Driver Version: 575.64.03 and 580.82.09 CUDA Version: 12.9 (in nvidia-smi) https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/index.html#ubuntu
- Docker installed https://docs.docker.com/engine/install/ubuntu/?utm_source=chatgpt.com I used Docker version 28.3.3, build 980b856
- NVIDIA Container Toolkit https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
- VSCode or anything similar https://code.visualstudio.com/docs/setup/linux
- I use Linux  6.14.0-29-generic #29~24.04.1-Ubuntu x86_64 x86_64 x86_64 GNU/Linux https://ubuntu.com/download/desktop

## 🛠️ Quick Setup

### 1. Clone and Build

#### Creeate .env
```bash
nano .env 
paste
HUGGING_FACE_HUB_TOKEN=your_token_here
```

```bash
# Clone the repository
git clone <your-repo-url>
cd VLLM_transcription

# Build the Docker image and run in deatached mode

```bash
docker compose build & docker compose up -d
```

#### Create and activate a virtual environment to run code 

##### Bash shell

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai
```
The service will be available at `http://localhost:8002`

## 🏗️ Architecture

### Docker Configuration

**Dockerfile**:
```dockerfile
FROM vllm/vllm-openai:latest
RUN pip install vllm[audio]
```

This extends the official VLLM Server image with audio processing capabilities.

**Docker Compose**:
- **Port**: Maps container port 8000 to host port 8002
- **GPU**: Uses NVIDIA runtime for GPU acceleration  
- **Memory**: Configured for 41% GPU memory utilization. You need to adjust it for yourself
- **Model**: Uses `openai/whisper-large-v3-turbo` by default
- **Concurrency**: Set to handle 2 sequences simultaneously

### Key Parameters Explained

| Parameter | Value | Description |
|-----------|-------|-------------|
| `--gpu_memory_utilization` | 0.41 | Uses 41% of GPU memory (adjust based on your GPU) |
| `--model` | `openai/whisper-large-v3-turbo` | Fast, accurate Whisper model |
| `--task` | `transcription` | Specifies speech-to-text task |
| `--max-num-seqs` | 2 | Maximum concurrent sequences |


### cURL Example

```bash
curl -X POST "http://localhost:8002/v1/audio/transcriptions" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@input1.mp3" \
    -F "model=openai/whisper-large-v3-turbo" \
    -F "language=en" \
    -F "response_format=json"
```

#### Which audio to use?
Frequency
A sample rate of 16 kHz is typically sufficient for speech transcription, as it covers the core frequency range of human voice

Format Options

WAV (Uncompressed): Preserves all audio details, resulting in the highest transcription quality but with the largest file size.

FLAC (Lossless Compression): Reduces file size significantly without losing audio quality, maintaining optimal transcription potential.

MP3 (Lossy Compression): Discards some audio data to reduce size, which can lower transcription accuracy by introducing artifacts.

Channels

Check that your chosen audio format and channel configuration is supported by the transcription model. While mono (single-channel) audio is standard and widely supported, some advanced models and APIs allow multichannel transcription for speaker separation; however, channel count may affect accuracy and model compatibility.

Network Delay

Larger audio files—such as uncompressed WAV—may introduce delays when uploading or streaming over networks. If bandwidth is a concern, consider FLAC for lossless compression to balance quality and transfer speed.

#### Simple Batch Processing Alternative

For basic batch processing without format conversion, use `async_transcribe.py`:

## 🔧 Performance Tuning

### GPU Memory Optimization

Adjust `--gpu_memory_utilization` based on your GPU:

- **8GB GPU**: 0.3-0.4 (30-40%)
- **12GB GPU**: 0.4-0.6 (40-60%)  
- **24GB+ GPU**: 0.6-0.8 (60-80%)

### Model Selection

Available models (fastest to most accurate):

1. `openai/whisper-base` - Fastest, less accurate
2. `openai/whisper-small` - Good balance
3. `openai/whisper-medium` - Better accuracy
4. `openai/whisper-large-v3-turbo` - Best speed/accuracy balance
5. `openai/whisper-large-v3` - Highest accuracy

### Health Check

```bash
# Test if service is responding
curl http://localhost:8002/health

# Check model info
curl http://localhost:8002/v1/models
```

## 📚 References

- [VLLM Documentation](https://docs.vllm.ai/en/stable/)
- [VLLM Issue #2492](https://github.com/vllm-project/vllm/issues/2492) - Audio configuration reference
- [VLLM Optimization Guide](https://docs.vllm.ai/en/stable/configuration/optimization.html)
- [OpenAI Audio API](https://platform.openai.com/docs/api-reference/audio)

## 📄 License

[Add your license here]
