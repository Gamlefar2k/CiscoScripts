import re
import os
import time

# User credentials
username = "username"
password = "password"
enable_pass = "enable password"

# Commands to execute
commands = [
    "show running-config | include hostname",
    "show interfaces status"
]

def main():
    # Read hostnames from the clipboard
    strClipboard = crt.Clipboard.Text
    hostnames = strClipboard.splitlines()

    for hostname in hostnames:
        # Open a new tab and connect to the session using Telnet
        tab = crt.Session.ConnectInTab(f"/TELNET {hostname}")
        tab.Screen.Send("\n")

        # Wait for the login prompt and enter the username
        if tab.Screen.WaitForString("Username:", 5):
            tab.Screen.Send(username + "\n")
        else:
            crt.Dialog.MessageBox(f"Login prompt not found for {hostname}")
            tab.Session.Disconnect()
            continue
        
        # Wait for the password prompt and enter the password
        if tab.Screen.WaitForString("Password:", 5):
            tab.Screen.Send(password + "\n")
        else:
            crt.Dialog.MessageBox(f"Password prompt not found for {hostname}")
            tab.Session.Disconnect()
            continue
        
        # Wait for the command prompt, either EXEC mode '>' or privileged EXEC mode '#'
        prompt = tab.Screen.WaitForStrings([">", "#"], 5)
        
        if prompt == 0:
            crt.Dialog.MessageBox(f"Failed to get command prompt for {hostname}")
            tab.Session.Disconnect()
            continue
        elif prompt == 1:
            # Not in privileged EXEC mode, enter enable mode
            tab.Screen.Send("enable\n")
            if tab.Screen.WaitForString("Password:", 5):
                tab.Screen.Send(enable_pass + "\n")
                if not tab.Screen.WaitForString("#", 5):
                    crt.Dialog.MessageBox(f"Enable command failed for {hostname}")
                    tab.Session.Disconnect()
                    continue
            else:
                crt.Dialog.MessageBox(f"Enable password prompt not found for {hostname}")
                tab.Session.Disconnect()
                continue
        elif prompt == 2:
            crt.Dialog.MessageBox(f"Logged in successfully to {hostname} with privileged EXEC mode")

        # Open a text file to save the output
        with open(f"{hostname}.txt", "w") as output_file:
            for command in commands:
                # Send the command
                tab.Screen.Send(command + "\n")
                
                # Capture the output until the next prompt
                if tab.Screen.WaitForString("#", 5):
                    output = tab.Screen.ReadString("#")
                    
                    # Write the output to the file
                    output_file.write(f"Command: {command}\n")
                    output_file.write(output)
                    output_file.write("\n\n")
                else:
                    crt.Dialog.MessageBox(f"Command prompt not found after {command} for {hostname}")

        # Disconnect the session
        tab.Session.Disconnect()

main()
