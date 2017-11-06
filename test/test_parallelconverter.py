import tempfile
import json
import os
import unittest

import amqp.load


# TODO: rename to rabbitmq test...
class TestParallelConverter(unittest.TestCase):
    """
    Requires that RabbitMQ is running
    """
    def test_should_load_message1_into_queue(self):
        pass


class TestProduceQueueMessages(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_create_json_with_dummy1_as_next(self):
        self.assertEqual(
            'dummy1',
            json.loads(amqp.load.message('dummy1', None))['next']
        )

    def test_should_create_json_with_dummy2_as_next(self):
        self.assertEqual(
            'dummy2',
            json.loads(amqp.load.message('dummy2', None))['next']
        )

    def test_should_create_json_with_dummy3_as_tiff(self):
        self.assertEqual(
            'dummy3',
            json.loads(amqp.load.message('dummy1', 'dummy3'))['tiff']
        )

    def test_should_create_json_with_dummy4_as_tiff(self):
        self.assertEqual(
            'dummy4',
            json.loads(amqp.load.message('dummy2', 'dummy4'))['tiff']
        )


    # should put next_file root folder1 sample1.docx in queue and location mid1 dcf1 did1
    # should put next_file root folder1 sample2.docx in queue and location mid1 dcf1 did2
