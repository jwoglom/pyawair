import requests
import json
import arrow

try:
  from urllib.parse import urlencode
except ImportError:
  from urllib import urlencode

class awair:

  def __init__(self, username, password, access_token=None):
    self.username = username
    self.password = password

    if not access_token:
      self.login()
    else:
      self.access_token = access_token
    self.password = None


  def make_request(self, url, params=None, method='GET'):
    headers = {"Authorization": "Bearer " + self.access_token}
    if params:
      params = urlencode(params, True).replace('+', '%20')
    if method == 'GET':
      r = requests.get(url, params=params, headers=headers)
    elif method == 'POST':
      r = requests.post(url, params=params, headers=headers)

    try:
      response = r.json()
    except Exception:
      print('Unable to parse JSON:', r.status_code, r.text)
      return {'data': None}

    return response

  def _datefmt(self, date):
    return arrow.get(date).format('YYYY-MM-DDTHH:mm:ss.000')+'Z'

  def login(self):
    print("logging in")
    url = "https://mobile-app.awair.is/v1/users/login"
    data = {"email": self.username, "password": self.password}
    response = requests.post(url, json=data).json()
    self.access_token = response['accessToken']
    self.user_id = response['userId']

  def devices(self):
    url = "https://internal.awair.is/v1.1/users/self/devices"
    devices = self.make_request(url, method="GET")['data']
    return devices

  """
  Returns weather data
  (untested: currently returns an error)
  """
  def weather(self, latitude, longitude):
    url = 'https://internal.awair.is/v1.2/weather?latitude={}&longitude={}'.format(latitude, longitude)
    return self.make_request(url, method="GET")

  """
  Returns raw sensor data over the given time period
  [{'timestamp': '2020-09-01T20:30:00.000Z',
   'score': 91.53333282470703,
   'sensor': {'co2': 501.23333740234375,
    'pm25': 1.8333333730697632,
    'temp': 25.66933250427246,
    'humid': 58.34000015258789,
    'voc': 136.5},
   'index': {'co2': 0, 'pm25': 0, 'temp': 1, 'humid': 1, 'voc': 0}},
  """
  def timeline(self, device, from_date=None, to_date=None):
    device_type = device['device_type']
    device_id = device['device_id']
    url = 'https://internal.awair.is/v1.2/devices/{}/{}/timeline'.format(device_type, device_id)
    if from_date and to_date:
      url += '?from={}&to={}'.format(self._datefmt(from_date), self._datefmt(to_date))

    return self.make_request(url, method="GET")['data']

  """Returns processed sensor data, including metadata and color fields
  [{'timestamp': '2020-08-29T19:02:09.000Z',
   'score': 76,
   'color': 'amber',
   'index': {'co2': 1, 'humid': 3, 'voc': 0, 'pm25': 0, 'temp': 1},
   'sensor': {'co2': 711,
    'humid': 77.5999984741211,
    'voc': 0,
    'pm25': 3,
    'temp': 25.670000076293945},
   'meta': {'temp': 'high', 'humid': 'high'}},
  """
  def events_score(self, device, desc="true", limit="1"):
    device_type = device['device_type']
    device_id = device['device_id']
    url = "https://internal.awair.is/v1/devices/{}/{}/events/score?desc={}&limit={}".format(device_type, device_id, desc, limit)
    return self.make_request(url, method="GET")['data']

  """
  Returns the sleep report
  (untested)
  """
  def sleep_report(self, device, timestamp, lang="en"):
    device_type = device['device_type']
    device_id = device['device_id']
    url = "https://internal.awair.is/v1.2/users/self/devices/{}/{}/sleep-report?lang={}&timestamp={}".format(device_type, device_id, lang, timestamp)
    return self.make_request(url, method="GET")

  """
  Returns history of the sleep report(s)
  (untested)
  """
  def sleep_report_history(self, device):
    device_type = device['device_type']
    device_id = device['device_id']
    url = "https://internal.awair.is/v1.2/users/self/devices/{}/{}/sleep-report/history".format(device_type, device_id)
    return self.make_request(url, method="GET")

  """
  Returns whether sleep reports are on.
  If a device is specified:
  {'enabled': False}
  If no device is specified:
  [{'device_id': XXXX,
   'device_type': 'awair-element',
   'device_name': 'Awair',
   'location_name': 'XXXX',
   'sleep_report_setting': {'enabled': False}}]
  """
  def sleep_report_setting(self, device=None):
    if device:
      device_type = device['device_type']
      device_id = device['device_id']
      url = "https://internal.awair.is/v1.2/users/self/devices/{}/{}/sleep-report-setting".format(device_type, device_id)
    else:
      url = "https://internal.awair.is/v1.2/users/self/devices/all/sleep-report-setting"

    r = self.make_request(url, method="GET")
    if 'data' in r:
      return r['data']

  """
  Returns the current display setting and brightness level
  [{'timestamp': '2020-09-05T00:56:37.787Z',
   'mode': 'co2',
   'brightness': 179}]
  """
  def events_display(self, device):
    device_type = device['device_type']
    device_id = device['device_id']
    url = "https://internal.awair.is/v1/users/self/devices/{}/{}/events/display".format(device_type, device_id)

    return self.make_request(url, method="GET")['data']

  """
  Returns notification inbox items for the given device
  [{'title': 'CO₂',
   'device_name': 'Awair',
   'description': 'Much better! The CO₂ in Awair is lower now.',
   'icon_url': 'https://d2afsft9cy76hy.cloudfront.net/img/icon_co2_0.png',
   'timestamp': '2020-09-05T18:00:00.000Z',
   'link': 'awair://trend?deviceType=awair-element&deviceId=XXXX&timestamp=2020-09-05T18:00:00.000Z&reason=co2-ok&component=co2'}],
 'pagination': {'has_next': True, 'next_to': '2020-09-05T14:55:00.000Z'}
  """
  def inbox_items(self, device, lang="en", limit="1"):
    device_id = device['device_id']
    url = "https://internal.awair.is/v1/users/self/inbox-items?to={}&lang={}&limit={}".format(device_id, lang, limit)

    return self.make_request(url, method="GET")['data']
