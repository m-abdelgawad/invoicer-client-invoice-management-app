import asyncio
import aiohttp


async def send_request(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status
    except Exception as e:
        return str(e)


async def load_test(url, requests_per_second, test_duration):
    total_requests = 0
    success_count = 0
    failure_count = 0

    start_time = time.time()

    while time.time() - start_time < test_duration:
        tasks = []
        for _ in range(requests_per_second):
            tasks.append(send_request(url))

        responses = await asyncio.gather(*tasks)

        total_requests += len(responses)
        success_count += responses.count(200)  # Assuming HTTP status code 200 for success
        failure_count += len(responses) - responses.count(200)

        # Delay to achieve the specified requests per second rate
        await asyncio.sleep(1 / requests_per_second)

    return total_requests, success_count, failure_count


if __name__ == "__main__":
    import time

    url = input("Enter the URL to test: ")
    requests_per_second = int(input("Enter requests per second: "))
    test_duration = int(input("Enter test duration in seconds: "))

    loop = asyncio.get_event_loop()
    total_requests, success_count, failure_count = loop.run_until_complete(
        load_test(url, requests_per_second, test_duration))

    print(f"Total Requests: {total_requests}")
    print(f"Successful Requests: {success_count}")
    print(f"Failed Requests: {failure_count}")
    print(f"Success Rate: {success_count / total_requests * 100:.2f}%")

    loop.close()
