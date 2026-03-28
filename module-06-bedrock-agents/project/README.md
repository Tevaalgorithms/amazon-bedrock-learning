# Module 06 Project — Customer Service Agent

## Goal

Build a customer service agent with 2 action groups:
1. **Order Lookup** — get customer orders
2. **FAQ** — answer common questions

## Architecture

```
User Query
    ↓
Agent (Claude)
    ↓
├─→ order_lookup_lambda (if asking about orders)
│    └─→ Returns order data
│
└─→ faq_lambda (if asking about policies)
     └─→ Returns FAQ answers
    ↓
Agent generates response with results
```

## Implementation

1. **Create 2 Lambda functions**
   - `order-lookup-handler` — returns mock orders
   - `faq-handler` — returns FAQ answers

2. **Create Agent** with 2 action groups pointing to Lambdas

3. **Create Agent Alias** for deployment

4. **Invoke and test**

## Starter Code

```python
import boto3

bedrock_agent = boto3.client('bedrock-agent')
bedrock_runtime = boto3.client('bedrock-agent-runtime')

# TODO: Create agent
# TODO: Add 2 action groups
# TODO: Create alias

# TODO: Invoke agent
response = bedrock_runtime.invoke_agent(
    agentId='agent-123',
    agentAliasId='prod',
    sessionId='customer-456',
    inputText='What was my last order?'
)
```

## Test Cases

- "Show me my orders" → calls order_lookup
- "What's your return policy?" → calls faq
- "What was my last order and when can I return it?" → calls both
