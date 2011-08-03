from django.db import models
import time 
import signal
import threading
DEFAULT_RESPONSE = 'Merci d avoir envoyer un sms a Gnokki DAKAR'
class SMS(models.Model):
      '''
      Model pour garder les sms recus de gnokii
          * date: date de reception du sms
          * identity: Le numero de l'envoyeur
          * text: Le text du message
      '''
      date = models.DateTimeField(auto_now_add=True)
      identity =models.CharField(max_length=20)
      # Est ce que Gnokii tronque les sms 
      text = models.TextField(max_length =160)
      def __unicode__(self):
          return "<SMS %s %s>"%\
            (self.identity, self.text)

class Handler(object):
      def __init__(self,api, model=None):
	  '''
	  Class receiver, recoit et sauvegarde les sms dans la base
	  def donnees
	    * api:gnokii instance,encapsule le bagage pour l'envoi
	    et la reception des sms.
	    * model:  model de donnees, pour la sauvegarde dans
	      une base, de ce fait on pourra lire les sms via django admin,
	      ou via un autre UI WEB
	  '''
	  self.api = api
	  self.M= model or SMS
      
      def handle(self, sms, identity):
	  '''
	  Traitement du sms recus, vous en faites ce que vous voulez
	  '''
	  # Mettre le sms dans une base de donnee
	  # par exemple est une tres bonne idee, on y accedera via django views
	  m = self.M(text = sms, identity = identity)
	  m.save()
	  # Envoie une response 
	  self.api.send(sms ='',to=identity)


class Reader(threading.Thread): 	
      ''' Utilise un Trhead pour demarrer Gnokii smsreader '''
      def __init__ (self):
          threading.Thread.__init__(self)
      
      def run(self):
          print 'Running Gnokii ...'
          self.proc= Popen(['gnokii --smsreader'], shell =True,
                           stdin=PIPE, stdout=PIPE ,stderr=PIPE)
          self.proc.wait()
          
      def stop(self):
          # Arreter le processus SMSREADER, je ne sais
	  # pourquoi mais l'implementation de ADAM MCKAIG
          # le processus Attend, mais indefiniment
	  # __smsreader_killer() est un fix
          smsreader_killer()

from pyinotify import *
from  subprocess import *
class Api:
     '''
     Api Gnokii
     '''
     def __init__(self):
         self.handler =Handler(self)
         self.th  =Reader()
     
     class NotifyEvent(ProcessEvent):         
	  def process_IN_CREATE(self,event):
                f  =open('%s/%s'% (event.path, event.name))
                # Handle  incoming sms
		# Le message text est le contenu du fichier                
		print 'I got an SMS'		
		sms =f.read()
		
	
                
		# Le numero de Telephone est dans le nom
		# du fichier stocke dans le dossier /tmp/sms
		# le format est du genre sms_phone_numer_int
                identity =event.name.split("_")[1][3:]           
		self.handler.handle(sms, identity)
     
                     
        
     def receiver(self):
         # Gnokii ne cree pas ce dossier par defaut, lorsque il demarre
         # si le dossier n'existe pas ,creeons le ?
         sms_dir = '/tmp/sms'
         if not os.path.isdir(sms_dir):
            os.mkdir(sms_dir)

         # Ici commence le monitoring des sms
         # recus par le modem
         # Mon Modem est un HUWAWEI EC1152(ORANGE SENEGAL)
         # J'utilise Ubuntu 10.10 
         # le port  est /dev/ttyUSB1
         # Note : Gonkii peut envoyer des sms via le port ttyUSB
         # , mais la reception ne peut se faire que Via ttyUSB1
         # si vous utilisez un autre modem(Nokia telephone)
         # regardez dans le fichier .config de Gnokii pour la configuration
         # Mettre model =AT, pour les modems de type USB
         # dans le fichier de configuration
         # Dans le fichier de configuration configure la reception
         # des sms dans le dossier /tmp/sms, si il n'exist pas gnokii le cree t-il, non!
         try:
             wm = WatchManager()
             # Definssions un ecouteur sur /tmp/sms
             # et ajoutons lui le handler
	     nv =self.NotifyEvent(Stats())
             nv.handler =self.handler
             self.te = ThreadedNotifier(
                     wm,
                     nv,
                     )
             wm.add_watch(sms_dir, IN_CREATE)
             self.te.deamon =True
             self.te.start()
         except Exception, e:
              print 'Error Starting to monitor incoming message'
              print e
         else:
	     print "Receiving message started"

     def _kill(self):
             # Tue le processus gnokii smsreader
             self.th.stop()
             # Tue le processus de notification,(tmp/sms/)
             self.te.stop()
        
     def send(self, to, sms):
          # Send a message to a user
          self.th.stop()
          sms =sms or DEFAULT_RESPONSE
          print '===SENDING SMS==='
          out ,err =Popen(['gnokii --sendsms $0', to], shell =True,
                          stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate(sms)
	  print out
	  print err
          time.sleep(1)
          self.th =Reader()
          self.th.setDaemon(True)
          self.th.start()
          

def smsreader_killer():
    '''
    Tue le processus smsreader, gnokii ne permet pas 
    d'executer les deux processus sur le port ttyUSB1
    '''		
    import os
    
    # Track tous les processus Gnokii en cours d'executions
    lines =os.popen('ps -aux | grep gnokii').readlines()
    for l in lines:
	# Le processus est t'il un smsreader, 
	# SI oui, nous le stoppons le temps d'envoyer un 
	# SMS
        if 'sms' in l:
	   pid  =l.split()[1]
	   # signal.SIGINT ne semble pas arrerter smsreader pour 
	   # mon cas? 
           os.kill(int(pid), signal.SIGTERM)
          
