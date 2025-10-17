# 1) Register
curl -s -X POST http://localhost:8000/register \
  -H 'content-type: application/json' \
  -d '{"email":"a@b.com","password":"password123"}'

# 2) Login (grab the token)
TOKEN=$(curl -s -X POST http://localhost:8000/login \
  -H 'content-type: application/json' \
  -d '{"email":"a@b.com","password":"password123"}' | jq -r .access_token)
echo "TOKEN=$TOKEN"

# 3) Produce to Kafka
curl -s -X POST http://localhost:8000/produce \
  -H "authorization: Bearer $TOKEN" -H 'content-type: application/json' \
  -d '{"text":"hello kafka"}'

# 4) Read messages (persisted by the consumer)
curl -s -H "authorization: Bearer $TOKEN" http://localhost:8000/messages | jq