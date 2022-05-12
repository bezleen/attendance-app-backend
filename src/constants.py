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

SERVICE_ACCOUNT_KEY = os.path.abspath(os.path.dirname(
    os.path.dirname(__file__)))+"/serviceAccountKey.json"

FIREBASE_CONFIG ={
  "apiKey": "AIzaSyBBna5KLzdGAlJrsffIFFZf2D_F5ALFL6s",
  "authDomain": "bezleen-app.firebaseapp.com",
  "databaseURL":"https://bezleen-app-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "bezleen-app",
  "storageBucket": "bezleen-app.appspot.com",
  "messagingSenderId": "1061161712722",
  "appId": "1:1061161712722:web:359016b4739596fb76b38b",
  "measurementId": "G-FBDJ8DXCJC",
  "serviceAccount": SERVICE_ACCOUNT_KEY
}
SMTP_PASSWORD=os.getenv('SMTP_PASSWORD')
DEFAULT_AVATAR=""
EXP_OTP=120
KEY_OTP_REDIS="helu-helu:auth/user:forgot_password_OTP-"
LENGTH_OTP=7