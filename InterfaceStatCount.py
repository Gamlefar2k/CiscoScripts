import csv
import re

commands = (
  "show int status | inc Gi|Te|Tw|Po",
  "show int count | inc Gi|Te|Tw|Po"
)

def main():
  data = {}

crt.GetScriptTab().Screen.Send("\r")
hostname = crt.GetScriptTab().Screen.ReadString("#")
