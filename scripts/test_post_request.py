import requests

url = 'http://127.0.0.1:8000/ia/analizar'
payload = {'prompt': 'Resume tendencias principales y problemas en mis ventas'}

try:
    r = requests.post(url, json=payload, timeout=30)
    print('Status:', r.status_code)
    print('Response:', r.text[:2000])
except Exception as e:
    print('Error making request:', e)
