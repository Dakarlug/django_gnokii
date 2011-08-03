import time
import signal
def run():
    print 'Starting Gnokki, crl+C for stop'
    from .models import Api
    api =Api()
    # Receiving SMS
    api.th.setDaemon(True)
    api.th.start()
    api.receiver()
    while 1:
          try:
             time.sleep(1)
          except KeyboardInterrupt, e:
             break
    print 'Gnokii stopped'

