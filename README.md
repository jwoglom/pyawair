# pyawair

A very simple python class to access the (private) awair api

This is a fork of https://github.com/harperreed/pyawair which has been updated due to changes in the Awair API.

## Why

I have a few Awair devices around my house and they are great. I like how they look, and the service that they provide. The only issue I have with teh device and service is that Awair doesn't offer a public API at the consumer level. I cannot incorporate the data that Awair is collecting into my dashboards and home automation.

I spent a bit of time looking into how to get access to their enterprise API. APparently you have to pay for it and have five or more devices. Both of those seemed untenable currently. The enterprise product looks really neat so I hope that one day I have an office that can use it!

This API is what powers their iOS app and is robust and well designed.

## Example

The API is super straightforward.

Import the class
```python
from pyawair import awair
```

You can isntantiate the class by logging in using your username and password
```python
username = "email@gmail.com"
password = "very long and secure password"

api =  awair(username, password)
```

If you already have an access token, you can use that instead of username and password. This will skip the login process
```python
access_token = "XXXXX"
api =  awair(username, password, access_token)
```

Once you are logged in, you can grab all the devices
```python
devices = api.devices()

for device in devices:  #Let's iterate through devices
  print(device) #Print the device

  print("Let's grab the weather")
      print(api.weather(latitude=device['latitude'], longitude=device['longitude']))

      print("Timeline from yesterday to today")
      # The date input is parsed by arrow and converted into the correct format
      print(api.timeline(device, from_date=yesterday.isoformat(), to_date=today.isoformat()))

      print("Event score")
      print api.events_score(device)
```

You can also access your in app "inbox"
```python
inbox = api.inbox_items(device, limit=10)
for message in inbox:
  print(message)
```
## Warning

Obviously this is not a supported API. You should not use this. You should work with Awair and use their enterprise offering.

If that offering doesn't work for you (much like it doesn't yet work for me) - then YMMV with this. I expect that they will change their api frequently (notice the versions in the URL).

## Yay!

I hope this is helpful. It would be pretty easy to use this to create a v nice custom component for home assistant. They API has enough resolution that you could really react to changes when they happen.

If you have questions or comments - hit me up on [twitter](https://twitter.com/harper/) or [email](mailto:harper@nata2.org).
