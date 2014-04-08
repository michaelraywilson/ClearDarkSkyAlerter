#!/usr/bin/python

# to parse the csv file from site
import csv

# to download the url
import urllib

# to get color from pictures
from PIL import Image

# to pass args
import sys

# import to send mail
import smtplib
from email.mime.text import MIMEText

# if passed --debug, will display debug output
debug = 0


###
### Email functionality requires a SMTP server
# Replace XXXXXXXXXX with your email
##
##
receiver = 'XXXXXXXXXX@gmail.com'

##
# Replace XXXXXXXXX with the senders email
#
sender = 'XXXXXXXXX'
subject = 'Good Night To Stargaze Soon'

header = "From: " + sender + "\n" +  \
         "To: " + receiver + "\n" +  \
         "Subject: " + subject + "\n"

#
# Replace url to the URL you are checking
#
body = "The conditions are right to be able to view the skys in the next few days. See for yourself: http://cleardarksky.com/c/PwwwlObKScsk.gif"

message = header + body


if len(sys.argv) == 2:
	if str(sys.argv[1]) == '--debug':
		debug = 1

###
### Replace this with your own local area
###
insite = urllib.urlopen("http://cleardarksky.com/txtc/PwwwlObKScsp.txt")
file = open('dl.txt', 'w+')
file.write(insite.read())
file.close()

###
### Replace this with your local area gif
###
CCOpic = urllib.urlopen('http://cleardarksky.com/c/PwwwlObKScsk.gif')
filepic = open('cds.gif', 'w+')
filepic.write(CCOpic.read())
filepic.close()


alerted = 0
file = open('dl.txt', 'rb')
reader = csv.reader(file)
rownum = 0
x = 129
y = 125
square = 0

def getrgb(x,y):
	im = Image.open('cds.gif')
	rgb_im = im.convert('RGB')
	r, g, b = rgb_im.getpixel((x,y))
	if (r == 0 and g == 0 and b < 120):
		print 'Dark enough... colors:'
		print r, g, b
		return True; 
	else:
		print 'Not Dark enough... colors:'
		print r, g, b
		return False;

for row in reader:
	# only view data (not comments or legend)
	if row[0].startswith("("):
		square += 1
		# Check Cloud Cover (if cloud2 = 9 or 10)
		if "10" in row[1] or "9" in row[1]:
			# Check Transparency (if trans2 = 4 or 5)
			if "4" in row[2] or "5" in row[2]:
				# Check Seeing (if seeing2 = 4 or 4)
				if "4" in row[3] or "5" in row[3]:
					# Check Darkness
					good_darkness = (getrgb ((square*12) + x, y))
					if (good_darkness == True) and (alerted is not 1):
						# Everything Checks Out
						print 'ROW: %s' % (row)
						try:
						        # You could use a gmailer if you wanted
							#
							smtpObj = smtplib.SMTP('x.x.x.x')
						        smtpObj.sendmail(sender, receiver, message)
						        print "Sent mail..."
							alerted = 1
						except smtplib.SMTPException as error:
						        print "Error: unable to send email : {err}".format(err=error)
					elif (debug == 1):
						print 'Darkness: %s' % good_darkness
				elif debug == 1:
					print 'Seeing row[3]: %s : did not match!' % (row)	
			elif debug == 1:
				print 'Transparency row[2]: %s :did not match!' % (row)
		elif debug == 1:
			print 'Cloud Cover row[1]: %s :did not match!' % (row)
	rownum +=1


file.close() 


