import unittest
from easy_scheduler.scheduler import Scheduler
import time


class TestScheduler(unittest.TestCase):
    """Test Scheduler."""

    @staticmethod
    def _normal_job():
        return 'success'

    @staticmethod
    def _exception_job():
        0 / 0
        return 'success'

    def setUp(self):
        self.scheduler = Scheduler(timezone='Asia/Hong_Kong')
        self.scheduler.start()

    def test_start_pause_resume_shutdown(self):
        """Test scheduler start, pause, resume, and shutdown."""
        self.assertTrue(self.scheduler._scheduler.running)

    def test_add_remove_job_status(self):
        """Test add job, remove job and job_status."""
        # test when job doesn't exist
        self.scheduler.remove('normal_job')
        self.assertEqual(self.scheduler.job_status('normal_job'), 'nonexistent')

        # test when job exists
        self.scheduler.add(
            'normal_job', self._normal_job,
            trigger='cron', hour='00', minute='01')
        self.assertEqual(self.scheduler.job_status('normal_job'), 'started')

        # test remove job
        self.scheduler.remove('normal_job')
        self.assertEqual(self.scheduler.job_status('normal_job'), 'nonexistent')

    def test_job_result(self):
        # test when job doesn't exist
        self.assertTrue(
            self.scheduler.job_result('normal_job', latest=True) is None)
        self.assertTrue(
            self.scheduler.job_result('normal_job', latest=False) is None)

        # test when job exists
        self.scheduler.add(
            'normal_job', self._normal_job,
            trigger='interval', seconds=1)

        time.sleep(3)
        self.assertEqual(
            self.scheduler.job_result('normal_job')[1], 'success')
        self.assertTrue(
            type(self.scheduler.job_result('normal_job', latest=False)), list)
        self.assertTrue(
            type(self.scheduler.job_result('normal_job', latest=False)[0]),
            list)
        self.assertTrue(
            len(self.scheduler.job_result('normal_job', latest=False)) > 1)

    def test_add_job(self):
        """Test add_job."""
        # test daily job
        self.scheduler.add(
            'normal_job', self._normal_job,
            trigger='cron', hour='12', minute='00')
        self.scheduler.print()

        # test interval job
        self.scheduler.add(
            'normal_job', self._normal_job,
            trigger='interval', seconds=1)
        self.scheduler.print()
        time.sleep(3)
        self.assertTrue(
            len(self.scheduler.job_result('normal_job', latest=False)) > 1)
        self.assertTrue(type(self.scheduler.job_result('normal_job')[0]), str)

        # test enable multiple times
        self.scheduler.add(
            'normal_job', self._normal_job,
            trigger='interval', seconds=1)
        time.sleep(2)
        self.scheduler.add(
            'normal_job', self._normal_job,
            trigger='interval', seconds=1)
        self.assertTrue(
            len(self.scheduler.job_result('normal_job', latest=False)) > 1)

    def test_exception_in_job(self):
        """Test exceptions in job."""
        self.scheduler.add(
            'job_exception', self._exception_job,
            trigger='interval', seconds=1)
        time.sleep(2)
        self.assertTrue('division by zero'
                        in self.scheduler.job_result('job_exception')[1])

    def test_next_run_time(self):
        """Test next_run_time."""
        # test job doesn't exist
        self.assertTrue(
            self.scheduler.job_next_run_time('job_normal', fmt='HH:mm') is None)

        # test job exists
        self.scheduler.add(
            'job_normal', self._normal_job,
            trigger='cron', hour='12', minute='00')
        self.assertEqual(
            self.scheduler.job_next_run_time('job_normal', fmt='HH:mm'),
            '12:00')

    def tearDown(self):
        self.scheduler.shutdown()
