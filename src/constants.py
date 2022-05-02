import os
PAGE_SIZE_MAX=50
PAGE_SIZE_DEFAULT=10
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


STATUS_ACTIVE = 'active'
STATUS_INACTIVE = 'inactive'

MESSAGE_SUCCESS='success'
PREFIX_CDN='http://14.225.254.88:5000'
# PREFIX_CDN='http://localhost:5000'

STATE_ALL='all'
STATE_ABSENT='absent'
STATE_ATTENDANCE='attendance'
UPLOAD_FOLDER=os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'src/static/uploads')

ALLOWED_FILE=set(['yml','png','jpg','jpeg','txt'])