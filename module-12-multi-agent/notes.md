# Module 12 — Multi-Agent Orchestration

## What is Multi-Agent Orchestration?

A **supervisor agent** delegates tasks to **subagents** that specialize in different domains.

```
User Query
    ↓
Supervisor Agent (routes to best subagent)
    ├→ Research Agent (finds information)
    ├→ Writer Agent (composes response)
    └→ Reviewer Agent (checks quality)
    ↓
Combined Response
```

## Supervisor Pattern

### Anatomy

1. **Supervisor Agent** — routes requests
2. **Subagent 1, 2, 3** — specialized agents
3. **Shared Knowledge Base** — common context
4. **Result Aggregator** — combines outputs

### Supervisor Logic

```python
def supervisor_decide(user_query: str) -> str:
    """Route query to appropriate subagent."""

    response = client.converse(
        modelId='anthropic.claude-3-5-sonnet-20241022-v1:0',
        messages=[{
            'role': 'user',
            'content': f'''You are a supervisor. Route this query to:
- RESEARCH: for fact-finding or data lookup
- WRITER: for content generation
- REVIEWER: for quality checking

Query: {user_query}

Respond with just the agent name.'''
        }]
    )

    decision = response['output']['message']['content'][0]['text'].strip()
    return decision
```

## Agent Specialization

### Research Agent
- Retrieves from knowledge bases
- Fetches real-time data
- Returns structured findings

```python
def research_agent(topic: str) -> dict:
    """Find information about topic."""
    response = bedrock_runtime.retrieve_and_generate(
        input={'text': topic},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'kb-research',
                'modelArn': '...'
            }
        }
    )
    return {
        'topic': topic,
        'findings': response['output']['text'],
        'sources': response['citations']
    }
```

### Writer Agent
- Creates content
- Uses supervisor instructions
- Returns draft

```python
def writer_agent(topic: str, research: dict) -> str:
    """Write about topic using research."""
    response = client.converse(
        modelId='anthropic.claude-3-5-sonnet-20241022-v1:0',
        system='You are a skilled writer. Write clearly and concisely.',
        messages=[{
            'role': 'user',
            'content': f'''Write about: {topic}
Using this research: {research['findings']}

Format as markdown.'''
        }]
    )
    return response['output']['message']['content'][0]['text']
```

### Reviewer Agent
- Evaluates quality
- Checks accuracy
- Returns feedback

```python
def reviewer_agent(content: str, rubric: dict) -> dict:
    """Review content against rubric."""
    response = client.converse(
        modelId='anthropic.claude-3-5-sonnet-20241022-v1:0',
        system='You are a quality reviewer.',
        messages=[{
            'role': 'user',
            'content': f'''Review this content:
{content}

Rate on: {list(rubric.keys())}
Return JSON with scores 1-10.'''
        }]
    )
    return json.loads(response['output']['message']['content'][0]['text'])
```

## Orchestration Patterns

### Sequential (Pipeline)
Subagents run one after another:

```
User Query → Research Agent → Writer Agent → Reviewer Agent → Output
```

**Use for:** Content pipeline, multi-step processes

### Parallel
Subagents run simultaneously:

```
User Query → Research Agent ┐
             Writer Agent   ├→ Aggregator → Output
             Reviewer Agent ┘
```

**Use for:** Fact-checking (get 3 perspectives), efficiency

### Hierarchical
Multi-level supervision:

```
Supervisor
    ├→ Sales Supervisor
    │    ├→ Quote Agent
    │    └→ Discount Agent
    └→ Support Supervisor
         ├→ Ticket Agent
         └→ Solution Agent
```

**Use for:** Large organizations

## Implementation: Supervisor + 3 Subagents

