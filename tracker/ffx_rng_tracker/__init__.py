import sys

MIN_VERSION_INFO = 3, 10

if sys.version_info < MIN_VERSION_INFO:
    MIN_VERSION_INFO = '.'.join(str(i) for i in MIN_VERSION_INFO)
    raise RuntimeError(f'Python ver. {MIN_VERSION_INFO} or higher is required')
