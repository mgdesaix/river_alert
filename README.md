# river_alert


NOAA provides  [water gauge data](https://water.weather.gov/ahps/) that paddlers use to know when conditions are good. Here in Richmond the James River has been low lately and I want to know when its predicted to be high enough to get exciting. 

Here's a couple of quick Python scripts: 1) to email gauge data for that day of locations I'm interested in; 2) check every 6 hours to see if water level is above certain threshold, then email

There's more efficient platforms to do this, but this is made pretty quick with the requests, BeautifulSoup, and smtplib libraries.
