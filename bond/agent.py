"""
Bond - LLM Agent with tool calling capabilities
Based on the Fly.io article pattern: https://fly.io/blog/everyone-write-an-agent/
"""

import json
from typing import List, Dict, Any, Callable, Optional
from anthropic import Anthropic
from bond.config import load_config


class BondAgent:
    """
    Core agent that manages conversation context and tool calling.

    Follows the pattern from the Fly.io article:
    - Context is an array of message objects
    - Tools are JSON schemas the LLM can call
    - Loop: call LLM → handle tool calls → repeat
    """

    def __init__(self):
        """Initialize the agent with configuration and empty context."""
        self.config = load_config()
        self.client = Anthropic(
            api_key=self.config['auth_token'],
            base_url=self.config['base_url']
        )
        self.context: List[Dict[str, Any]] = []
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.tool_functions: Dict[str, Callable] = {}

    def add_tool(self, name: str, description: str, parameters: Dict[str, Any], function: Callable):
        """
        Add a tool that the agent can call.

        Args:
            name: Name of the tool
            description: Description of what the tool does
            parameters: JSON schema for the tool's parameters
            function: Python function to call when tool is invoked
        """
        # Store tools in Anthropic's native format
        self.tools[name] = {
            'name': name,
            'description': description,
            'input_schema': parameters,
        }
        self.tool_functions[name] = function

    def _prepare_messages(self) -> List[Dict[str, Any]]:
        """
        Prepare messages for API call.
        Converts internal context to API format.
        """
        # For now, just return the context as-is
        # Future: could transform between different message formats
        return self.context

    def _convert_to_anthropic_format(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert internal message format to Anthropic API format.
        """
        anthropic_messages = []
        for msg in messages:
            if msg['role'] == 'user':
                anthropic_messages.append({
                    'role': 'user',
                    'content': msg['content']
                })
            elif msg['role'] == 'assistant':
                if 'tool_calls' in msg:
                    # Handle tool calls - convert to Anthropic format
                    content = []
                    for tool_call in msg['tool_calls']:
                        content.append({
                            'type': 'tool_use',
                            'id': tool_call['id'],
                            'name': tool_call['function']['name'],
                            'input': json.loads(tool_call['function']['arguments'])
                        })
                    anthropic_messages.append({
                        'role': 'assistant',
                        'content': content
                    })
                else:
                    anthropic_messages.append({
                        'role': 'assistant',
                        'content': msg['content']
                    })
            elif msg['role'] == 'tool':
                # Handle tool results
                anthropic_messages.append({
                    'role': 'user',
                    'content': [{
                        'type': 'tool_result',
                        'tool_use_id': msg['tool_call_id'],
                        'content': msg['content']
                    }]
                })
        return anthropic_messages

    def call(self, messages: List[Dict[str, Any]], use_tools: bool = True) -> Any:
        """
        Call the LLM with tools and messages.

        Args:
            messages: List of message objects
            use_tools: Whether to include tools in the call

        Returns:
            LLM response
        """
        tools_list = list(self.tools.values()) if self.tools and use_tools else None

        # Convert context format to Anthropic format
        anthropic_messages = self._convert_to_anthropic_format(messages)

        kwargs = {
            'model': self.config['model'],
            'max_tokens': 1000,
            'messages': anthropic_messages,
        }

        if tools_list:
            kwargs['tools'] = tools_list

        response = self.client.messages.create(**kwargs)

        return response

    def tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single tool call.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            Formatted tool response for the LLM
        """
        if tool_name not in self.tool_functions:
            return {
                "role": "tool",
                "tool_call_id": "unknown",
                "content": f"Error: Tool '{tool_name}' not found"
            }

        try:
            result = self.tool_functions[tool_name](**arguments)

            # Handle primitive vs structured results
            # Primitives (str, int, float, bool, None) should be converted to string directly
            # Structured data (dict, list) should be JSON-encoded
            if isinstance(result, (str, int, float, bool, type(None))):
                content = str(result)
            else:
                # For dicts, lists, or other complex types, JSON-encode them
                content = json.dumps(result)

            return {
                "role": "tool",
                "tool_call_id": "generated",  # Will be overwritten
                "content": content
            }
        except Exception as e:
            return {
                "role": "tool",
                "tool_call_id": "error",
                "content": f"Error executing tool '{tool_name}': {str(e)}"
            }

    def handle_tools(self, response: Any) -> bool:
        """
        Process tool calls from LLM response.

        Following the article pattern:
        - Check if response has tool calls
        - Execute each tool call
        - Add results to context
        - Return True if tools were called (continue loop)

        Args:
            response: LLM response object from Anthropic API

        Returns:
            True if tools were called, False otherwise
        """
        if not response.content or len(response.content) == 0:
            return False

        # Check if any content blocks are tool_use blocks
        tool_use_blocks = [block for block in response.content if block.type == 'tool_use']
        if not tool_use_blocks:
            return False

        # Execute each tool call
        for tool_use in tool_use_blocks:
            tool_name = tool_use.name
            arguments = tool_use.input

            # Execute the tool
            tool_result = self.tool_call(tool_name, arguments)

            # Convert to our internal format for context
            tool_call_dict = {
                "id": tool_use.id,
                "type": "function",
                "function": {
                    "name": tool_use.name,
                    "arguments": json.dumps(tool_use.input)
                }
            }

            # Add tool call to context
            self.context.append({
                "role": "assistant",
                "tool_calls": [tool_call_dict]
            })

            # Set the tool_call_id and add result
            tool_result["tool_call_id"] = tool_use.id
            self.context.append(tool_result)

        return True

    def process(self, user_input: str) -> str:
        """
        Process user input through the agent.

        This is the main loop from the article:
        1. Add user input to context
        2. Call LLM
        3. Handle tool calls in a loop
        4. Add final response to context
        5. Return the response text

        Args:
            user_input: User's input message

        Returns:
            Agent's response text
        """
        # Add user input to context
        self.context.append({"role": "user", "content": user_input})

        # Call LLM
        response = self.call(self.context, use_tools=True)

        # Handle tool calls in a loop
        while self.handle_tools(response):
            # Re-call LLM with updated context
            response = self.call(self.context, use_tools=True)

        # Add final response to context
        if response.content and len(response.content) > 0:
            # Extract text from content blocks (excluding tool_use blocks)
            text_blocks = [block for block in response.content if block.type == 'text']
            if text_blocks:
                final_message = text_blocks[0].text
                self.context.append({"role": "assistant", "content": final_message})
                return final_message

        return "No response generated"

    def reset_context(self):
        """Clear the conversation context."""
        self.context = []

    def get_context(self) -> List[Dict[str, Any]]:
        """Get the current conversation context."""
        return self.context.copy()
