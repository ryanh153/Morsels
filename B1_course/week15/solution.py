import queue
import threading
from collections import defaultdict
from time import perf_counter
from typing import Dict, List, Tuple

import requests


def speed_test(urls: List[str], number_of_checks: int = 4) -> Dict[str, List[float]]:
    """Make a get request to each url in urls number_of_checks times and store the time for each in a dictionary
    urls: List of url strings
    number_of_checks: Number of times to make a get request to each url
    return: Dictionary whose keys are the url strings and whose values are lists of the time for each get request"""

    # set up return values and containers for threads and their results
    results = defaultdict(list)
    threads = list()
    thread_returns: queue.Queue[Tuple[str, float]] = queue.Queue()

    # start all threads
    for url in urls:
        for _ in range(number_of_checks):
            t = threading.Thread(target=time_request, args=(url, thread_returns))
            t.start()
            threads.append(t)

    # wait for all threads to finish
    for thread in threads:
        thread.join()

    # put run times for all requests into results dictionary
    while not thread_returns.empty():
        url, run_time = thread_returns.get()
        results[url].append(run_time)

    return results


def time_request(url: str, q: queue.Queue[Tuple[str, float]]) -> None:
    """Function for timing an http request and putting the result on a queue.Queue object"""
    start = perf_counter()
    requests.get(url)
    q.put((url, perf_counter()-start))
