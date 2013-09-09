import os
from caiubem.settings.base import *

env = os.environ.get('ENV', 'development')

if env == 'production':
    from caiubem.settings.production import *
elif env == 'test':
    from caiubem.settings.test import *
else:
    from caiubem.settings.development import *
