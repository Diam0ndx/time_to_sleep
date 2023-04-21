import os
import sys
import time
import datetime
from urllib.error import URLError
from urllib.request import urlopen
import ctypes #for admin permissions

to_sleep=2

def get_the_time():
	try:
		with urlopen("http://just-the-time.appspot.com") as res:
			global today, clock, hours, minutes, seconds, to_sleep
			res = res.read().strip().decode("utf-8") #result from the website
			today = str(res[:11])
			clock = str(res[11:]) #return the clock only
			print(f"the date is: {today} \nand the time is: {str(int(clock[:2])+2)+str(clock[2:])} \n")
			hours = int(clock[:2]) #it is 2 hours late
			minutes = int(clock[-5:-3])
			seconds = int (clock[-2:])
			time_tuple = ( int(res[0:4]), # Year
                  int(res[5:7]), # Month
                  int(res[8:10]), # Day
                  int(res[11:13]), # Hour
                  int(res[14:16]), # Minute
                  int(res[-2:]), # Second
                  0, # Millisecond
              )
			#print(datetime.date(int(today)).isocalendar())
			#print( datetime.date("-".join(time_tuple[0:3])).isocalendar())
			try:
				if sys.platform == "win32":
				    import pywintypes
				    import win32api
				    #for admin permissions
				    #ctypes.windll.shell32.ShellExecuteW(
                    #           None, 'runas', sys.executable, ' '.join(sys.argv), None, None)
				    
			        # pywin32.SetSystemTime(year, month , dayOfWeek , day , hour , minute , second , millseconds )
				    dayOfWeek = (datetime.date(int(res[0:4]),int(res[5:7]), int(res[8:10])).isocalendar()[2], )
				    win32api.SetSystemTime(*time_tuple[:2] , *dayOfWeek , *time_tuple[2:])
				    exit(0)
			except pywintypes.error:
				print("seems like there is no permissions to change the time\n")


								

	except URLError:
		if to_sleep<30:
			to_sleep*=2
		print("no internet connection :/")
		time.sleep(to_sleep)
		get_the_time()


def main(): #to check the time
	get_the_time()
	if hours >= 19 or hours <=4:
		print("it is so late man, sorry but you have to sleep right now, but it's okey, come back later 🤗")
		print("Turn off")
		os.system("shutdown /s /t 60")
	else:
	   left_min = 59 - minutes
	   left_hours = 18 - hours
	   left_seconds = 59 - seconds
	   if (left_hours * 3600 + left_min*60 + left_seconds) > 0:
	        left_time = left_hours * 3600 + left_min*60 + left_seconds
	   else:
	        left_time = 60
	   print(f"the time that left to play is {left_time//3600} hours and {int(left_time%3600/60)} minutes, and you will be warrned 2 min before it")
	   print("enjoy")
	   command = f"shutdown /s /t {left_time} "
	   os.system(command)

	
main()
input("\npress any key to close the screen")
#todo:close = warning + turn off