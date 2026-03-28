# Module 04 Project — Terminal Chatbot

## Goal

Build an interactive terminal chatbot with:
- Multi-turn conversation history
- Streaming responses
- Token usage tracking
- Clean TUI

## Implementation

Create `chatbot.py`:

```python
import boto3
from typing import List

client = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL_ID = 'anthropic.claude-3-5-haiku-20241022-v1:0'

def chat_with_streaming(messages: List[dict]) -> str:
    """Send messages and stream response."""
    # TODO: Use client.converse_stream()
    # TODO: Print each chunk as it arrives
    # TODO: Track total tokens
    pass

def main():
    messages = []
    total_tokens = 0

    print("Chat with Claude (type 'exit' to quit)")
    print("-" * 40)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            break

        # TODO: Add user message to history
        # TODO: Stream response
        # TODO: Add assistant response to history
        # TODO: Print token usage

if __name__ == '__main__':
    main()
```

## Expected Output

```
Chat with Claude (type 'exit' to quit)
----------------------------------------

You: What is your name?
Claude: I'm Claude, an AI assistant made by Anthropic. How can I help you today?
[45 input tokens, 18 output tokens]

You: Tell me about yourself.
Claude: I'm Claude, an AI assistant created by Anthropic. I can help with a wide
range of tasks including answering questions, writing, analysis, math, coding,
and creative projects...
[89 input tokens, 156 output tokens]

You: exit
```

## Key Features

1. **Streaming** — text appears as it's generated
2. **History** — context persists across turns
3. **Token Tracking** — see cumulative usage
4. **Clean UI** — easy to follow conversation

## Variations

1. **System Prompt** — make it a specialized bot (Python expert, therapist, etc)
2. **Conversation Save/Load** — save chats to file
3. **Multi-model** — switch models mid-conversation
4. **Cost Tracker** — show running cost estimate
