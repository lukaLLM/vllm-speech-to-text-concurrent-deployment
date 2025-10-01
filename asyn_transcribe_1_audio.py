import asyncio
import time
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

async def main():
    client = AsyncOpenAI(
        api_key="EMPTY",
        base_url="http://localhost:8002/v1",
    )
    audio_path = "input1.wav"
    num_requests = 1
    tasks = [transcribe_once(client, audio_path, i+1) for i in range(num_requests)]
    results = await asyncio.gather(*tasks)
    times = [t for _, t, _ in results]
    print("\nTranscriptions:")
    for idx, t, text in results:
        print(f"Request {idx}: {t:.2f} ms\n{text}\n{'-'*40}")
    print(f"Average time: {sum(times)/len(times):.2f} ms")
    print(f"Longest time: {max(times):.2f} ms")

if __name__ == "__main__":
    asyncio.run(main())
