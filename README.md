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
    scheduler.add('first_job', lambda: 'success', 'cron', hour='00', minute='01')
    scheduler.add('second_job', lambda: 'success', 'interval', seconds=10)
    scheduler.remove('second_job')
    scheduler.print()
    
    scheduler.job_status('first_job')
    scheduler.job_result('first_job')
    scheduler.job_next_run_time('first_job')
    
    scheduler.shutdown()
    ```
    
## TODO

- Add database support.
- Add ```pause(id=None)```, ```resume(id=None)```.
- Disable logging for exceptions in jobs.
