from pyawair import awair

if __name__ == "__main__":
    import datetime

    username = "email@gmail.com" #The email you use to login to Awair
    password = "very long and secure password" #The secure password you use to login to awair

    api =  awair(username, password) #Let's authenticate

    devices = api.devices() #Grab the devices that are on your account

    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)

    for device in devices:  #Let's iterate through devices
      print(device) #Print the device

      print("Let's grab the weather")
      print(api.weather(latitude=device['latitude'], longitude=device['longitude']))

      print("Timeline from yesterday to today")
      # The date input is parsed by arrow and converted into the correct format
      print(api.timeline(device, from_date=yesterday.isoformat(), to_date=today.isoformat()))

      print("Event score")
      print api.events_score(device)

      inbox = api.inbox_items(device, limit=10)
      for message in inbox:
        print(message)

