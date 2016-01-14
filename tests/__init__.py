__author__ = 'fermayo'

# Python 3.4.2 includes mock in-box, prefer that version
# For other versions, patch it up to use the external mock library
try:
    from unittest import mock
except ImportError:
    import sys

    sys.modules['unittest'] = __import__('unittest')
    sys.modules['unittest.mock'] = __import__('mock')
    setattr(sys.modules['unittest'], 'mock', __import__('mock'))
