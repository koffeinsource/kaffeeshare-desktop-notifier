#!/usr/bin/env python3

import logging
import argparse
import time
import urllib.request
import json
from gi.repository import Notify
#import pynotify  # deprecated


logging.basicConfig(level=logging.DEBUG)


class Indicator:
  def __init__(self, refresh, url):
    self.refresh = refresh
    self.url = url
    self.last_url = ''

  def check_site(self):
    raw_data = urllib.request.urlopen(self.url).read()
    #print(raw_data)
    parsed = json.loads(raw_data.decode())
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    top_url = parsed['Items'][0]['url']
    top_caption = parsed['Items'][0]['caption']
    logging.info("Top url: %s", top_url)
    assert top_url
    if not self.last_url or self.last_url != top_url:
      self.last_url = top_url
      self.show_notification(top_caption)

  def show_notification(self, body):
    app_name = "Kaffeeshare Notifier"
    Notify.init(app_name)
    summary = "New on Kaffeeshare"
    notification = Notify.Notification.new(summary, body, 'dialog-information')
    notification.show ()

  def run(self):
    while True:
      try:
        self.check_site()
      except Exception:
        logging.exception("Could not get data from Kaffeeshare")
      time.sleep(self.refresh)  # secs


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Kaffeshare Notifier",
     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-r", "--refresh", type=int, default=60, help="refresh inteval [seconds]")
  parser.add_argument("URL", nargs='?', help="Resource URL")
  
  args = parser.parse_args()
  try:
    indicator = Indicator(args.refresh, args.URL)
    indicator.run()
  except KeyboardInterrupt:
    print("\nAborted Kaffeshare Notifier")

