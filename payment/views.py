from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse

def get_supported_currencies():
    headers = {
        'x-api-key': settings.NOWPAYMENTS_API_KEY
    }
    response = requests.get('https://api.nowpayments.io/v1/currencies', headers=headers)
    if response.status_code == 200:
        return response.json()['currencies']
    return []

def create_payment(request):
    if request.method == 'POST':
        # Get the payment amount and currency from the request
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        pay_currency = request.POST.get('pay_currency')

        # Prepare the request payload
        payload = {
            'price_amount': amount,
            'price_currency': currency,
            'pay_currency': pay_currency,
            'ipn_callback_url': 'https://yourwebsite.com/ipn/',  # IPN URL
            'order_id': '12345',  # Your custom order ID
            'order_description': 'Order description here'
        }

        # Send the request to NOWPayments
        headers = {
            'x-api-key': settings.NOWPAYMENTS_API_KEY
        }
        response = requests.post('https://api.nowpayments.io/v1/invoice', json=payload, headers=headers)

        # Process the response
        if response.status_code == 200:
            response_data = response.json()
            return redirect(response_data['invoice_url'])
        else:
            return JsonResponse(response.json(), status=response.status_code)
    
    # Fetch supported cryptocurrencies
    supported_currencies = get_supported_currencies()
    return render(request, 'pay/create_payment.html', {'supported_currencies': supported_currencies})




@csrf_exempt
def ipn(request):
    if request.method == 'POST':
        data = request.POST
        # Process the IPN data here (e.g., update order status)
        print(data)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)