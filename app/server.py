from multiprocessing import Process
import uvicorn
import time

from src.config.settings import settings

#run app as a separate process with uvicorn --reload
def run_server(host: str, port: int, reload: bool = True, wait: int = 15) -> Process:
    proc = Process(
        target=uvicorn.run,
        args=("app:app",),
        kwargs={
            "host": host,
            "port": port,
            "reload": reload,
        },
    )
    proc.start()
    time.sleep(wait)
    assert proc.is_alive()
    return proc

if __name__ == "__main__":
    proc = run_server(settings.HOST, settings.PORT, settings.DEBUG)