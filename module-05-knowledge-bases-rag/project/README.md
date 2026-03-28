# Module 05 Project — Document Q&A System

## Goal

Build a system that:
1. Creates a Bedrock Knowledge Base
2. Ingests PDF documents
3. Answers questions with citations
4. Shows retrieval quality

## Implementation Steps

1. **Create S3 bucket** for documents
2. **Create OpenSearch Serverless collection** for vector store
3. **Create Knowledge Base** (Bedrock console or IaC)
4. **Upload PDFs** via sync job
5. **Query with citations**

## Starter Code

```python
import boto3

bedrock_client = boto3.client('bedrock-agent')

# TODO: Create knowledge base
knowledge_base_id = 'YOUR_KB_ID'

# TODO: Upload documents (via S3 or console)

# TODO: Query with RetrieveAndGenerate
response = bedrock_client.retrieve_and_generate(
    input={'text': 'Your question here'},
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': knowledge_base_id
        }
    }
)

# TODO: Extract answer and citations
answer = response['output']['text']
sources = response['citations']
```

## Key Learning

- Knowledge Base setup (infrastructure)
- Chunking and embedding
- Retrieval quality
- Citation handling
