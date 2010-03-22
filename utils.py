import os
import logging
from google.appengine.ext import db


def GetPathElements():
    '''split PATH_INFO out to a list, filtering blank/empty values'''
    return [ x for x in os.environ['PATH_INFO'].split('/') if x ]

def GetUserAgent():
    '''return the user agent string'''
    return os.environ['HTTP_USER_AGENT']

def Debug():
    '''return True if script is running in the development envionment'''
    return 'Development' in os.environ['SERVER_SOFTWARE']


def sort_by_attr(seq,attr, reverse=True):
    intermed = [ (getattr(seq[i],attr), i, seq[i]) for i in xrange(len(seq)) ]
    intermed.sort()
    if reverse: 
      intermed.reverse() # ranked from greatest to least
    return [ tup[-1] for tup in intermed ]

def sort_by_key(seq,attr, reverse=True):
    intermed = [ (seq[i][attr], i, seq[i]) for i in xrange(len(seq)) ]
    intermed.sort()
    if reverse: 
      intermed.reverse() # ranked from greatest to least
    return [ tup[-1] for tup in intermed ]
       


def defer(method, *args,  **kwargs):
  # A payload can also be sent
  from google.appengine.ext.deferred import deferred
  from google.appengine.api.labs import taskqueue
  # _queue, _countdown, name, _eta
  kwargs['_name'] = task_name( str(method.__name__) + str(args) + str(kwargs.values()))
  try:
   deferred.defer(method, *args, **kwargs)
   logging.info('deferred method %s with args %s and kwargs %s' % (method.__name__, args, kwargs))
  except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError):
    logging.warning('unable to create task with name %s' %
    kwargs['_name'], exc_info=True)
  
def add_task(queue_name='default',payload=None,**kwargs):
  # A payload can also be sent
  if kwargs.get('params', None):
    for json_type in ['kwargs', 'entities']: #
       if kwargs['params'].get(json_type, None):
         from django.utils import simplejson
         kwargs['params'][json_type] = simplejson.dumps(
         kwargs['params'][json_type])
       
  from google.appengine.api.labs import taskqueue
  queue = taskqueue.Queue(name=queue_name)
  try:
    task = taskqueue.Task(payload=payload, **kwargs)
    logging.info('adding task: %s' % kwargs)
    queue.add(task)
  # TODO: Why don't these exceptions work? 
  except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError):
    logging.warning('unable to create task with name %s' %
    kwargs.get('name','(no name provided)'), exc_info=True)


def task_name(string, timestamp=True, version=True):
  # add timestamp if this task may be repeated
  if timestamp: 
    # always going to be unique
    import time
    full_string= "%s-%s" % (string,
    str(time.time()) + str(time.clock())) # see if this gets rid of errors
  elif version:
    # add version name, so version can be changed to override
    full_string = "%s-%s" % (string, os.environ['CURRENT_VERSION_ID'])
  # remove non alphanumeric chars
  import re
  pattern = re.compile('[^A-Za-z0-9-]')
  safe_string = re.sub(pattern, '', full_string)
  MAX_STR_LENGTH = 100
  return safe_string[:MAX_STR_LENGTH] + str(randomInt(digits=20))


class TaskFailError(Exception):
  """ Tasks fail all the time, but 
  they shouldn't be clogging the error logs. """
  def __init__(self, error_msg):
    logging.warning(error_msg)
    

def randomInt(digits=5):
  max = int(''.join('9' for d in range(digits)))
  import random
  return int(str(random.randint(0,max)).zfill(digits))
  
  
def transactionize(fun):
  def decorate(*args, **kwargs):
    return db.run_in_transaction(fun, *args, **kwargs)
  return decorate

