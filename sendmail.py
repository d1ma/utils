from getpass import getpass
import smtplib
import sys,os

def send_email(recipient, subject, msg, confirm=False):
	sender = from_email
	content = prefix % (recipient, from_email, subject,  msg)
	try:
		print 'Sending to %s from %s' % (recipient, sender)
		print 'Content:\n%s' % content
		if confirm:
			raw_input('Confirmation set to true, Press Enter to continue')
		smtp = smtplib.SMTP('cs.stanford.edu')
		smtp.sendmail(sender, [recipient], content)
	except Exception, ex:
	 	print 'Unable to send mail to %s. %s' % (recipient, str(ex))



confirm = False
from_email = ""
template_file = ""
student_file = ""
subject = ""

if (len(sys.argv) == 1):
	print 'USAGE: python sendmail.py you@cs.stanford.edu template_file tuples_file subject [Confirm?]'

if len(sys.argv) > 1:
	from_email = sys.argv[1]
else:
	from_email = raw_input('Enter cs email: ')

if (len(sys.argv) > 2):
	template_file = sys.argv[2]
else:
	template_file = raw_input('Enter template: ')

if (len(sys.argv) > 3):
	student_file = sys.argv[3]
else:
	student_file = raw_input('Enter tuples file: ')

if (len(sys.argv) > 4):
	subject = sys.argv[4]
else:
	subject = raw_input('Enter email subject: ')


if (len(sys.argv) > 5):
	confirm = sys.argv[5] == 'Confirm'
else:
	confirm = (raw_input('Type Confirm to confirm') == 'Confirm')

prefix = 'To: %s\nFrom: %s\nSubject: %s\n%s'

for fname in [student_file, template_file]:
	if not os.access(fname, os.R_OK):
		print "could not open file %s, exiting" % fname
		sys.exit(1)

''' READ TEMPLATE '''
template_f = open(template_file)
template = template_f.read()
template_f.close()
print 'Template read:\n%s' % template
raw_input('Press enter to continue')

''' READ STUDENTS '''
student_f = open(student_file)
student_lines = student_f.readlines()
student_f.close()
student_tuples = map(lambda line: tuple(line.split(',')), student_lines)

sent_file = 'sent_log.txt'
sent_f = open(sent_file, 'a')

''' SEND '''
for i, student in enumerate(student_tuples):
	msg = template % (student[1], str(student[2]))
	send_email(student[0], subject, msg, confirm)
	print str(i) + ': Sent %s\n' % (str(student))
	sent_f.write(str(student) + '\n')
sent_f.close()
