import importlib
import time
import unittest
import warnings
from unittest.mock import patch

import ratelimit


class RateLimitTests(unittest.TestCase):

    """Tests for ratelimit"""

    @classmethod
    def setUpClass(cls):
        """Monkey-patch the time module and then import ratelimit."""

        cls.clock = Clock()
        cls.patches = [
            patch('time.perf_counter', cls.clock),
            patch('time.sleep', cls.clock.increment),
        ]
        for p in cls.patches:
            p.start()
        warnings.simplefilter("ignore", ResourceWarning)
        importlib.reload(ratelimit)

    @classmethod
    def tearDownClass(cls):
        """Undo all our monkey-patching."""
        for p in cls.patches:
            p.stop()

    def tearDown(self):
        self.clock.reset()

    def test_just_one_call(self):
        @ratelimit.ratelimit(per_second=5)
        def add(x, y):
            return x + y
        self.assertEqual(add(2, 3), 5)

    def test_five_calls(self):
        @ratelimit.ratelimit(per_second=5)
        def subtract(x, y):
            return x - y
        self.assertEqual(subtract(2, 3), -1)
        self.assertEqual(subtract(x=1, y=1), 0)
        self.assertEqual(subtract(x=2, y=1), 1)
        self.assertEqual(subtract(6, y=3), 3)
        self.assertEqual(subtract(1, 3), -2)

    def test_sixth_call_raises_exception(self):
        @ratelimit.ratelimit(per_second=5)
        def subtract(x, y):
            return x - y
        self.assertEqual(subtract(2, 3), -1)
        self.assertEqual(subtract(x=1, y=1), 0)
        self.assertEqual(subtract(x=2, y=1), 1)
        self.assertEqual(subtract(6, y=3), 3)
        self.assertEqual(subtract(1, 3), -2)
        with self.assertRaises(Exception):
            subtract(5, 3)

    def test_slow_calls_work(self):
        @ratelimit.ratelimit(per_second=5)
        def subtract(x, y):
            time.sleep(0.201)
            return x - y
        self.assertEqual(subtract(2, 3), -1)
        self.assertEqual(subtract(x=1, y=1), 0)
        self.assertEqual(subtract(x=2, y=1), 1)
        self.assertEqual(subtract(6, y=3), 3)
        self.assertEqual(subtract(1, 3), -2)
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(9, 3), 6)

    def test_sleeping_works(self):
        @ratelimit.ratelimit(per_second=5)
        def subtract(x, y):
            return x - y
        self.assertEqual(subtract(2, 3), -1)
        self.assertEqual(subtract(x=1, y=1), 0)
        self.assertEqual(subtract(x=2, y=1), 1)
        self.assertEqual(subtract(6, y=3), 3)
        self.assertEqual(subtract(1, 3), -2)
        time.sleep(1)
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(9, 3), 6)

    def test_progressively_faster_calls(self):
        @ratelimit.ratelimit(per_second=5)
        def sleeping(seconds):
            time.sleep(seconds)
        sleeping(8)
        sleeping(4)
        sleeping(2)
        sleeping(1)
        sleeping(0.25)
        sleeping(0.25)
        sleeping(0.125)
        sleeping(0.0625)
        sleeping(0.03125)
        with self.assertRaises(Exception):
            sleeping(0.015625)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_sleep_argument(self):
        @ratelimit.ratelimit(per_second=5, sleep=True)
        def subtract(x, y):
            time.sleep(0.1)
            return x - y
        t1 = time.perf_counter()
        self.assertEqual(subtract(2, 3), -1)
        self.assertEqual(subtract(x=1, y=1), 0)
        self.assertEqual(subtract(x=2, y=1), 1)
        self.assertEqual(subtract(6, y=3), 3)
        t2 = time.perf_counter()
        self.assertEqual(subtract(1, 3), -2)
        t3 = time.perf_counter()
        self.assertEqual(subtract(5, 3), 2)
        t4 = time.perf_counter()
        self.assertEqual(subtract(9, 3), 6)
        t5 = time.perf_counter()
        self.assertLess(t2-t1, 1)
        self.assertLess(t3-t1, 1)
        self.assertGreaterEqual(t4-t1, 1)
        self.assertGreaterEqual(t5-t1, 1)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_thread_safety(self):
        from concurrent.futures import ThreadPoolExecutor
        import os.path
        import sys
        from tempfile import TemporaryDirectory
        sys.setswitchinterval(0.00000000000001)
        tmpdir = TemporaryDirectory()

        class SlowFalse:
            def __bool__(self):
                real_sleep(0.0001)
                return False

        @ratelimit.ratelimit(per_second=30, sleep=SlowFalse())
        def make_file(i):
            start = real_perf_counter()
            path = os.path.join(tmpdir.name, str(i) + ".txt")
            with open(path, mode='wt') as f:
                f.write(str(i))
            real_sleep(0.005)
            stop = real_perf_counter()
            return start, stop

        def do_it(i):
            try:
                return make_file(i)
            except Exception as e:
                return e

        pool = ThreadPoolExecutor(max_workers=50)
        results = pool.map(do_it, range(50))
        responses = list(results)
        successes = [r for r in responses if isinstance(r, tuple)]
        self.assertIn(len(successes), [29, 30, 31])  # Could be off by 1
        successes_by_start = sorted(successes, key=lambda time: time[0])
        prev_stop = 0
        concurrent = 0
        for start, stop in successes_by_start:
            if prev_stop > start:
                concurrent += 1
            prev_stop = stop
        self.assertGreater(concurrent, 0, "Threads didn't run concurrently")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_works_as_context_manager(self):
        five_per_second = ratelimit.ratelimit(per_second=5)
        with self.assertRaises(Exception):
            numbers = []
            for i in range(10):
                with five_per_second:
                    numbers.append(i)
        self.assertEqual(numbers, [0, 1, 2, 3, 4])
        three_per_second = ratelimit.ratelimit(per_second=3, sleep=True)
        numbers = []
        times = []
        start_time = time.perf_counter()
        for i in range(12):
            with three_per_second:
                numbers.append(i)
                times.append(round(time.perf_counter() - start_time))
        one_second_from_start = 1
        two_seconds_from_start = 2
        self.assertEqual(numbers, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.assertLessEqual(times[0], one_second_from_start)
        self.assertLessEqual(one_second_from_start, times[3])
        self.assertGreaterEqual(two_seconds_from_start, times[3])
        self.assertEqual(
            times,
            [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3],
            "3 per second",
        )


real_perf_counter = time.perf_counter


def real_sleep(duration):
    now = real_perf_counter()
    end = now + duration
    while now < end:
        now = real_perf_counter()


class Clock:

    """Fake version of time.perf_counter."""

    def __init__(self):
        self.bumps = []

    def __call__(self):
        return real_perf_counter() + sum(self.bumps)

    def reset(self):
        self.bumps.clear()

    def increment(self, count):
        self.bumps.append(count)


try:
    from ctypes import windll
except ImportError:
    pass  # We're not running on Windows
else:
    # Change timer resolution to 1 millisecond
    windll.winmm.timeBeginPeriod(1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
