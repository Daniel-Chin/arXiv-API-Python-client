import typing as tp
from os import path
from datetime import datetime
from zoneinfo import ZoneInfo
import shelve
from contextlib import contextmanager
import threading

from platformdirs import user_cache_dir

APP_NAME = "arxiv_api_client"

CACHE_DIR = user_cache_dir(APP_NAME)

CACHE_DATE = 'CACHE_DATE'

def getNYTime():
    return datetime.now(ZoneInfo("America/New_York"))

@contextmanager
def Cache(
    getNYTime: tp.Callable[[], datetime] = getNYTime, 
):
    with shelve.open(path.join(CACHE_DIR, 'cache')) as shelf:
        thread: threading.Thread | None = None
        lock = threading.Lock()

        def getToday():
            return str(getNYTime().date())

        def clear():
            nonlocal thread
            shelf.clear()
            shelf[CACHE_DATE] = getToday()
            thread = None

        def invalidate():
            nonlocal thread
            if thread is not None:
                return
            try:
                cache_date: str = shelf[CACHE_DATE]
            except KeyError:
                need_purge = True
            else:
                need_purge = cache_date != getToday()
            if need_purge:
                thread = threading.Thread(target=clear)
                thread.start()
        
        def get(key: str):
            with lock:
                invalidate()
                if thread is not None:
                    raise KeyError('Cache purge in progress')
                return shelf[key]
        
        def set_(key: str, value, timeout: float = 0.1):
            with lock:
                assert key != CACHE_DATE
                invalidate()
                if thread is not None:
                    try:
                        thread.join(timeout)
                    except TimeoutError:
                        return  # silently give up the set. Slight inefficiency but safe.
                    else:
                        assert thread is None
                shelf[key] = value
        
        try:
            yield get, set_
        finally:
            t_ = thread
            if t_ is not None:
                t_.join()

def test():
    '''
    A single-thread unit test.  
    '''
    t = datetime.now()
    def getFakeTime():
        return t
    
    with Cache(
        getFakeTime,    # dependency injection
    ) as (getCache, setCache):
        setCache('a', 1)
        assert getCache('a') == 1
        try:
            getCache('b')
        except KeyError:
            pass
        else:
            assert False
        t = t.replace(year=t.year + 1)
        try:
            getCache('a')
        except KeyError:
            pass
        else:
            assert False

if __name__ == "__main__":
    test()
