# Module 08 — Bedrock Flows

## What Are Bedrock Flows?

**Flows** are visual workflows that orchestrate models, knowledge bases, agents, and data processing using node-based composition.

## Architecture

```
Start Node
    ↓
Input Node (receives user question)
    ↓
Knowledge Base Node (retrieves documents)
    ↓
Condition Node (if good retrieval, proceed)
    ├─→ Yes: Prompt Node (generate answer)
    └─→ No: Fallback Node (ask for clarification)
    ↓
End Node (return response)
```

## Node Types

### 1. Input Node
Receives user input (text, document, etc)

```json
{
    "name": "user-input",
    "type": "INPUT",
    "configuration": {
        "inputVariableKey": "userQuestion"
    }
}
```

### 2. Prompt Node
Calls a model with a prompt

```json
{
    "name": "generate-answer",
    "type": "PROMPT",
    "configuration": {
        "modelId": "anthropic.claude-3-5-sonnet-20241022-v1:0",
        "systemPrompt": "You are a helpful assistant.",
        "userPrompt": "${userQuestion}"
    }
}
```

### 3. Knowledge Base Node
Retrieves from a KB

```json
{
    "name": "retrieve-docs",
    "type": "KNOWLEDGE_BASE",
    "configuration": {
        "knowledgeBaseId": "kb-123",
        "retrievalConfiguration": {
            "numberOfResults": 5
        }
    }
}
```

### 4. Agent Node
Invokes a Bedrock Agent

```json
{
    "name": "call-agent",
    "type": "AGENT",
    "configuration": {
        "agentId": "agent-123",
        "agentAliasId": "prod"
    }
}
```

### 5. Condition Node
Branches based on logic

```json
{
    "name": "check-retrieval",
    "type": "CONDITION",
    "configuration": {
        "conditions": [
            {
                "path": "retrievalScore",
                "operator": ">",
                "value": "0.8"
            }
        ]
    }
}
```

### 6. Iterator Node
Loops over a list

```json
{
    "name": "process-documents",
    "type": "ITERATOR",
    "configuration": {
        "itemsPath": "documents",
        "outputPath": "processedDocs"
    }
}
```

## Creating a Flow (Code)

```python
import boto3

bedrock_flows = boto3.client('bedrock-flows')

flow_definition = {
    'nodes': [
        {
            'name': 'input-node',
            'type': 'INPUT',
            'id': 'input-1',
            'outputs': [{'name': 'body'}]
        },
        {
            'name': 'prompt-node',
            'type': 'PROMPT',
            'id': 'prompt-1',
            'configuration': {
                'modelId': 'anthropic.claude-3-5-haiku-20241022-v1:0',
                'systemPrompt': 'You are helpful.',
                'userPrompt': '${input-1.body}'
            },
            'inputs': [{'name': 'body', 'nodeId': 'input-1', 'outputName': 'body'}]
        },
        {
            'name': 'output-node',
            'type': 'OUTPUT',
            'id': 'output-1',
            'inputs': [{'name': 'body', 'nodeId': 'prompt-1', 'outputName': 'output'}]
        }
    ]
}

response = bedrock_flows.create_flow(
    name='simple-chat-flow',
    description='Simple chatbot flow',
    definition=flow_definition
)

flow_id = response['flowId']
```

## Using the Console (Simpler)

AWS Console provides visual flow builder:

1. Go to Bedrock → Flows
2. Create flow
3. Drag nodes onto canvas
4. Connect nodes
5. Configure each node
6. Deploy (create alias)
7. Invoke via API

## Flow Aliases

Deploy flows with versioned aliases:

```python
response = bedrock_flows.create_flow_alias(
    flowId='flow-123',
    name='prod',
    description='Production flow'
)

alias_id = response['flowAliasId']
```

## Invoking a Flow

```python
bedrock_runtime = boto3.client('bedrock-runtime')

response = bedrock_runtime.invoke_flow(
    flowIdentifier='flow-123',
    flowAliasIdentifier='prod',
    inputs={
        'userQuestion': 'What is the return policy?'
    }
)

for event in response['responseStream']:
    if 'flowOutputEvent' in event:
        output = event['flowOutputEvent']['body']
        print(output)
```

## Common Flow Patterns

### 1. RAG with Fallback
```
Input → KB Retrieval → Check Score
                        ├─ High: Generate Answer
                        └─ Low: Ask Clarifying Question
```

### 2. Multi-Step Processing
```
Input → KB Search → Extract Key Terms → Generate Summary → Evaluate Quality
```

### 3. Agent with Guard Rails
```
Input → Check Safety → Route to Agent → Apply Guardrails → Output
```

## Advantages Over Code

| Aspect | Code | Flows |
|--------|------|-------|
| Visibility | Low | High |
| Debugging | Harder | Easier |
| Non-technical | No | Yes |
| Maintenance | Manual versioning | Built-in |
| Deployment | Manual | Built-in aliases |

## Limitations

- Can't do complex logic (use Lambda for that)
- Node outputs must be text
- No custom Python nodes
- Limited to predefined node types

## Costs

Same as constituent parts:
- Model invocations → standard pricing
- KB retrieval → standard pricing
- Agent calls → standard pricing
- Flow orchestration → free

## Gotchas

### 1. Node Output Format
Output must be JSON-serializable. Text only for now.

### 2. No Error Handling
If a node fails, flow fails. No retry logic built-in.

### 3. Long Flows
Each node is sequential. Long flows = high latency.

## Next Steps

Module 08 project: Build content workflow (topic → KB → draft → publish).

## Resources

- **Flows Docs:** https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html
- **Flow Console:** https://console.aws.amazon.com/bedrock/flows
