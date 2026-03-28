# Module 04 — Converse API & Streaming

## What is the Converse API?

The **Converse API** is a unified, model-agnostic API for text generation. Unlike InvokeModel (which requires model-specific request formatting), Converse works with any text model using the same interface.

### InvokeModel vs Converse

| Feature | InvokeModel | Converse |
|---------|-------------|----------|
| **API Format** | Model-specific JSON | Unified format |
| **Models** | All types (code, image, etc) | Text models only |
| **Streaming** | Supported | Supported |
| **Use Case** | Direct API access | Building apps |

## When to Use Converse

✅ **Use Converse if:**
- Building multi-model applications
- Want simpler API surface
- Don't need exotic features
- Just getting started

❌ **Use InvokeModel if:**
- Need image models
- Optimizing for cost (InvokeModel slightly cheaper)
- Need model-specific features

## Basic Converse API

### Request Format

```python
response = client.converse(
    modelId='anthropic.claude-3-5-sonnet-20241022-v1:0',
    messages=[
        {
            'role': 'user',
            'content': 'Hello, who are you?'
        }
    ],
    system='You are a helpful assistant.',
    inferenceConfig={
        'temperature': 0.7,
        'maxTokens': 1024
    }
)
```

### Response Format

```python
{
    'output': {
        'message': {
            'role': 'assistant',
            'content': [
                {
                    'text': 'I am Claude, an AI assistant...'
                }
            ]
        }
    },
    'usage': {
        'inputTokens': 10,
        'outputTokens': 25
    },
    'stopReason': 'end_turn'
}
```

## Multi-Turn Conversations

The Converse API maintains conversation history:

```python
messages = []

# Turn 1: User question
messages.append({
    'role': 'user',
    'content': 'What is the capital of France?'
})

response = client.converse(
    modelId='anthropic.claude-3-5-haiku-20241022-v1:0',
    messages=messages
)

# Add assistant response to history
messages.append({
    'role': 'assistant',
    'content': response['output']['message']['content']
})

# Turn 2: Follow-up question
messages.append({
    'role': 'user',
    'content': 'What is its population?'
})

response = client.converse(
    modelId='anthropic.claude-3-5-haiku-20241022-v1:0',
    messages=messages
)
```

The model uses full conversation history for context.

## Streaming Responses

For better UX, stream responses as they arrive:

```python
response = client.converse_stream(
    modelId='anthropic.claude-3-5-haiku-20241022-v1:0',
    messages=[
        {'role': 'user', 'content': 'Explain quantum computing...'}
    ]
)

# Streaming event loop
for event in response['stream']:
    if 'contentBlockDelta' in event:
        text = event['contentBlockDelta']['delta']['text']
        print(text, end='', flush=True)  # Print as it arrives
```

### Why Stream?

- **Better UX** — user sees response immediately
- **Faster perceived latency** — doesn't feel like waiting
- **Handle long responses** — display before generation finishes
- **Cancel early** — stop if user uninterested

## Token Counting

```python
response = client.converse(...)

tokens_in = response['usage']['inputTokens']
tokens_out = response['usage']['outputTokens']
total_tokens = tokens_in + tokens_out

print(f"Used {tokens_in} input + {tokens_out} output = {total_tokens} total")
```

### Token Estimation

- 1 token ≈ 4 characters ≈ 0.75 words
- 1000 tokens ≈ 750 words ≈ 3 pages

## Inference Config

Fine-tune model behavior:

```python
inferenceConfig={
    'temperature': 0.7,  # 0=deterministic, 1=creative
    'topP': 0.9,         # nucleus sampling threshold
    'topK': 250,         # limit to top K tokens
    'maxTokens': 1024,   # hard limit on response length
    'stopSequences': ['\n\n']  # stop on these strings
}
```

## System Prompts

Give context for the entire conversation:

```python
response = client.converse(
    modelId='anthropic.claude-3-5-haiku-20241022-v1:0',
    system='''You are a Python expert.
Always respond with code examples.
Use type hints in all code.
Explain your reasoning.''',
    messages=[
        {'role': 'user', 'content': 'How do I read a file?'}
    ]
)
```

System prompt applies to all turns in the conversation.

## Converse vs InvokeModel Examples

### Same Task with Both APIs

**InvokeModel (Claude-specific):**
```python
request = {
    'anthropic_version': 'bedrock-2023-06-01',
    'max_tokens': 100,
    'messages': [{'role': 'user', 'content': 'Hello'}]
}
response = client.invoke_model(
    modelId='anthropic.claude-3-5-haiku-20241022-v1:0',
    body=json.dumps(request)
)
```

**Converse (model-agnostic):**
```python
response = client.converse(
    modelId='anthropic.claude-3-5-haiku-20241022-v1:0',
    messages=[{'role': 'user', 'content': 'Hello'}],
    inferenceConfig={'maxTokens': 100}
)
```

Converse is simpler and same API works for any model.

## Error Handling

```python
try:
    response = client.converse(...)
except client.exceptions.ThrottlingException:
    print("Rate limited, retry with exponential backoff")
except client.exceptions.AccessDeniedException:
    print("Check IAM permissions")
except Exception as e:
    print(f"Error: {e}")
```

## Gotchas

### 1. Stop Sequences
If you set `stopSequences: ['\n']`, output stops at first newline. Use carefully.

### 2. Temperature Not Supported Everywhere
Some models don't support all inference config parameters.

### 3. Streaming Can Timeout
Long-running streams might timeout. Monitor connection.

## Next Steps

Module 04 project: Build a terminal chatbot with streaming, conversation history, and token counting.

## Resources

- **Converse API Docs:** https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Converse.html
- **Converse Stream:** https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ConverseStream.html
