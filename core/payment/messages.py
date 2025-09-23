def get_confirmation_message(method, order_id, lang='en'):
    messages = {
        'mpesa': {
            'en': f"STK push sent for Order #{order_id}. Please complete payment on your phone.",
            'sw': f"Malipo ya M-Pesa kwa Order #{order_id} yameanzishwa. Tafadhali kamilisha kwenye simu yako."
        },
        'airtel': {
            'en': f"Airtel Money payment initiated for Order #{order_id}.",
            'sw': f"Malipo ya Airtel Money kwa Order #{order_id} yameanzishwa."
        },
        'paypal': {
            'en': f"Redirecting to PayPal for Order #{order_id}.",
            'sw': f"Unaelekezwa kwa PayPal kwa Order #{order_id}."
        },
        'bank': {
            'en': f"Bank transfer instructions generated for Order #{order_id}.",
            'sw': f"Maelezo ya uhamisho wa benki kwa Order #{order_id} yametolewa."
        }
    }
    return messages.get(method, {}).get(lang, "Payment method not recognized.")
