# api/views.py
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
# app/views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives, send_mail

class MailSenderT(APIView):
    def post(self, request):
        
        # İstersen request.body/POST içinden al
        to = 'alihan.eymirli@alapala.com'
        subject = 'Test Maili'
        username = 'Alihan'

        # Düz metin ve HTML içeriği
        text_content = f"Merhaba {username},\nBu bir test mailidir."
        html_content = f"<h2>Merhaba {username}</h2><p>Bu <strong>Arge Portal</strong> üzerinden gönderilen bir test mailidir.</p>"

        try:
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                None,               # from_email ayarları settings'ten alınır DEFAULT_FROM_EMAIL varsa None bırakılabilir
                [to],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
