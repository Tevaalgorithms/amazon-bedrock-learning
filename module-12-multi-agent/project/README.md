# Module 12 Project — Multi-Agent Content Pipeline

## Goal

Build a system with 3 specialized agents orchestrated by a supervisor:
1. **Research Agent** — retrieves from KB
2. **Writer Agent** — composes content
3. **Reviewer Agent** — checks quality

## Architecture

```
User: "Write about Machine Learning"
    ↓
Supervisor Agent: Routes to all 3 (parallel)
    ├→ Research Agent: Finds ML articles
    ├→ Writer Agent: Drafts content
    └→ Reviewer Agent: Checks draft quality
    ↓
Aggregator: Combines results
    ↓
Output: "Here's ML content... (reviewed)"
```

## Implementation

```python
from concurrent.futures import ThreadPoolExecutor
import boto3

bedrock_runtime = boto3.client('bedrock-runtime')
bedrock_agent = boto3.client('bedrock-agent-runtime')

def research_agent(topic):
    """Find research on topic."""
    # TODO: Query KB or use Converse to research
    return f"Researched {topic}"

def writer_agent(topic, research):
    """Write content."""
    response = bedrock_runtime.converse(
        modelId='anthropic.claude-3-5-sonnet-20241022-v1:0',
        messages=[
            {'role': 'user', 'content': f'Write about {topic} using: {research}'}
        ]
    )
    return response['output']['message']['content'][0]['text']

def reviewer_agent(content):
    """Review content quality."""
    response = bedrock_runtime.converse(
        modelId='anthropic.claude-3-5-sonnet-20241022-v1:0',
        messages=[
            {'role': 'user', 'content': f'Rate this on 1-10: {content}'}
        ]
    )
    return response['output']['message']['content'][0]['text']

def run_parallel_agents(topic):
    """Execute all agents in parallel."""
    with ThreadPoolExecutor(max_workers=3) as executor:
        research = executor.submit(research_agent, topic).result()
        content = executor.submit(writer_agent, topic, research).result()
        review = executor.submit(reviewer_agent, content).result()

    return {
        'topic': topic,
        'research': research,
        'content': content,
        'review': review
    }

# Main
result = run_parallel_agents('Quantum Computing')
print(f"Research: {result['research']}")
print(f"Content: {result['content']}")
print(f"Review: {result['review']}")
```

## Test Cases

- Simple topic: "Python Basics"
- Complex topic: "Quantum Machine Learning"
- Current events: "Latest AI trends"

## Key Learnings

- Agent specialization
- Parallel execution for performance
- Result aggregation
- Error handling across agents
- Cost optimization (parallel vs sequential)
