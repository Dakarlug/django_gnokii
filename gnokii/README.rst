Django_gnokii est une toute petite application Gnokii qui est encapsule 
par une application Django. L'idee a la base etait de creer un systeme
de monitoring SMS tres leger au dessus de Gnokii avec un WEB UI Django/JQuery
Django_Gnokii poll les sms recus,envoi un accuse de Reception, et 
affiche en temps reel les SMS sur le WEB UI.

Vous pouvez Demarrer django_gnokii de facon tres simple 
  >>> from django_gnokii import gnokii
  >>> gnokii.run()
     Starting Gnokki, crl+C for stop
     Running Gnokii ... 
     Receiving message started




Puis vous pouvez envoyer un SMS a votre Modem.django_gnokii
stockera le sms recu dans une base, puis accessible depuis
le WEB UI.
  >>> python manage.py runserver
      Development server is running at http://127.0.0.1:8000/


  
================MODEM===================

django_gnokii utilise un modem HUAWEI MOBILE (Modem vendu par Orange) a 10000 FCFA.
Gnokii accpete la reception des sms via le port ttyUSB1.Donc si vous
devez utiliser une application comme django_gnokii, utilisez le port ttyUSB1, vous
pourrez combiner l'envoi et la reception.
     >>> model =AT
     >>> port  =ttyUSB1
     >>> sms_inbox = /tmp/sms
=================SYTEM==================

django_gnokii est teste avec la version Ubuntu 10.10, mais 
je ne vois pas une raison pour que cela ne fonctionne pas 
avec d'autres distributions.

================ AUTHORS ===============
django_gnokii est base sur une implementation de gnokii de
Adam MCkaig(UNICEF), je l'ai un peu bidouille afin de
l'adatpter a mes besions, mais egalement fixer quelques bugs
.Je vous serais reconnaissant de tester et de fixer, puis 
de m'envoyer les rapports d'erreurs a dia.aliounes@gmail.com



