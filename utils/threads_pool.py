from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

def run_threads_pool(func, tasks, max_workers):
    
    if max_workers <= 0:
        max_workers = 1

    res = []

    with ThreadPoolExecutor(max_workers = max_workers) as executor:
       
        futures = []

        for item in tasks:

            future = executor.submit(
                func,
                item
            )

            futures.append(future)

        for future in as_completed(futures):
            try:

                result = future.result()
                res.append(result)

            except Exception as e:
                res.append({"error":str(e)})
    return res

        