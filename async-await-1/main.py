# non_concurrent_async.py
import asyncio
import time

async def work(name: str, delay: float):
    print(f"{time.strftime('%X')}  start {name}")
   # await asyncio.sleep(delay)  # this yields, but nothing else is scheduled
   
    print(f"{time.strftime('%X')}  end   {name}")

async def main():
    t0 = time.perf_counter()

    # ❗ Sequential awaits: no concurrency here
    # for i in range(3):
    #     await work(f"job-{i}", 1.0)

    await asyncio.gather(*(work(f"job-{i}", 1.0) for i in range(3)))

    dt = time.perf_counter() - t0
    print(f"\nTotal elapsed ~ {dt:.2f}s (≈ number_of_jobs × 1s, so it's sequential)")

if __name__ == "__main__":
    asyncio.run(main())