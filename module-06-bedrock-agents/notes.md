# Module 06 — Bedrock Agents

## What is an Agent?

An **agent** is a model that can decide what to do and use tools (action groups) to accomplish tasks.

```
User: "What was my last order?"
    ↓
Agent decides: "I need to look up orders"
    ↓
Agent calls: get_orders_tool(user_id)
    ↓
Tool returns: [Order#123, Order#456]
    ↓
Agent decides: "Return last order details"
    ↓
Response: "Your last order was #456 for $50"
```

## Agent Anatomy

1. **Model** — Claude 3 Haiku/Sonnet/Opus
2. **Agent Instructions** — what the agent is for, how to behave
3. **Action Groups** — functions the agent can call
4. **Lambda Functions** — backend for each action

## Creating an Agent

### Step 1: Define Action Groups

Action groups are functions the agent can invoke.

```json
{
    "actionGroupName": "order-lookup",
    "description": "Look up customer orders",
    "apiSchema": {
        "properties": {
            "customerId": {
                "type": "string",
                "description": "The customer ID"
            },
            "status": {
                "type": "string",
                "enum": ["pending", "shipped", "delivered"],
                "description": "Filter by order status"
            }
        },
        "required": ["customerId"]
    },
    "actionGroupExecutor": {
        "lambda": "arn:aws:lambda:us-east-1:...:function:lookup-orders"
    }
}
```

### Step 2: Create Lambda Handler

Lambda function that executes the action:

```python
def lambda_handler(event, context):
    """Lookup customer orders"""

    action_group = event['actionGroup']
    api_path = event['apiPath']
    http_method = event['httpMethod']

    parameters = event['parameters']  # From agent
    customer_id = parameters['customerId']

    # TODO: Lookup orders from database
    orders = [
        {'id': 'ORDER123', 'amount': 100},
        {'id': 'ORDER124', 'amount': 50}
    ]

    return {
        'statusCode': 200,
        'body': {'orders': orders}
    }
```

### Step 3: Create Agent

```python
bedrock_agent = boto3.client('bedrock-agent')

response = bedrock_agent.create_agent(
    agentName='customer-service-bot',
    agentArn='...',
    description='Helps customers with orders and FAQ',
    foundationModel='anthropic.claude-3-5-sonnet-20241022-v1:0',
    instruction='''You are a helpful customer service agent.
You can look up orders and answer common questions.
Always be polite and helpful.
If you don't know, say so.'''
)

agent_id = response['agent']['agentId']
```

### Step 4: Create Agent Alias (for deployment)

```python
response = bedrock_agent.create_agent_alias(
    agentId=agent_id,
    agentAliasName='prod'
)

agent_alias_id = response['agentAlias']['agentAliasId']
```

### Step 5: Invoke Agent

```python
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')

response = bedrock_agent_runtime.invoke_agent(
    agentId=agent_id,
    agentAliasId=agent_alias_id,
    sessionId='user-123',  # Track conversation
    inputText='What was my last order?'
)

# Stream response
for event in response['completion']:
    if 'chunk' in event:
        print(event['chunk']['bytes'].decode())
```

## Multi-Action Workflows

Agent can use multiple tools in sequence:

```
User: "Process my return for order #123"
    ↓
Agent: Call get_order(ORDER123) → returns order details
    ↓
Agent: Call initiate_return(ORDER123) → returns RMA number
    ↓
Agent: Call send_return_label(RMA_NUM) → returns shipping label
    ↓
Response: "Return initiated, RMA #RMA123, label sent to email"
```

## Session State

Track conversation state:

```python
session_id = 'customer-123'

# Turn 1
response = bedrock_agent_runtime.invoke_agent(
    agentId=agent_id,
    agentAliasId=agent_alias_id,
    sessionId=session_id,
    inputText='Show me my orders'
)

# Turn 2 (agent remembers context)
response = bedrock_agent_runtime.invoke_agent(
    agentId=agent_id,
    agentAliasId=agent_alias_id,
    sessionId=session_id,
    inputText='Which one is most recent?'  # Refers to previous orders
)
```

## Return of Control

Agent can pause and ask for confirmation:

```python
response = bedrock_agent_runtime.invoke_agent(...)

for event in response['completion']:
    if 'returnControl' in event:
        # Agent needs user input before proceeding
        control_data = event['returnControl']['invokingEvent']
        print(f"Agent needs: {control_data}")

        # User provides input
        user_input = input("> ")

        # Resume agent with user input
        response = bedrock_agent_runtime.invoke_agent(
            ...,
            inputText=user_input
)
```

## Code Interpreter

Agent can execute Python code:

```python
# In agent instructions:
'''You have access to a code interpreter.
Use it to calculate complex math, analyze data, or write code.
Provide the code and results to the user.'''

# Agent can now do:
# User: "What's 2^100?"
# Agent: "I'll use the code interpreter"
# Agent: python: print(2**100)
# Result: 1267650600228229401496703205376
```

## Guardrails Integration

Protect agent output:

```python
bedrock_agent_runtime.invoke_agent(
    agentId=agent_id,
    agentAliasId=agent_alias_id,
    sessionId=session_id,
    inputText='Question',
    guardrailConfiguration={
        'guardrailId': 'gr-123',
        'guardrailVersion': '1'
    }
)
```

## Costs

- Per invocation: Same as regular model call
- Lambda execution: Standard pricing
- Data transfer: Minimal

Example: 100 multi-action agent calls/day ≈ $1-2/month

## Gotchas

### 1. Lambda IAM Permissions
Lambda needs permissions to execute. Check trust relationship.

### 2. Timeout
Long-running tools can timeout. Set appropriate timeouts.

### 3. Tool Discovery
Agent needs clear tool descriptions. Vague descriptions = wrong tool selection.

### 4. Error Handling
Lambda must return properly formatted response, or agent fails.

## Next Steps

Module 06 project: Build customer service agent with 2 action groups.

## Resources

- **Agent Docs:** https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html
- **API Reference:** https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_InvokeAgent.html
