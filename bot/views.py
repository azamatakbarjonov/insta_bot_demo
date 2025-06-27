from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

VERIFY_TOKEN = 'azambot_token'
PAGE_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse('Verification failed', status=403)

    elif request.method == 'POST':
        data = json.loads(request.body)
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                value = change.get('value', {})
                if value.get('field') == 'messages':
                    message = value.get('messages', [])[0]
                    sender = message.get('from')
                    text = message.get('text', {}).get('body', '').lower()
                    reply = handle_auto_reply(text)
                    send_message(sender, reply)
        return HttpResponse("OK", status=200)

def handle_auto_reply(text):
    if 'salom' in text:
        return "Salom! BZA Osh Markaziga hush kelibsiz 😊"
    elif 'menyu' in text:
        return "Menyuni ko‘rish: https://bza.uz/menu"
    elif 'buyurtma' in text:
        return "Buyurtma: https://bza.uz/book"
    else:
        return "Savolingiz uchun rahmat. Tez orada javob beramiz."

def send_message(sender_id, message_text):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": message_text}
    }
    requests.post(url, headers=headers, data=json.dumps(payload))
