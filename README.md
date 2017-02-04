# easy-scheduler

Lightly encapsulated APScheduler for easier use.

## Features

- Job excecution result and status quering supported

## Getting Started

- Installation

    ```pip install https://github.com/jxltom/easy-scheduler/archive/master.zip```

- Usage

    ```python
    from easy_scheduler.scheduler import Scheduler
    
    scheduler = Scheduler(timezone='Asia/Hong_Kong')
    scheduler.start()
    scheduler.add()
    scheduler.add()
    scheduler.remove()
    scheduler.print()
    
    scheduler.job_status()
    scheduler.job_result()
    scheduler.job_next_run_time()
    
    scheduler.shutdown()
    ```
    
## TODO

- Add database support.
- Add ```pause(id=None)```, ```resume(id=None)```.
- Disable logging for exceptions in jobs.
