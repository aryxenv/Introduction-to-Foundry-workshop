# Example Prompts for Testing Your Chatbot

Use these example prompts to test your RAG chatbot's capabilities.

## Basic Questions (Knowledge Base)

### About TechCorp

```
What products does TechCorp offer?
```

```
When was TechCorp founded?
```

```
What are TechCorp's office hours?
```

```
How can I contact TechCorp support?
```

### Policies

```
What is your return policy?
```

```
How long do I have to return a product?
```

```
What shipping options are available?
```

```
How much does overnight shipping cost?
```

```
What is your refund processing time?
```

```
Do you ship internationally?
```

### Customer Support

```
How can I get customer support?
```

```
What is your email for support?
```

```
Is live chat available?
```

```
What is your phone support number?
```

## Complex Questions (Multi-hop)

```
I want to return a product I bought 20 days ago. What should I do and when will I get my refund?
```

```
Compare your shipping options and tell me which one is best for urgent deliveries.
```

```
I need help with DataVision. How can I reach your support team?
```

```
What are all the ways I can contact TechCorp and when are each available?
```

## Questions Outside Knowledge Base

These should demonstrate how the chatbot handles unknown information:

```
What is your pricing for enterprise plans?
```

```
Do you have any job openings?
```

```
What is the weather like today?
```

```
Who is the CEO of TechCorp?
```

```
Can you help me with Python programming?
```

## Conversational Follow-ups

Test multi-turn conversation:

```
User: What products do you offer?
Bot: [Response about SmartAssist, DataVision, CloudSync]

User: Tell me more about SmartAssist
Bot: [Response about SmartAssist]

User: How much does it cost?
Bot: [Should handle gracefully as pricing isn't in knowledge base]
```

## Edge Cases

### Very Short Queries

```
Products?
```

```
Hours?
```

```
Return?
```

### Very Long Queries

```
I purchased one of your products about three weeks ago and I've been using it extensively but I've run into some issues and I'm considering returning it but I'm not sure if I'm still within the return window and I'd also like to know about the refund process and how long it typically takes and whether I need to keep the original packaging or if I can return it in different packaging and also what condition does the product need to be in for a successful return?
```

### Ambiguous Questions

```
Tell me about your service
```

```
What do you do?
```

```
How does it work?
```

### Questions with Typos

```
Whta are yuor office huors?
```

```
Hw can I contct supprt?
```

## Voice-Specific Prompts (Lab 2)

These work well with voice interaction:

### Natural Voice Commands

```
"Hey, what are your office hours?"
```

```
"I need to return something"
```

```
"Tell me about your products"
```

```
"How can I contact support?"
```

### Conversational Style

```
"Hi there! Can you help me with something?"
```

```
"I'm interested in learning more about what you offer"
```

```
"Quick question - do you do international shipping?"
```

## Testing Different Tones

### Formal

```
I would like to inquire about your return policy and refund procedures.
```

### Casual

```
Hey, what's your return policy?
```

### Urgent

```
I need to return a product immediately! What's the process?
```

## Multilingual (If Implemented)

### Spanish

```
¿Cuáles son sus horarios de oficina?
```

### French

```
Quels sont vos heures de bureau?
```

### German

```
Was sind Ihre Bürozeiten?
```

## Testing RAG Quality

### Source Attribution

After asking questions, verify:
- Are the sources cited correctly?
- Does the response match the source content?
- Are multiple sources combined appropriately?

### Example Questions for Source Testing

```
What are ALL the products TechCorp offers? (Should cite company_info.txt)
```

```
Explain your complete return and refund process (Should cite policies.txt)
```

```
Give me all contact methods for TechCorp (Should cite company_info.txt)
```

## Performance Testing

### Rapid-fire Questions

Ask these in quick succession:

```
1. What products do you offer?
2. What are your office hours?
3. What is your return policy?
4. How much is express shipping?
5. How can I contact support?
```

### Session Continuity

Test that the chatbot maintains context:

```
User: What are your shipping options?
Bot: [Lists shipping options]

User: How long does the fastest one take?
Bot: [Should reference overnight shipping from previous context]

User: And the slowest?
Bot: [Should reference standard shipping]
```

## Expected Behaviors

### Good Responses Should:

✅ Be accurate to the source material  
✅ Cite sources when available  
✅ Be concise and clear  
✅ Use natural language  
✅ Stay on topic  
✅ Admit when information isn't available  

### Bad Responses to Watch For:

❌ Hallucinating information not in knowledge base  
❌ Contradicting source material  
❌ Being overly verbose  
❌ Ignoring user's question  
❌ Being rude or unhelpful  
❌ Making up data or facts  

## Evaluation Criteria

Rate responses on:

1. **Accuracy** (1-5): Does it match the source material?
2. **Relevance** (1-5): Does it answer the question?
3. **Completeness** (1-5): Is the answer thorough?
4. **Clarity** (1-5): Is it easy to understand?
5. **Source Usage** (1-5): Are sources cited appropriately?

## Creating Your Own Test Cases

When adding your own documents, create test questions that:

1. Test basic fact retrieval
2. Require connecting multiple pieces of information
3. Have no answer in the knowledge base
4. Test edge cases specific to your domain
5. Validate source attribution

## Automated Testing

Use these in your test scripts:

```python
# Example test cases
test_cases = [
    {
        "query": "What are your office hours?",
        "expected_source": "company_info.txt",
        "expected_keywords": ["Monday", "Friday", "9 AM", "5 PM", "EST"]
    },
    {
        "query": "What is your return policy?",
        "expected_source": "policies.txt",
        "expected_keywords": ["30 days", "original packaging", "refund"]
    }
]
```

---

**Pro Tip**: Keep a log of questions that don't work well. This helps identify areas for improvement in your knowledge base or RAG implementation!
