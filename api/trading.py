import json
import requests

TRADELOCKER_REFRESH_URL = 'https://demo.tradelocker.com/backend-api/auth/jwt/refresh'
TRADELOCKER_ORDER_URL = 'https://demo.tradelocker.com/backend-api/trade/accounts/486567/orders'
REFRESH_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0cmFkZWxvY2tlci1hcGkiLCJhdWQiOiJ0cmFkZWxvY2tlci1hcGktdHJhZGVycyIsInR5cGUiOiJyZWZyZXNoX3Rva2VuIiwic3ViIjoiRlBJUFMjZTNjNDgwMDItNDJjNS00NWM2LWEwMGItZGQ5ODU3YmU4MWUxIiwidWlkIjoiZTNjNDgwMDItNDJjNS00NWM2LWEwMGItZGQ5ODU3YmU4MWUxIiwiYnJhbmQiOiJGUElQUyIsImlhdCI6MTcxNTcwMTYwMSwiZXhwIjoxNzE2MzA2NDAxfQ.k1eQbJouIdY_ilogCWLv6YTMsd0cjsirkiBZQmvGvsiT-Lvc8VO7JZumQ_KeyJ2U1oIHJ2qwh2id_NCW7eAk55SlLpqssgOO1QGOaJ4m1knrGhvJUt5pvJrOOjlZhbuJg0VbJ51ACCoQKVYPL_v7Gv6Ky3B3sl47Ysh553TWXHagODA64V287KhxQySgSm_HwQBA4W7JBP4gfIONnq2lv4soJglE7hr-d8ygb8L30x0Y20lxnijl7TaT3lfqtf-CpVVkBQ-f6vAMwsWGqUdLWsDtJSnGn5gTDQLLqTZcW_v1KVPqvG4wrtmANoknUYuLPpjh3If-g14S9SqO6qRldA'

def handler(request):
    body = request.json()
    qty = body.get('qty')
    side = body.get('side')

    if not qty or not side:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid data')
        }

    # Получение нового токена
    refresh_response = requests.post(
        TRADELOCKER_REFRESH_URL,
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json={'refreshToken': REFRESH_TOKEN}
    )

    if refresh_response.status_code != 200:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error refreshing token: {refresh_response.text}')
        }

    access_token = refresh_response.json().get('accessToken')

    if not access_token:
        return {
            'statusCode': 500,
            'body': json.dumps('No access token received')
        }

    # Отправка торгового ордера
    order_response = requests.post(
        TRADELOCKER_ORDER_URL,
        headers={
            'accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'accNum': '1',
            'Content-Type': 'application/json'
        },
        json={
            'qty': qty,
            'routeId': 318101,
            'side': side,
            'validity': 'IOC',
            'type': 'market',
            'tradableInstrumentId': 238
        }
    )

    if order_response.status_code != 200:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error placing order: {order_response.text}')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Order placed successfully')
    }
