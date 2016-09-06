# -*- coding: utf-8 -*-
"""
Unit Test Template
"""

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import os
import time

from ioflo.aid.sixing import *
from ioflo.aid import odict
from ioflo.test import testing
from ioflo.base import globaling
from ioflo.base import Data, Deck

from ioflo.aid.consoling import getConsole

from ioflo.base import storing
from ioflo.base import logging

console = getConsole()


def setUpModule():
    console.reinit(verbosity=console.Wordage.profuse)

def tearDownModule():
    console.reinit(verbosity=console.Wordage.concise)


class BasicTestCase(testing.LoggerIofloTestCase):
    """
    Example TestCase
    """

    def setUp(self):
        """
        Call super if override so House Framer and Frame are setup correctly
        """
        super(BasicTestCase, self).setUp()

    def tearDown(self):
        """
        Call super if override so House Framer and Frame are torn down correctly
        """
        super(BasicTestCase, self).tearDown()


    def testLogger(self):
        """
        Test creating a logger with a log and loggees
        """
        console.terse("{0}\n".format(self.testLogger.__doc__))
        self.assertEqual(self.house.store, self.store)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.prefix, '/tmp/log/ioflo')
        self.assertTrue(self.logger.runner)  # runner generator is made when logger created

        heading = self.store.create('pose.heading').create(value = 0.0)
        position = self.store.create('pose.position').create([("north", 10.0), ("east", 5.0)])

        log = logging.Log(name='test',
                          store=self.store,
                          kind='text',
                          baseFilename='',
                          rule=globaling.ALWAYS)

        self.assertEqual(log.baseFilename, log.name)
        self.assertEqual(log.path, '')
        self.assertEqual(log.file, None)
        self.assertEqual(log.kind, 'text')

        self.assertEqual(log.rule, globaling.ALWAYS)
        self.assertEqual(log.action, log.always)

        log.addLoggee(tag = 'heading', loggee = 'pose.heading')
        log.addLoggee(tag = 'pos', loggee = 'pose.position')
        log.resolve()

        self.logger.addLog(log)
        self.logger.reopen()  # this updates paths on all logs
        self.assertTrue(self.logger.path.startswith('/tmp/log/ioflo/HouseTest/LoggerTest_'))
        self.assertTrue(log.path.startswith(self.logger.path))
        self.assertTrue(log.path.endswith(log.baseFilename + '.txt'))
        self.assertTrue(log.file)

        log.prepare()
        self.assertEqual(log.formats, {'_time': '%0.4f',
                                        'heading': odict([('value', '\t%0.4f')]),
                                        'pos': odict([('north', '\t%0.4f'), ('east', '\t%0.4f')])})

        self.house.store.changeStamp(0.0)

        log() #log
        for i in range(20):
            self.store.advanceStamp(0.125)
            if i == 5:
                heading.value += 0.0
                position.data.north += 0.0
                position.data.east -= 0.0
            elif i == 10:
                pass
            else:
                heading.value = float(i)
                position.data.north += 2.0
                position.data.east -= 1.5

            log() #log

        log.flush()
        log.file.seek(0)
        line = log.file.readline()
        self.assertEqual(line, 'text\tAlways\ttest\n')
        line = log.file.readline()
        self.assertEqual(line, '_time\theading\tpos.north\tpos.east\n')
        lines = log.file.readlines()
        self.assertEqual(lines, ['0.0000\t0.0000\t10.0000\t5.0000\n',
                                '0.1250\t0.0000\t12.0000\t3.5000\n',
                                '0.2500\t1.0000\t14.0000\t2.0000\n',
                                '0.3750\t2.0000\t16.0000\t0.5000\n',
                                '0.5000\t3.0000\t18.0000\t-1.0000\n',
                                '0.6250\t4.0000\t20.0000\t-2.5000\n',
                                '0.7500\t4.0000\t20.0000\t-2.5000\n',
                                '0.8750\t6.0000\t22.0000\t-4.0000\n',
                                '1.0000\t7.0000\t24.0000\t-5.5000\n',
                                '1.1250\t8.0000\t26.0000\t-7.0000\n',
                                '1.2500\t9.0000\t28.0000\t-8.5000\n',
                                '1.3750\t9.0000\t28.0000\t-8.5000\n',
                                '1.5000\t11.0000\t30.0000\t-10.0000\n',
                                '1.6250\t12.0000\t32.0000\t-11.5000\n',
                                '1.7500\t13.0000\t34.0000\t-13.0000\n',
                                '1.8750\t14.0000\t36.0000\t-14.5000\n',
                                '2.0000\t15.0000\t38.0000\t-16.0000\n',
                                '2.1250\t16.0000\t40.0000\t-17.5000\n',
                                '2.2500\t17.0000\t42.0000\t-19.0000\n',
                                '2.3750\t18.0000\t44.0000\t-20.5000\n',
                                '2.5000\t19.0000\t46.0000\t-22.0000\n'])

        log.close()


    def testLogAlways(self):
        """
        Test creating a logger with a log and loggees
        """
        console.terse("{0}\n".format(self.testLogAlways.__doc__))

        self.assertEqual(self.house.store, self.store)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.prefix, '/tmp/log/ioflo')
        self.assertTrue(self.logger.runner)  # runner generator is made when logger created

        heading = self.store.create('pose.heading').create(value = 0.0)
        position = self.store.create('pose.position').create([("north", 10.0), ("east", 5.0)])

        log = logging.Log(name='test',
                          store=self.store,
                          kind='text',
                          baseFileName='',
                          rule=globaling.ALWAYS)

        self.assertEqual(log.baseFilename, log.name)
        self.assertEqual(log.path, '')
        self.assertEqual(log.file, None)
        self.assertEqual(log.kind, 'text')

        self.assertEqual(log.rule, globaling.ALWAYS)
        self.assertEqual(log.action, log.always)

        log.addLoggee(tag = 'heading', loggee = 'pose.heading')
        log.addLoggee(tag = 'pos', loggee = 'pose.position')

        self.logger.addLog(log)
        self.logger.resolve()  # resolves logs as well


        self.house.store.changeStamp(0.0)
        self.assertIs(log.stamp, None)
        status = self.logger.runner.send(globaling.START)  # reopens prepares and logs once
        self.assertTrue(self.logger.path.startswith('/tmp/log/ioflo/HouseTest/LoggerTest_'))
        self.assertTrue(log.path.startswith(self.logger.path))
        self.assertTrue(log.path.endswith(log.baseFilename + '.txt'))
        self.assertTrue(log.file)
        self.assertEqual(log.formats, {'_time': '%0.4f',
                                       'heading': odict([('value', '\t%0.4f')]),
                                       'pos': odict([('north', '\t%0.4f'), ('east', '\t%0.4f')])})

        for i in range(20):
            self.store.advanceStamp(0.125)
            if i == 5:
                heading.value += 0.0
                position.data.north += 0.0
                position.data.east -= 0.0
            elif i == 10:
                pass
            else:
                heading.value = float(i)
                position.data.north += 2.0
                position.data.east -= 1.5

            status = self.logger.runner.send(globaling.RUN)

        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # logs once and closes logs

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        line = log.file.readline()
        self.assertEqual(line, 'text\tAlways\ttest\n')
        line = log.file.readline()
        self.assertEqual(line, '_time\theading\tpos.north\tpos.east\n')
        lines = log.file.readlines()
        self.assertEqual(lines, ['0.0000\t0.0000\t10.0000\t5.0000\n',
                                '0.1250\t0.0000\t12.0000\t3.5000\n',
                                '0.2500\t1.0000\t14.0000\t2.0000\n',
                                '0.3750\t2.0000\t16.0000\t0.5000\n',
                                '0.5000\t3.0000\t18.0000\t-1.0000\n',
                                '0.6250\t4.0000\t20.0000\t-2.5000\n',
                                '0.7500\t4.0000\t20.0000\t-2.5000\n',
                                '0.8750\t6.0000\t22.0000\t-4.0000\n',
                                '1.0000\t7.0000\t24.0000\t-5.5000\n',
                                '1.1250\t8.0000\t26.0000\t-7.0000\n',
                                '1.2500\t9.0000\t28.0000\t-8.5000\n',
                                '1.3750\t9.0000\t28.0000\t-8.5000\n',
                                '1.5000\t11.0000\t30.0000\t-10.0000\n',
                                '1.6250\t12.0000\t32.0000\t-11.5000\n',
                                '1.7500\t13.0000\t34.0000\t-13.0000\n',
                                '1.8750\t14.0000\t36.0000\t-14.5000\n',
                                '2.0000\t15.0000\t38.0000\t-16.0000\n',
                                '2.1250\t16.0000\t40.0000\t-17.5000\n',
                                '2.2500\t17.0000\t42.0000\t-19.0000\n',
                                '2.3750\t18.0000\t44.0000\t-20.5000\n',
                                '2.5000\t19.0000\t46.0000\t-22.0000\n',
                                '2.6250\t19.0000\t46.0000\t-22.0000\n'])

        self.assertIsNot(log.stamp, None)
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.START)  # logs once no headers since log stamp not none
        self.store.advanceStamp(0.125)
        heading.value += 5.0
        status = self.logger.runner.send(globaling.RUN)  # logs once
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # logs once and closes logs

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        lines = log.file.readlines()
        self.assertEqual(lines, ['text\tAlways\ttest\n',
                                '_time\theading\tpos.north\tpos.east\n',
                                '0.0000\t0.0000\t10.0000\t5.0000\n',
                                '0.1250\t0.0000\t12.0000\t3.5000\n',
                                '0.2500\t1.0000\t14.0000\t2.0000\n',
                                '0.3750\t2.0000\t16.0000\t0.5000\n',
                                '0.5000\t3.0000\t18.0000\t-1.0000\n',
                                '0.6250\t4.0000\t20.0000\t-2.5000\n',
                                '0.7500\t4.0000\t20.0000\t-2.5000\n',
                                '0.8750\t6.0000\t22.0000\t-4.0000\n',
                                '1.0000\t7.0000\t24.0000\t-5.5000\n',
                                '1.1250\t8.0000\t26.0000\t-7.0000\n',
                                '1.2500\t9.0000\t28.0000\t-8.5000\n',
                                '1.3750\t9.0000\t28.0000\t-8.5000\n',
                                '1.5000\t11.0000\t30.0000\t-10.0000\n',
                                '1.6250\t12.0000\t32.0000\t-11.5000\n',
                                '1.7500\t13.0000\t34.0000\t-13.0000\n',
                                '1.8750\t14.0000\t36.0000\t-14.5000\n',
                                '2.0000\t15.0000\t38.0000\t-16.0000\n',
                                '2.1250\t16.0000\t40.0000\t-17.5000\n',
                                '2.2500\t17.0000\t42.0000\t-19.0000\n',
                                '2.3750\t18.0000\t44.0000\t-20.5000\n',
                                '2.5000\t19.0000\t46.0000\t-22.0000\n',
                                '2.6250\t19.0000\t46.0000\t-22.0000\n',
                                '2.7500\t19.0000\t46.0000\t-22.0000\n',
                                '2.8750\t24.0000\t46.0000\t-22.0000\n',
                                '3.0000\t24.0000\t46.0000\t-22.0000\n'])
        log.file.close()

    def testLogOnce(self):
        """
        Test log with once rule
        """
        console.terse("{0}\n".format(self.testLogOnce.__doc__))

        self.assertEqual(self.house.store, self.store)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.prefix, '/tmp/log/ioflo')
        self.assertTrue(self.logger.runner)  # runner generator is made when logger created

        log = logging.Log(name='test',
                          store=self.store,
                          kind='text',
                          baseFileName='',
                          rule=globaling.ONCE)

        self.assertEqual(log.rule, globaling.ONCE)
        self.assertEqual(log.action, log.once)

        heading = self.store.create('pose.heading').create(value = 0.0)
        log.addLoggee(tag = 'heading', loggee = 'pose.heading')
        self.logger.addLog(log)
        self.logger.resolve()  # resolves logs as well

        self.house.store.changeStamp(0.0)
        self.assertIs(log.stamp, None)
        status = self.logger.runner.send(globaling.START)  # reopens prepares and logs once
        self.assertEqual(log.formats, {
                                       '_time': '%0.4f',
                                       'heading': odict([('value', '\t%0.4f')])
                                      })

        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.25)
        heading.value += 0.0  # updated but same value
        status = self.logger.runner.send(globaling.RUN)  # logs since updated
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.5)
        heading.value += 5.0  # update with different value
        status = self.logger.runner.send(globaling.RUN)  # logs since updated
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # not log since not updated

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        lines = log.file.readlines()
        self.assertEqual(lines, ['text\tOnce\ttest\n', '_time\theading\n', '0.0000\t0.0000\n'])
        log.file.close()

    def testLogNever(self):
        """
        Test log with never rule
        """
        console.terse("{0}\n".format(self.testLogNever.__doc__))

        self.assertEqual(self.house.store, self.store)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.prefix, '/tmp/log/ioflo')
        self.assertTrue(self.logger.runner)  # runner generator is made when logger created

        log = logging.Log(name='test',
                          store=self.store,
                          kind='text',
                          baseFileName='',
                          rule=globaling.NEVER)

        self.assertEqual(log.rule, globaling.NEVER)
        self.assertEqual(log.action, log.never)

        heading = self.store.create('pose.heading').create(value = 0.0)
        log.addLoggee(tag = 'heading', loggee = 'pose.heading')
        self.logger.addLog(log)
        self.logger.resolve()  # resolves logs as well

        self.house.store.changeStamp(0.0)
        self.assertIs(log.stamp, None)
        status = self.logger.runner.send(globaling.START)  # reopens prepares and logs once
        self.assertEqual(log.formats, {
                                       '_time': '%0.4f',
                                       'heading': odict([('value', '\t%0.4f')])
                                      })

        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.25)
        heading.value += 0.0  # updated but same value
        status = self.logger.runner.send(globaling.RUN)  # logs since updated
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.5)
        heading.value += 5.0  # update with different value
        status = self.logger.runner.send(globaling.RUN)  # logs since updated
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # not log since not updated

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        lines = log.file.readlines()
        self.assertEqual(lines, ['text\tNever\ttest\n', '_time\theading\n'])
        log.file.close()


    def testLogUpdate(self):
        """
        Test log with update rule
        """
        console.terse("{0}\n".format(self.testLogUpdate.__doc__))

        self.assertEqual(self.house.store, self.store)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.prefix, '/tmp/log/ioflo')
        self.assertTrue(self.logger.runner)  # runner generator is made when logger created

        log = logging.Log(name='test',
                          store=self.store,
                          kind='text',
                          baseFileName='',
                          rule=globaling.UPDATE)

        self.assertEqual(log.rule, globaling.UPDATE)
        self.assertEqual(log.action, log.update)

        heading = self.store.create('pose.heading').create(value = 0.0)
        log.addLoggee(tag = 'heading', loggee = 'pose.heading')
        self.logger.addLog(log)
        self.logger.resolve()  # resolves logs as well

        self.house.store.changeStamp(0.0)
        self.assertIs(log.stamp, None)
        status = self.logger.runner.send(globaling.START)  # reopens prepares and logs once
        self.assertEqual(log.formats, {
                                       '_time': '%0.4f',
                                       'heading': odict([('value', '\t%0.4f')])
                                      })

        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.25)
        heading.value += 0.0  # updated but same value
        status = self.logger.runner.send(globaling.RUN)  # logs since updated
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.5)
        heading.value += 5.0  # update with different value
        status = self.logger.runner.send(globaling.RUN)  # logs since updated
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # not log since not updated

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        lines = log.file.readlines()
        self.assertEqual(lines, ['text\tUpdate\ttest\n',
                                '_time\theading\n',
                                '0.0000\t0.0000\n',
                                '0.2500\t0.0000\n',
                                '0.5000\t5.0000\n'])
        log.file.close()


    def testLogUpdateFields(self):
        """
        Test log with update rule and passed in fields list
        """
        console.terse("{0}\n".format(self.testLogUpdateFields.__doc__))

        self.assertEqual(self.house.store, self.store)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.prefix, '/tmp/log/ioflo')
        self.assertTrue(self.logger.runner)  # runner generator is made when logger created

        log = logging.Log(name='test',
                          store=self.store,
                          kind='text',
                          baseFileName='',
                          rule=globaling.UPDATE)

        self.assertEqual(log.rule, globaling.UPDATE)
        self.assertEqual(log.action, log.update)

        ned = self.store.create('pose.ned').create(north = 0.0, east=0.0, down=0.0)
        log.addLoggee(tag = 'ned', loggee = 'pose.ned', fields=['north', 'east'])
        self.logger.addLog(log)
        self.logger.resolve()  # resolves logs as well

        self.house.store.changeStamp(0.0)
        self.assertIs(log.stamp, None)
        status = self.logger.runner.send(globaling.START)  # reopens prepares and logs once
        self.assertEqual(log.formats, {'_time': '%0.4f',
                                       'ned': odict([('north', '\t%0.4f'),
                                                     ('east', '\t%0.4f')])})

        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.25)
        ned.update(north=0.0)  # updated but same value
        status = self.logger.runner.send(globaling.RUN)  # log since updated
        self.store.advanceStamp(0.125)
        ned.update(down=0.0)  # updated a field but not loggee field
        status = self.logger.runner.send(globaling.RUN)  # log since updated any field
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.5)
        ned.update(north=5.0, east=7.0)  # update with different values
        status = self.logger.runner.send(globaling.RUN)  # log since updated
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # not log since not updated

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        lines = log.file.readlines()
        self.assertEqual(lines, ['text\tUpdate\ttest\n',
                                '_time\tned.north\tned.east\n',
                                '0.0000\t0.0000\t0.0000\n',
                                '0.2500\t0.0000\t0.0000\n',
                                '0.3750\t0.0000\t0.0000\n',
                                '0.5000\t5.0000\t7.0000\n']
                               )
        log.file.close()

    def testLogChange(self):
        """
        Test log with change rule
        """
        console.terse("{0}\n".format(self.testLogChange.__doc__))

        self.assertEqual(self.house.store, self.store)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.prefix, '/tmp/log/ioflo')
        self.assertTrue(self.logger.runner)  # runner generator is made when logger created

        log = logging.Log(name='test',
                          store=self.store,
                          kind='text',
                          baseFileName='',
                          rule=globaling.CHANGE)

        self.assertEqual(log.rule, globaling.CHANGE)
        self.assertEqual(log.action, log.change)

        heading = self.store.create('pose.heading').create(value = 0.0)
        log.addLoggee(tag = 'heading', loggee = 'pose.heading')
        self.logger.addLog(log)
        self.logger.resolve()  # resolves logs as well

        self.house.store.changeStamp(0.0)
        self.assertIs(log.stamp, None)
        status = self.logger.runner.send(globaling.START)  # reopens prepares and logs once
        self.assertEqual(log.formats, {
                                       '_time': '%0.4f',
                                       'heading': odict([('value', '\t%0.4f')])
                                      })
        self.assertTrue('heading' in log.lasts)

        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.25)
        heading.value += 0.0  # updated but same value
        status = self.logger.runner.send(globaling.RUN)  # no log since updated but not changed
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.5)
        heading.value += 5.0  # update with different value
        status = self.logger.runner.send(globaling.RUN)  # logs since changed
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # not log since not updated

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        lines = log.file.readlines()
        self.assertEqual(lines, ['text\tChange\ttest\n',
                                '_time\theading\n',
                                '0.0000\t0.0000\n',
                                '0.5000\t5.0000\n'])
        log.file.close()

    def testLogChangeFields(self):
        """
        Test log with update rule and passed in fields list
        """
        console.terse("{0}\n".format(self.testLogChangeFields.__doc__))

        self.assertEqual(self.house.store, self.store)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.prefix, '/tmp/log/ioflo')
        self.assertTrue(self.logger.runner)  # runner generator is made when logger created

        log = logging.Log(name='test',
                          store=self.store,
                          kind='text',
                          baseFileName='',
                          rule=globaling.CHANGE)

        self.assertEqual(log.rule, globaling.CHANGE)
        self.assertEqual(log.action, log.change)

        ned = self.store.create('pose.ned').create(north = 0.0, east=0.0, down=0.0)
        fields = ['north', 'east']
        log.addLoggee(tag = 'ned', loggee = 'pose.ned', fields=fields)
        self.logger.addLog(log)
        self.logger.resolve()  # resolves logs as well

        self.house.store.changeStamp(0.0)
        self.assertIs(log.stamp, None)
        status = self.logger.runner.send(globaling.START)  # reopens prepares and logs once
        self.assertEqual(log.formats, {'_time': '%0.4f',
                                       'ned': odict([('north', '\t%0.4f'),
                                                     ('east', '\t%0.4f')])})
        self.assertTrue('ned' in log.lasts)
        last = log.lasts['ned']
        for field in fields:
            self.assertEqual(getattr(last, field), 0.0)

        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.25)
        ned.update(north=0.0)  # updated but same value
        status = self.logger.runner.send(globaling.RUN)  # not log since not changed
        self.store.advanceStamp(0.125)
        ned.update(down=4.0)  # updated a field but not loggee field
        status = self.logger.runner.send(globaling.RUN)  # not log since not changed given field
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.5)
        ned.update(north=5.0, east=7.0)  # update with different values
        status = self.logger.runner.send(globaling.RUN)  # log since changed given field
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # not log since not changed

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        lines = log.file.readlines()
        self.assertEqual(lines, ['text\tChange\ttest\n',
                                '_time\tned.north\tned.east\n',
                                '0.0000\t0.0000\t0.0000\n',
                                '0.5000\t5.0000\t7.0000\n']
                            )
        log.file.close()

    def testLogStreak(self):
        """
        Test log with streak rule
        """
        console.terse("{0}\n".format(self.testLogStreak.__doc__))

        self.assertEqual(self.house.store, self.store)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.prefix, '/tmp/log/ioflo')
        self.assertTrue(self.logger.runner)  # runner generator is made when logger created

        log = logging.Log(name='test',
                          store=self.store,
                          kind='text',
                          baseFileName='',
                          rule=globaling.STREAK)

        self.assertEqual(log.rule, globaling.STREAK)
        self.assertEqual(log.action, log.streak)

        heading = self.store.create('pose.heading').create(value = 0.0)
        log.addLoggee(tag = 'heading', loggee = 'pose.heading')
        self.logger.addLog(log)
        self.logger.resolve()  # resolves logs as well

        self.house.store.changeStamp(0.0)
        self.assertIs(log.stamp, None)
        status = self.logger.runner.send(globaling.START)  # reopens prepares and logs once
        self.assertEqual(log.formats, {
                                       '_time': '%0.4f',
                                       'heading': odict([('value', '\t%s')])
                                      })

        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.25)
        heading.value += 0.0  # updated but same value
        status = self.logger.runner.send(globaling.RUN)  # no log since updated but not changed
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.5)
        heading.value += 5.0  # update with different value
        status = self.logger.runner.send(globaling.RUN)  # logs since changed
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # not log since not updated

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        lines = log.file.readlines()
        self.assertEqual(lines, ['text\tStreak\ttest\n',
                                '_time\theading\n',
                                '0.0000\t0.0\n',
                                '0.1250\t0.0\n',
                                '0.2500\t0.0\n',
                                '0.3750\t0.0\n',
                                '0.5000\t5.0\n',
                                '0.6250\t5.0\n'])
        log.file.close()

        heading.value = ["hello", "how", "are", "you", 5.0, 6, 7]

        self.assertEqual(log.stamp, 0.625)
        status = self.logger.runner.send(globaling.START)  # reopens prepares and logs once
        self.assertEqual(log.formats, {
                                       '_time': '%0.4f',
                                       'heading': odict([('value', '\t%s')])
                                      })
        #self.assertTrue('heading' in log.lasts)

        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        heading.value.append(10.0)
        status = self.logger.runner.send(globaling.RUN)  # no log since updated but not changed
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        heading.value.append(15)
        heading.value.append(20)
        status = self.logger.runner.send(globaling.RUN)  # logs since changed
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # not log since not updated

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        lines = log.file.readlines()
        self.assertEqual(lines, ['text\tStreak\ttest\n',
                                '_time\theading\n',
                                '0.0000\t0.0\n',
                                '0.1250\t0.0\n',
                                '0.2500\t0.0\n',
                                '0.3750\t0.0\n',
                                '0.5000\t5.0\n',
                                '0.6250\t5.0\n',
                                '0.6250\thello\n',
                                '0.6250\thow\n',
                                '0.6250\tare\n',
                                '0.6250\tyou\n',
                                '0.6250\t5.0\n',
                                '0.6250\t6\n',
                                '0.6250\t7\n',
                                '0.8750\t10.0\n',
                                '1.1250\t15\n',
                                '1.1250\t20\n'])
        log.file.close()

    def testLogDeck(self):
        """
        Test log with deck rule
        """
        console.terse("{0}\n".format(self.testLogDeck.__doc__))

        self.assertEqual(self.house.store, self.store)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.prefix, '/tmp/log/ioflo')
        self.assertTrue(self.logger.runner)  # runner generator is made when logger created

        log = logging.Log(name='test',
                          store=self.store,
                          kind='text',
                          baseFileName='',
                          rule=globaling.DECK)

        self.assertEqual(log.rule, globaling.DECK)
        self.assertEqual(log.action, log.deck)

        ned = self.store.create('pose.ned')
        fields = ['north', 'east']
        log.addLoggee(tag = 'ned', loggee = 'pose.ned', fields=fields)
        self.logger.addLog(log)
        self.logger.resolve()  # resolves logs as well

        ned.push(odict(north=0.0, east=0.0, down=0.0))
        ned.push(odict(north=5.0, east=4.0, down=3.0))
        ned.push(odict(north=6.0, east=3.0, down=2.0))
        ned.push(odict(east=2.0, down=1.0))
        ned.push(odict(down=0.0))
        ned.push(odict(north=7.0, east=4.0, down=3.0))
        ned.push(["hi", "there"])
        ned.push(odict(north=8.0, east=5.0, down=4.0))

        self.assertEqual(ned.deck, Deck([odict([('down', 0.0),('north', 0.0), ('east', 0.0)]),
                                         odict([('down', 3.0), ('north', 5.0), ('east', 4.0)]),
                                         odict([('down', 2.0), ('north', 6.0), ('east', 3.0)]),
                                         odict([('down', 1.0), ('east', 2.0)]),
                                         odict([('down', 0.0)]),
                                         odict([('down', 3.0), ('north', 7.0), ('east', 4.0)]),
                                         ['hi', 'there'],
                                         odict([('down', 4.0), ('north', 8.0), ('east', 5.0)])]))

        self.house.store.changeStamp(0.0)
        self.assertIs(log.stamp, None)
        status = self.logger.runner.send(globaling.START)  # reopens prepares and logs once
        self.assertEqual(log.formats, {'_time': '%0.4f',
                                       'ned': odict([('north', '\t%s'), ('east', '\t%s')])})

        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # no log since not updated
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.25)
        ned.push(odict(north=9.0, east=6.0, down=5.0))  # push another
        status = self.logger.runner.send(globaling.RUN)  # not log since not changed
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.RUN)  # not log since not changed given field
        self.store.advanceStamp(0.125)
        self.assertEqual(self.store.stamp, 0.5)
        ned.push(odict(north=10.0, east=7.0, down=6.0))  # push
        status = self.logger.runner.send(globaling.RUN)  # log since changed given field
        self.store.advanceStamp(0.125)
        status = self.logger.runner.send(globaling.STOP)  # not log since not changed

        log.reopen()
        log.file.seek(0)  # reopen appends so seek back to start
        lines = log.file.readlines()
        self.assertEqual(lines, ['text\tDeck\ttest\n',
                                '_time\tned.north\tned.east\n',
                                '0.0000\t0.0\t0.0\n',
                                '0.0000\t5.0\t4.0\n',
                                '0.0000\t6.0\t3.0\n',
                                '0.0000\t\t2.0\n',
                                '0.0000\t\t\n',
                                '0.0000\t7.0\t4.0\n',
                                '0.0000\t8.0\t5.0\n',
                                '0.2500\t9.0\t6.0\n',
                                '0.5000\t10.0\t7.0\n'])
        log.file.close()



def runOne(test):
    '''
    Unittest Runner
    '''
    test = BasicTestCase(test)
    suite = unittest.TestSuite([test])
    unittest.TextTestRunner(verbosity=2).run(suite)

def runSome():
    """ Unittest runner """
    tests =  []
    names = ['testLogger',
             'testLogAlways',
             'testLogOnce',
             'testLogNever',
             'testLogUpdate',
             'testLogUpdateFields',
             'testLogChange',
             'testLogChangeFields',
             'testLogStreak',
             'testLogDeck',
            ]
    tests.extend(map(BasicTestCase, names))
    suite = unittest.TestSuite(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)

def runAll():
    """ Unittest runner """
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(BasicTestCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__' and __package__ is None:

    #console.reinit(verbosity=console.Wordage.concise)

    #runAll() #run all unittests

    runSome()#only run some

    #runOne('testLogDeck')
