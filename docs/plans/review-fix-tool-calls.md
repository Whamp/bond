# Plan: Harden Tool Call Messaging

- [ ] Ensure assistant messages recorded for tool invocations never include `None` content so the z.ai API isn't sent JSON `null` values.
- [ ] Convert SDK tool call objects to plain dictionaries before adding them to `BondAgent.context` to avoid serialization errors on the next `chat.completions.create` call.
- [ ] Adjust `BondAgent.tool_call` to stringify primitive tool results without double-encoding while still supporting structured JSON payloads.
