#!/bin/bash
# Quick Auth API Test Script

BASE_URL="http://localhost:8000"

echo "🚀 Testing Authentication APIs"
echo "================================"
echo ""

# Test 1: Register
echo "1️⃣  Registering user..."
REGISTER=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "quicktest", "email": "quick@test.com", "password": "test123", "full_name": "Quick Test"}')
echo "$REGISTER" | python3 -m json.tool 2>/dev/null || echo "$REGISTER"
echo ""

# Test 2: Login
echo "2️⃣  Logging in..."
LOGIN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "quicktest", "password": "test123"}')
TOKEN=$(echo "$LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
echo "$LOGIN" | python3 -m json.tool 2>/dev/null || echo "$LOGIN"
echo ""

# Test 3: Get Current User
if [ ! -z "$TOKEN" ]; then
  echo "3️⃣  Getting current user (with token)..."
  curl -s -X GET "$BASE_URL/api/auth/me" \
    -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null
  echo ""
fi

echo "✅ Quick test completed!"
echo ""
echo "💡 Tip: Open http://localhost:8000/docs for interactive testing"
