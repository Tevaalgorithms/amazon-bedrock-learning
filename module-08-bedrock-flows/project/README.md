# Module 08 Project — Content Workflow Flow

## Goal

Create a Bedrock Flow that:
1. Takes a topic as input
2. Retrieves related documents from KB
3. Generates draft content
4. Evaluates quality
5. Routes to publish or revision

## Implementation

Use the Bedrock Flows console (easiest):

1. Create flow
2. Add nodes:
   - Input Node: receives topic
   - KB Node: retrieve documents
   - Prompt Node: generate draft
   - Condition Node: check quality score
   - Output Node: publish or revise

3. Create alias and deploy
4. Invoke via API

```python
bedrock_runtime = boto3.client('bedrock-runtime')

response = bedrock_runtime.invoke_flow(
    flowIdentifier='content-workflow',
    flowAliasIdentifier='prod',
    inputs={'topic': 'Machine Learning Basics'}
)

for event in response['responseStream']:
    if 'flowOutputEvent' in event:
        print(event['flowOutputEvent']['body'])
```

## Architecture Diagram

```
Input (topic)
    ↓
Retrieve from KB
    ↓
Generate draft via Prompt node
    ↓
Evaluate (quality score)
    ↓
Condition: score > 0.8?
├─ Yes: Output → Publish
└─ No: Output → Needs Revision
```

## Key Learning

- Visual workflow design
- Node chaining
- Conditional routing
- Deployment with aliases
