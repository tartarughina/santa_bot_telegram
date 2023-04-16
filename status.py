import time
from typing import Tuple

class Status:
    def __init__(self) -> None:
        self.running: bool = True
        self.start_time: float = time.time()
        self.last_restart: float = None
        self.last_stop: float = None
    

    def stop(self) -> None:
        self.running = False
        self.last_stop = time.time()


    def restart(self) -> None:
        self.running = True
        self.last_restart = time.time()

    
    def get_status(self) -> Tuple[bool, float, float, float]:
        return (self.running, self.start_time, self.last_stop, self.last_restart)