```python
import boto3
import json
from concurrent.futures import ThreadPoolExecutor

client = boto3.client('bedrock-runtime')

def supervisor(query: str) -> str:
    """Main orchestrator."""

    # Step 1: Supervisor routes request
    routing = client.converse(
        modelId='anthropic.claude-3-5-sonnet-20241022-v1:0',
        messages=[{
            'role': 'user',
            'content': f'Route to: RESEARCH, WRITER, REVIEWER? Query: {query}'
        }]
    )

    agent = routing['output']['message']['content'][0]['text'].strip()

    # Step 2: Call appropriate subagent
    if 'RESEARCH' in agent:
        result = research_agent(query)
    elif 'WRITER' in agent:
        result = writer_agent(query)
    else:
        result = reviewer_agent(query)

    return result

def parallel_agents(query: str) -> dict:
    """Run all agents in parallel."""
    with ThreadPoolExecutor(max_workers=3) as executor:
        research_future = executor.submit(research_agent, query)
        writer_future = executor.submit(writer_agent, query)
        reviewer_future = executor.submit(reviewer_agent, query)

        return {
            'research': research_future.result(),
            'writer': writer_future.result(),
            'reviewer': reviewer_future.result()
        }

def main():
    query = "Explain quantum computing"

    # Sequential approach
    result = supervisor(query)
    print(f"Supervisor result:\n{result}")

    # Parallel approach
    results = parallel_agents(query)
    print(f"All agents:\n{json.dumps(results, indent=2)}")
```

## Communication Between Agents

### Shared Context

```python
class AgentContext:
    def __init__(self):
        self.messages = []
        self.data = {}

    def add_message(self, agent: str, message: str):
        self.messages.append({'agent': agent, 'message': message})

    def get_context(self) -> str:
        return '\n'.join([f"{m['agent']}: {m['message']}" for m in self.messages])

context = AgentContext()

# Agent 1 adds to context
context.add_message('Research', 'Found 10 papers on topic')

# Agent 2 reads context
other_context = context.get_context()
```

## Bedrock Native Multi-Agent

Bedrock supports inline agents:

```python
# Create supervisor with subagents as action groups
response = bedrock_agent.create_agent(
    agentName='supervisor',
    instruction='Route queries to subagents',
    actionGroups=[
        {
            'actionGroupName': 'call-research-agent',
            'actionGroupExecutor': {
                'lambda': 'arn:aws:lambda:...:invoke-research-agent'
            }
        },
        {
            'actionGroupName': 'call-writer-agent',
            'actionGroupExecutor': {
                'lambda': 'arn:aws:lambda:...:invoke-writer-agent'
            }
        }
    ]
)
```

## State Management

Track conversation state across agents:

```python
class ConversationState:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages = []
        self.agent_results = {}

    def add_to_history(self, role: str, content: str):
        self.messages.append({'role': role, 'content': content})

    def save(self, agent: str, result: str):
        self.agent_results[agent] = result

    def get_full_context(self) -> str:
        return '\n'.join([f"{m['role']}: {m['content']}" for m in self.messages])
```

## Challenges

### 1. Latency
Multiple sequential agents = longer response time. Mitigate with parallelization.

### 2. Cost
Multiple model invocations. Mitigate by routing smartly.

### 3. Error Propagation
If one agent fails, whole chain fails. Mitigate with fallbacks.

### 4. Token Limit Exceeded
Long conversation histories can exceed context limits. Mitigate with summarization.

## Best Practices

1. **Clear roles** — each agent should have one specialty
2. **Simple routing** — supervisor decision should be quick
3. **Parallel when possible** — don't wait unnecessarily
4. **Logging** — track which agents called, results, costs
5. **Testing** — test agent combinations before production
6. **Metrics** — measure end-to-end quality, not individual agent quality

## When to Use Multi-Agent

✅ **Use if:**
- Complex workflow with distinct steps
- Need human-interpretable decisions
- Different agents have different tools
- Specialization improves quality

❌ **Don't use if:**
- Single agent handles task fine
- Response time critical (latency adds up)
- Cost matters more than quality

## Example Workflows

### Content Pipeline
```
Research (find info) → Writer (compose) → Reviewer (check) → Publish
```

### Customer Service
```
Classify Query (agent 1) → Lookup Info (agent 2) → Generate Response (agent 3)
```

### Code Review
```
Parse Code (agent 1) → Check Security (agent 2) → Check Style (agent 3) → Summarize (agent 4)
```

## Next Steps

Module 12 project: Supervisor + 3 subagents content pipeline.

## Resources

- **Agent Patterns:** https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html
- **Orchestration:** https://docs.anthropic.com/en/docs/build-a-bot
- **LangGraph (external):** https://langchain-ai.github.io/langgraph/
