import json
import os
import pika
import unittest

import amqp.load
import test.util
from tiff.converter import ParallelConverter
from tiff.filehandler import LocalFilePathStrategy
from siarddk.docindex import DocIndexHandler


# TODO: rename to rabbitmq test...
class TestParallelConverter(unittest.TestCase,
                            test.util.StandardConversionTestSetup):
    """
    Requires that RabbitMQ is running
    """

    def setUp(self):
        self.source, self.target = self.prepare('test/resources/root')
        self.name = 'AVID.MAG.1000'
        self.converter = ParallelConverter(
            self.target,
            self.name,
            'localhost',
            LocalFilePathStrategy(self.source),
            DocIndexHandler(self.target, self.name)
        )
        self.converter._setup_connections()

    def tearDown(self):
        self.converter.message_channel.queue_delete(
            queue=ParallelConverter.MESSAGE_QUEUE_NAME)
        self.converter.message_channel.queue_delete(
            queue=ParallelConverter.PROCESSED_QUEUE_NAME)
        self.converter.connection.close()
        self.cleanup()

    def _send_processed_queue_message(self, body):
        send_channel = self.converter.connection.channel()
        send_channel.queue_declare(queue=ParallelConverter.PROCESSED_QUEUE_NAME,
                                   durable=True)
        send_channel.basic_publish(
            exchange='',
            routing_key=self.converter.PROCESSED_QUEUE_NAME,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

    def test_should_aggregate_localfilepathstrategy(self):
        converter = ParallelConverter(None, None, None,
                                      LocalFilePathStrategy(None), None)
        self.assertEqual('LocalFilePathStrategy',
                         converter.file_path_strategy.__class__.__name__)

    def test_should_aggregate_inplacefilepathstrategy(self):
        converter = ParallelConverter(None, None, None,
                                      'InPlaceFilePathStrategy_dummy', None)
        self.assertEqual('InPlaceFilePathStrategy_dummy',
                         converter.file_path_strategy)

    def test_should_aggregate_docindexhandler(self):
        converter = ParallelConverter(None, None, None,
                                      LocalFilePathStrategy(None),
                                      'DocIndexHandler_dummy')
        self.assertEqual('DocIndexHandler_dummy', converter.docindex_handler)

    def test_should_store_name(self):
        self.assertEqual('AVID.MAG.1000', self.converter.name)

    def test_should_store_target(self):
        self.assertEqual(self.target, self.converter.target)

    def test_should_store_host(self):
        self.assertEqual('localhost', self.converter.host)

    def test_next_file_should_be_folder1_sample1_docx(self):
        self.assertEqual(
            os.path.join(self.source, 'folder1', 'sample1.docx'),
            self.converter._get_next()[0]
        )

    def test_next_file_should_be_folder1_sample2_docx(self):
        self.converter._get_next()
        self.assertEqual(
            os.path.join(self.source, 'folder1', 'sample2.docx'),
            self.converter._get_next()[0]
        )

    def test_tiff_path_should_be_111_1_tif(self):
        self.assertEqual(
            os.path.join(self.target, '%s.1' % self.name, 'Documents',
                         'docCollection1', '1', '1.tif'),
            self.converter._get_next()[1]
        )

    def test_tiff_path_should_be_112_1_tif(self):
        self.converter._get_next()
        self.assertEqual(
            os.path.join(self.target, '%s.1' % self.name, 'Documents',
                         'docCollection1', '2', '1.tif'),
            self.converter._get_next()[1]
        )

    def test_build_correct_queue_message(self):
        next_file, tiff_path = self.converter._get_next()
        self.assertEqual(
            json.dumps({
                'next': next_file,
                'tiff': tiff_path
            }),
            self.converter._send_message(next_file, tiff_path)
        )

    def test_store_connection(self):
        self.assertEqual('BlockingConnection',
                         self.converter.connection.__class__.__name__)

    def test_store_channel(self):
        self.assertEqual('BlockingChannel',
                         self.converter.message_channel.__class__.__name__)

    def test_should_load_message1_into_queue(self):
        next_file, tiff_path = self.converter._get_next()
        self.converter._send_message(next_file, tiff_path)

        message_from_queue = str(self.converter.message_channel.basic_get(
            queue=ParallelConverter.MESSAGE_QUEUE_NAME)[-1], 'utf-8')

        self.assertEqual(
            json.dumps({
                'next': next_file,
                'tiff': tiff_path
            }),
            message_from_queue
        )

    def test_messages_sent_is_0_when_no_messages_are_sent(self):
        self.assertEqual(0, self.converter.messages_sent)

    def test_messages_sent_is_1_when_1_messages_is_sent(self):
        self.converter._send_message('dummy1', 'dummy2')
        self.assertEqual(1, self.converter.messages_sent)

    def test_max_queue_length_should_be_100(self):
        self.assertEqual(100, self.converter.QUEUE_MAX)

    def test_should_load_1_messages_into_queue(self):
        self.converter._load_messages(1)
        self.assertEqual(1, self.converter.messages_sent)

        message_from_queue = str(self.converter.message_channel.basic_get(
            queue=ParallelConverter.MESSAGE_QUEUE_NAME)[-1], 'utf-8')

        self.assertEqual(
            json.dumps({
                'next': os.path.join(self.source, 'folder1', 'sample1.docx'),
                'tiff': os.path.join(self.target, '%s.1' % self.name,
                                     'Documents', 'docCollection1', '1',
                                     '1.tif')
            }),
            message_from_queue
        )

    def test_should_load_2_messages_into_queue(self):
        self.converter._load_messages(2)
        self.assertEqual(2, self.converter.messages_sent)

        message_from_queue = str(self.converter.message_channel.basic_get(
            queue=ParallelConverter.MESSAGE_QUEUE_NAME)[-1], 'utf-8')
        self.assertEqual(
            json.dumps({
                'next': os.path.join(self.source, 'folder1', 'sample1.docx'),
                'tiff': os.path.join(self.target, '%s.1' % self.name,
                                     'Documents', 'docCollection1', '1',
                                     '1.tif')
            }),
            message_from_queue
        )

        message_from_queue = str(self.converter.message_channel.basic_get(
            queue=ParallelConverter.MESSAGE_QUEUE_NAME)[-1], 'utf-8')
        self.assertEqual(
            json.dumps({
                'next': os.path.join(self.source, 'folder1', 'sample2.docx'),
                'tiff': os.path.join(self.target, '%s.1' % self.name,
                                     'Documents', 'docCollection1', '2',
                                     '1.tif')
            }),
            message_from_queue
        )

    # @unittest.skip('ksjdksj')
    def test_only_add_max_messages_to_queue(self):
        self.converter.QUEUE_MAX = 3  # For convenience
        self._send_processed_queue_message('end')
        self.converter.run()
        self.assertEqual(3, self.converter.messages_sent)

    def test_progress_count_should_be_0_initially(self):
        self.assertEqual(0, self.converter.messages_processed)

    @unittest.skip('later')
    def test_progress_count_should_be_1_when_first_messages_processed(self):
        # send_channel = self.converter.connection.channel()
        # send_channel.queue_declare(queue=ParallelConverter.PROCESSED_QUEUE_NAME,
        #                            durable=True)
        # send_channel.basic_publish(
        #     exchange='',
        #     routing_key=self.converter.PROCESSED_QUEUE_NAME,
        #     body='1',
        #     properties=pika.BasicProperties(
        #         delivery_mode=2,
        #     )
        # )
        self._send_processed_queue_message('1')
        self.converter.run()

        self.assertEqual(1, self.converter.messages_processed)

    # def test_should_consume_progress_queue(self):
    #     pass

    def test_x(self):
        pass


# MAX = queue size = 10

# should add MAX messages to queue
# should check progress queue for progress
# should store progress
# should load more messages into queue if number of messages in queues < MAX/2
# should only load more messages if any left
# should only load as many messages as are left
# should close connection all messages have passed through


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
