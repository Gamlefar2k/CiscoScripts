# $language = "python"
# $interface = "1.0"

#  Description:
#  The basis for this script is proudly copied from Vandyke.com and modified.
#  It will when executed in SecureCRT from EXEC mode on a switch run the listed
#  commands and paste the output to the systems clipboard.

SCRIPT_TAB = crt.GetScriptTab()
SCRIPT_TAB.Screen.Synchronous = True

commands = [
"show run",
"show cdp nei",
"show lldp nei",
"show int status",
"show int status",
"show power in",
"show etherch su",
"show ver | inc upt"] 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():

	if not crt.Session.Connected:
		crt.Dialog.MessageBox(
			"This script currently requires a valid connection to a "
			"Cisco device.\n\n"
			"Please connect and then run this script again.")
		return

	crt.Screen.Synchronous = True

	if not SendExpect("term len 0", "#"):
		return

	hostname = CaptureOutputOfCommand("show run | inc hostname","#")[10:]
	data = hostname
	#data = hostname[:len(hostname)//2]

	for command in commands:
		output = CaptureOutputOfCommand(command, "#")
		data += ('\r') + command + ('\r') + output

	crt.Clipboard.Format = "CF_UNICODETEXT"
	crt.Clipboard.Text = data

	if not SendExpect("term len 25", "#"):
		return

	crt.Dialog.MessageBox(
		"Success! Text is now in the clipboard")
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SendExpect(send, expect):

	if not SCRIPT_TAB.Session.Connected:
		return

	SCRIPT_TAB.Screen.Send(send + '\r')
	SCRIPT_TAB.Screen.WaitForString(expect)

	return True


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CaptureOutputOfCommand(command, prompt):
	if not crt.Session.Connected:
		return "[ERROR: Not Connected.]"
	
	SCRIPT_TAB.Screen.Send(command + '\r')
	SCRIPT_TAB.Screen.WaitForString('\r')

	return SCRIPT_TAB.Screen.ReadString(prompt)

main()
