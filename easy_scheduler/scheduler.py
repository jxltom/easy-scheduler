from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import (EVENT_JOB_EXECUTED, EVENT_JOB_ERROR,
                                EVENT_JOB_ADDED, EVENT_JOB_REMOVED)
import arrow


class Scheduler:

    def __init__(self, timezone='UTC'):
        """Initialize scheduler."""
        self._scheduler = BackgroundScheduler(timezone=timezone)
        self._scheduler.add_listener(self._event_job_executed,
                                     EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self._scheduler.add_listener(self._event_job_added, EVENT_JOB_ADDED)
        self._scheduler.add_listener(self._event_job_removed, EVENT_JOB_REMOVED)

        self._status, self._data = {}, {}

    def _event_job_executed(self, event):
        """Update job data after execution."""
        t = arrow.utcnow().to(self._scheduler.timezone).format()
        d = str(event.exception) if event.exception else event.retval
        self._data[event.job_id].append([t, d])

    def _event_job_added(self, event):
        """Update job status and data after adding."""
        self._status[event.job_id] = 'started'
        self._data.setdefault(event.job_id, [])

    def _event_job_removed(self, event):
        """Update job status after removing."""
        self._status[event.job_id] = 'nonexistent'

    def start(self):
        """Start scheduler."""
        self._scheduler.start()

    def shutdown(self, wait=False):
        """Shutdown scheduler."""
        self._scheduler.shutdown(wait=wait)

    def add(self, id, func, trigger, **kwargs):
        """Add job."""
        self.remove(id)
        self._scheduler.add_job(id=id, func=func, trigger=trigger,**kwargs)

    def remove(self, id):
        """Remove job."""
        if self._status.get(id) in ('started', 'paused'):
            self._scheduler.remove_job(id)

    def job_result(self, id, latest=True):
        """Get job results."""
        r = self._data.get(id)
        return r if not latest else r[0] if r else None

    def job_status(self, id):
        """Get job status.

        :return 'started', 'stopped', 'nonexistent'.
        """
        if self._status.get(id, None) is None:
            return 'nonexistent'
        return self._status.get(id)

    def job_next_run_time(self, id, fmt='YYYY-MM-DD HH:mm:ssZZ'):
        """Get job next run time as string."""
        if self._status.get(id):
            t = self._scheduler.get_job(id).next_run_time
            return arrow.get(t).format(fmt=fmt)
        return None

    def print(self):
        """Print jobs information."""
        self._scheduler.print_jobs()

