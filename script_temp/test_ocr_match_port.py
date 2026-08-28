import requests, os, json

test_dir = r'D:\Code2026\tcg-embedding-service\test-images'
files = [f for f in os.listdir(test_dir) if f.endswith('.jpg')]
if not files:
    print('No test images found')
    exit(1)

test_img = os.path.join(test_dir, files[0])
print('Testing with:', files[0])

with open(test_img, 'rb') as f:
    resp = requests.post('http://localhost:8056/v1/ocr-match', files={'file': f}, timeout=30)

print('Status:', resp.status_code)
data = resp.json()
print('status:', data.get('status'))
print('query_text:', data.get('query_text', '')[:200])
results = data.get('results', [])
print('results count:', len(results))
for r in results[:3]:
    print('  #%d: %s %s score=%.4f has_image=%s' % (r['rank'], r['product_id'], r['product_name'][:50], r['score'], r['has_image']))

print()
print('Frontend test:')
resp2 = requests.get('http://localhost:8056/', timeout=5)
print('Frontend status:', resp2.status_code)
print('Frontend size:', len(resp2.text), 'chars')

if results:
    pid = results[0]['product_id']
    resp3 = requests.get('http://localhost:8056/v1/images/%s_200w' % pid, timeout=5)
    print('Image test: %s_200w -> status=%d size=%d bytes' % (pid, resp3.status_code, len(resp3.content)))
    if resp3.status_code == 404:
        resp4 = requests.get('http://localhost:8056/v1/images/%s_200w.jpg' % pid, timeout=5)
        print('Image test with .jpg: %s_200w.jpg -> status=%d size=%d bytes' % (pid, resp4.status_code, len(resp4.content)))
