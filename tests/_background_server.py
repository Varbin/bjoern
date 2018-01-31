#!/usr/bin/env python
"""
Simple instance for runnint a simple WSGI app temporarily in the background.
"""

from multiprocessing import Process
from time import sleep

import bjoern


class BackgroundBjoern(object):
    """
    Runs bjoern with arguments in a background process.
    
    Note: All arguments must be serializable by pickle.
    
    Example:
    
        >>> def app(environ, start_response):
        ...     start_response('200 OK', [('Content-Type', 'text/plain')])
        ...     [b'Hello World!']
        ...
        >>> with BackgroundBjoern(app, 'localhost', 8080):
        ...     requests.get('http://localhost:8080')
        ...
        <Response [200]>
    
    """
    def __init__(self, *args, **kwargs):
        self.p = Process(target=bjoern.run, args=args, kwargs=kwargs)
        
    def __enter__(self):
        self.p.start()
        sleep(.5)  # Startup time!
        
    def __exit__(self, *args, **kwargs):
        self.p.terminate()
