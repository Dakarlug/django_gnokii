# Create your views here.
from .models import SMS as S
from django.core import serializers
from django.shortcuts import render_to_response
from django.http import HttpResponse
'''
Pour afficher les SMS recus par Gnokii, nous allons
appeler cette vue chaque quelques secondes via jQuery,la
page de rendue dans /templates/sms.html doit donc
contenir un bout de code pour appeler cette vue .
nous y mettons le code suivant.
<!DOCTYPE html>
     <html lang="en">
     <head>
       <meta charset="utf-8">
       <title>Gnokii-DJANGO-SMS</title>
     </head>
     <style type="text/css">
        body { 
             font-family: arial, verdana, sans-serif;
             font-size: 12px; }
     </style>
 <body>
   <div>Polling SMS FROM GNOKII each 10 seconds </div>
   <!--script src="/js/jquery.min.js"></script-->
   <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js" type="text/javascript"></script>
   <script>
         function  __to_html(data){
            items = []
            $.each(data, function(key, sms) {
                items.push('<li id="' + key + '">'+ sms.fields.identity + '  >>  '+ sms.fields.text + '</li>');
            });
            $('ul').html(items.join(''));
         }
         function polling(){
           jQuery.ajax({
                type: "GET",
                url: 'poll/',
                dataType: "json",
                success:__to_html,
                error:function(XMLHttpRequest, textStatus, errorThrown){
                    alert(XMLHttpRequest.responseText);
                }
            });
            setTimeout("polling()", 5000);
      }
      $(document).ready(
           setTimeout("polling()", 5000)
      );
   </script>
   <div><ul></ul></div>
 </body>
 </html>
'''
def __index(req):
    data = S.objects.all()
    if req.path=='/poll/':
        json_sms = serializers.serialize(
            "json",
            S.objects.all())
        return HttpResponse(
            json_sms,
            mimetype ='application/json')
    return render_to_response(
		'sms.html',
		{'data':data})


def __find_sms(sender):
    # Retourne les sms qui ont ete recus par Gnokii
    # en provenance du numero de Telephone
    # *sender:le numero de TelePhone qui a envoye le message.
    return S.objects.filter(indentity = sender)
