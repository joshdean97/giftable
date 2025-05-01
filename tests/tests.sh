#!/bin/bash

base_url="http://localhost:5000"
giftcards_endpoint="$base_url/api/giftcards"

# --- Helper: Extract a JSON field value manually
extract_field() {
  echo "$1" | grep -o "\"$2\": *[^,}]*" | sed -E "s/\"$2\": *\"?([^\",}]*)\"?/\1/"
}

# Test 1: Check if server is running
echo "🔎 Checking if server is running at $base_url ..."
response=$(curl -s -o /dev/null -w "%{http_code}" "$base_url")
if [ "$response" -ne 200 ]; then
    echo "❌ Server not running (HTTP $response)"
    exit 1
else
    echo "✅ Server running (HTTP $response)"
fi

# Test 2: Get all gift cards
echo "🔎 Fetching all gift cards..."
response=$(curl -s -o /dev/null -w "%{http_code}" "$giftcards_endpoint/")
if [ "$response" -ne 200 ]; then
    echo "❌ Failed to get gift cards (HTTP $response)"
    exit 1
else
    echo "✅ Gift cards fetched (HTTP $response)"
fi

# Test 3: Create a new gift card
echo "🆕 Creating a new gift card..."
create_response=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"balance": 100}' \
  )

if ! echo "$create_response" | jq . >/dev/null 2>&1; then
    echo "❌ Invalid JSON response. Full response:"
    echo "$create_response"
    exit 1
fi

code=$(echo "$create_response" | jq -r '.code // empty')

if [ -z "$code" ]; then
    echo "❌ Failed to extract gift card code. Full response:"
    echo "$create_response"
    exit 1
else
    echo "✅ Gift card created with code: $code"
fi

# Test 4: Check balance
echo "💰 Checking balance for gift card $code..."
balance_response=$(curl -s "$giftcards_endpoint/$code/")
balance=$(extract_field "$balance_response" "balance")

if [ -z "$balance" ]; then
    echo "❌ Could not fetch balance. Response:"
    echo "$balance_response"
    exit 1
else
    echo "✅ Gift card has balance: £$balance"
fi

# Test 5: Redeem £25
echo "💸 Redeeming £25 from gift card $code..."
redeem_response=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"amount": 25}' \
  "$giftcards_endpoint/redeem/$code/")

new_balance=$(extract_field "$redeem_response" "new_balance")

if [ -z "$new_balance" ]; then
    echo "❌ Redeem failed. Response:"
    echo "$redeem_response"
    exit 1
else
    echo "✅ £25 redeemed. New balance: £$new_balance"
fi

# ✅ Done
echo ""
echo "🎉 All tests completed successfully."
