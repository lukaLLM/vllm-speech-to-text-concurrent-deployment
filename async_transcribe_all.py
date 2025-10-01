import asyncio
import time
from pathlib import Path
from openai import AsyncOpenAI

async def transcribe_once(client, audio_path, idx):
    start = time.perf_counter()
    with open(audio_path, "rb") as f:
        result = await client.audio.transcriptions.create(
            file=f,
            model="openai/whisper-large-v3-turbo",
            language="en",
            response_format="json",
            temperature=0.0,
        )
    elapsed = (time.perf_counter() - start) * 1000  # ms
    return idx, elapsed, result.text

async def transcribe_all_files():
    client = AsyncOpenAI(
        api_key="EMPTY",
        base_url="http://localhost:8002/v1",
    )

    current_dir = Path.cwd()
    format = "wav"
    audio_files = list(current_dir.glob(f"*.{format}"))

    if not audio_files:
        print(f"❌ No {format} files found in the current directory.")
        return

    print(f"📁 Found {len(audio_files)} {format} files in {current_dir}")

    tasks = [transcribe_once(client, str(audio_file), i + 1) for i, audio_file in enumerate(audio_files)]
    results = await asyncio.gather(*tasks)

    times = [t for _, t, _ in results]
    print("\nTranscriptions:")
    for idx, t, text in results:
        print(f"Request {idx}: {t:.2f} ms\n{text}\n{'-'*40}")
    print(f"Average time: {sum(times)/len(times):.2f} ms")
    print(f"Longest time: {max(times):.2f} ms")

if __name__ == "__main__":
    asyncio.run(transcribe_all_files())