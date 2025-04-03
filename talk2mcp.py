import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
from google import genai
from concurrent.futures import TimeoutError
from functools import partial

# Load environment variables from .env file
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

max_iterations = 15
last_response = None
iteration = 0
completed = False
iteration_response = []

async def generate_with_timeout(client, prompt, timeout=30):
    """Generate content with a timeout"""
    print("Starting LLM generation...")
    try:
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                ),
            ),
            timeout=timeout
        )
        print("LLM generation completed")
        return response
    except TimeoutError:
        print("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        raise

def reset_state():
    """Reset all global variables to their initial state"""
    global last_response, iteration, iteration_response, completed
    last_response = None
    iteration = 0
    iteration_response = []

async def main():
    reset_state()  # Reset at the start of main
    print("Starting main execution...")
    try:
        print("Establishing connection to MCP server...")
        server_params = StdioServerParameters(
            command="python",
            args=["server.py"]
        )
        async with stdio_client(server_params) as (read, write):
            print("Connection established, creating session...")
            async with ClientSession(read, write) as session:
                print("Session created, initializing...")
                await session.initialize()

                # Get available tools
                print("Requesting tool list...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                print(f"Successfully retrieved {len(tools)} tools")

                # Create system prompt with available tools
                print("Creating system prompt...")
                tools_description = []
                for i, tool in enumerate(tools):
                    try:
                        params = tool.inputSchema
                        desc = getattr(tool, 'description', 'No description available')
                        name = getattr(tool, 'name', f'tool_{i}')
                        if 'properties' in params:
                            param_details = []
                            for param_name, param_info in params['properties'].items():
                                param_type = param_info.get('type', 'unknown')
                                param_details.append(f"{param_name}: {param_type}")
                            params_str = ', '.join(param_details)
                        else:
                            params_str = 'no parameters'
                        tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
                        tools_description.append(tool_desc)
                        print(f"Added description for tool: {tool_desc}")
                    except Exception as e:
                        print(f"Error processing tool {i}: {e}")
                        tools_description.append(f"{i+1}. Error processing tool")

                tools_description = "\n".join(tools_description)
                print("Successfully created tools description")

                system_prompt = f"""You are a browser cum math agent solving problems in iterations and finally display it inside a rectangle
in the broswer based paint app. You have access to various mathematical tools and the action tools. You need to use EXACTLY these tools to calculate the answer
and finally displaying the answer inside a rectangle created in the browser based paint app.
Available tools:
{tools_description}
You must respond with EXACTLY ONE line in one of these formats (no additional text) to calculate the answer:
1. For function calls:
   FUNCTION_CALL: function_name|param1|param2|...
2. If the final answer is calculated:
   CALCULATED_ANSWER: [number]
   
But once CALCULATED_ANSWER is ready, You must respond with EXACTLY ONE line in one of these formats (no additional text):
1. For operating the browser app to perform display actions. The actions are available in the list of tools:
   ACTION: action_name|param1|param2|...
2. When no more pending actions to display the answer:
   COMPLETED: [boolean]
   
Important:
- When a function returns multiple values, you need to process all of them
- Only give CALCULATED_ANSWER when you have completed all necessary calculations
- Do not repeat function calls with the same parameters.
- Once CALCULATED_ANSWER is ready, you MUST suggest actions from the list of available tools to display the annswer.
- Do not repeat same actions on the browser app.
- STRICTLY returns EXACTLY ONE line response that follows the prescribed format.
- If some action require no action_value, respond with action_name|_. "_" indicates default action shall be taken as defined.
- 'COMPLETED: [boolean]' must be called when no action remains

Examples:
- FUNCTION_CALL: add|5|3
- FUNCTION_CALL: strings_to_chars_to_int|INDIA
- FUNCTION_CALL: int_list_to_exponential_sum|[73, 78, 68, 73, 65]
- CALCULATED_ANSWER: [7.599822246093079e+33]
- ACTION: open_paint_app_in_browser|_
- ACTION: create_rectangle_in_paint_app|_
- ACTION: write_inside_rectangle_in_paint_app|120|200|300|400|[7.599822246093079e+33]
- COMPLETED: [True]

DO NOT include any explanations or additional text.
Your entire response should be a single line starting with EXACTLY ONE of these ['FUNCTION_CALL:', 'CALCULATED_ANSWER:', 'ACTION:', 'COMPLETED:']"""

                query = """Find the ASCII values of characters in INDIA and then return sum of exponentials of those values."""
                print("Starting iteration loop...")
                global iteration, last_response, completed
                while not completed:
                    print(f"\n--- Iteration {iteration + 1}, Completed {completed} ---")
                    if last_response is None:
                        current_query = query
                    else:
                        current_query = current_query + "\n\n" + "\n".join(iteration_response)
                        current_query = current_query + " What should be done next?"

                    print("Preparing to generate LLM response...")
                    prompt = f"{system_prompt}\n\nQuery: {current_query}"
                    #print("##############################")
                    #print(prompt)
                    #print("##############################")
                    try:
                        response = await generate_with_timeout(client, prompt)
                        response_text = response.text.strip()
                        print(f"LLM Response: {response_text}")
                        for line in response_text.split('\n'):
                            line = line.strip()
                            if line.startswith("FUNCTION_CALL:"):
                                response_text = line
                                break
                    except Exception as e:
                        print(f"Failed to get LLM response: {e}")
                        break

                    if response_text.startswith("FUNCTION_CALL:"):
                        _, function_info = response_text.split(":", 1)
                        parts = [p.strip() for p in function_info.split("|")]
                        func_name, params = parts[0], parts[1:]

                        #print(f"\nDEBUG: Raw function info: {function_info}")
                        print(f"DEBUG: Split parts: {parts}")
                        print(f"DEBUG: Function name: {func_name}")
                        print(f"DEBUG: Raw parameters: {params}")
                        try:
                            tool = next((t for t in tools if t.name == func_name), None)
                            if not tool:
                                print(f"DEBUG: Available tools: {[t.name for t in tools]}")
                                raise ValueError(f"Unknown tool: {func_name}")
                            print(f"DEBUG: Found tool: {tool.name}")
                            print(f"DEBUG: Tool schema: {tool.inputSchema}")
                            arguments = {}
                            schema_properties = tool.inputSchema.get('properties', {})
                            print(f"DEBUG: Schema properties: {schema_properties}")
                            for param_name, param_info in schema_properties.items():
                                if not params:
                                    raise ValueError(f"Not enough parameters provided for {func_name}")
                                else:
                                    value = params.pop(0)
                                    if value == '_':
                                        print(f"DEBUG: Function call requires no parametrs")
                                        arguments = None
                                        break
                                    param_type = param_info.get('type', 'string')
                                    print(f"DEBUG: Converting parameter {param_name} with value {value} to type {param_type}")
                                    if param_type == 'integer':
                                        arguments[param_name] = int(value)
                                    elif param_type == 'number':
                                        arguments[param_name] = float(value)
                                    elif param_type == 'array':
                                        if isinstance(value, str):
                                            value = value.strip('[]').split(',')
                                            arguments[param_name] = [int(x.strip()) for x in value]
                                        else:
                                            arguments[param_name] = str(value)
                                    else:
                                        arguments[param_name] = str(value)
                            print(f"DEBUG: Final arguments: {arguments}")
                            print(f"DEBUG: Calling tool {func_name}")
                            if arguments is None:
                                result = await session.call_tool(func_name)
                            else:
                                result = await session.call_tool(func_name, arguments=arguments)

                            print(f"DEBUG: Raw result: {result}")
                            if hasattr(result, 'content'):
                                print(f"DEBUG: Result has content attribute")
                                if isinstance(result.content, list):
                                    iteration_result = [
                                        item.text if hasattr(item, 'text') else str(item)
                                        for item in result.content
                                    ]
                                else:
                                    iteration_result = str(result.content)
                            else:
                                print(f"DEBUG: Result has no content attribute")
                                iteration_result = str(result)
                            print(f"DEBUG: Final iteration result: {iteration_result}")
                            if isinstance(iteration_result, list):
                                result_str = f"[{', '.join(iteration_result)}]"
                            else:
                                result_str = str(iteration_result)
                            iteration_response.append(
                                f"In the {iteration + 1} iteration you called {func_name} with {arguments} parameters, and the function returned {result_str}."
                            )
                            last_response = iteration_result
                        except Exception as e:
                            print(f"DEBUG: Error details: {str(e)}")
                            print(f"DEBUG: Error type: {type(e)}")
                            import traceback
                            traceback.print_exc()
                            iteration_response.append(f"Error in iteration {iteration + 1}: {str(e)}")
                            break
                    elif response_text.startswith("CALCULATED_ANSWER:"):
                        _, answer = response_text.split(":", 1)
                        print(f"DEBUG: Calculated answer is {answer}. \nNow, let's display it as mentioned.\n")

                        iteration_response.append(
                            f"In the {iteration + 1} iteration, I have received {answer} as the calculated answer.\n\n"
                            f"Great, we are ready with the answer."
                            f"Now, you need to STRICTLY perform actions for displaying this answer in the paint app.\n"
                            f"IMPORTANT: \nHere, onwards you need to respond in EXACTLY ONE LINE and the line starts with either of 'ACTION:', 'COMPLETED:'\n"
                        )

                    elif response_text.startswith("ACTION:"):
                        _, function_info = response_text.split(":", 1)
                        parts = [p.strip() for p in function_info.split("|")]
                        func_name, params = parts[0], parts[1:]

                        print(f"\nDEBUG: Raw action info: {function_info}")
                        print(f"DEBUG: Split parts: {parts}")
                        print(f"DEBUG: Action name: {func_name}")
                        print(f"DEBUG: Raw parameters: {params}")

                        try:
                            tool = next((t for t in tools if t.name == func_name), None)
                            if not tool:
                                print(f"DEBUG: Available tools: {[t.name for t in tools]}")
                                raise ValueError(f"Unknown tool: {func_name}")
                            print(f"DEBUG: Found tool: {tool.name}")
                            print(f"DEBUG: Tool schema: {tool.inputSchema}")
                            arguments = {}
                            schema_properties = tool.inputSchema.get('properties', {})
                            print(f"DEBUG: Schema properties: {schema_properties}")
                            for param_name, param_info in schema_properties.items():
                                if not params:
                                    raise ValueError(f"Not enough parameters provided for {func_name}")
                                else:
                                    value = params.pop(0)
                                    if value == '_':
                                        print(f"DEBUG: Action call requires no parameters")
                                        arguments = None
                                        break
                                    arguments[param_name] = str(value)
                            print(f"DEBUG: Final arguments: {arguments}")
                            print(f"DEBUG: Calling tool {func_name}")
                            if arguments is None:
                                result = await session.call_tool(func_name)
                            else:
                                result = await session.call_tool(func_name, arguments=arguments)

                            print(f"DEBUG: Raw result: {result}")
                            if hasattr(result, 'content'):
                                print(f"DEBUG: Result has content attribute")
                                if isinstance(result.content, list):
                                    iteration_result = [
                                        item.text if hasattr(item, 'text') else str(item)
                                        for item in result.content
                                    ]
                                else:
                                    iteration_result = str(result.content)
                            else:
                                print(f"DEBUG: Result has no content attribute")
                                iteration_result = str(result)
                            print(f"DEBUG: Final iteration result: {iteration_result}")
                            if isinstance(iteration_result, list):
                                result_str = f"[{', '.join(iteration_result)}]"
                            else:
                                result_str = str(iteration_result)
                            iteration_response.append(
                                f"In the {iteration + 1} iteration, perfomed {func_name} action, and the action returned - {result_str}."
                                f"Based on action: {func_name}  with result: {result_str}, we need to do perform the next step."
                            )
                            last_response = iteration_result
                        except Exception as e:
                            print(f"DEBUG: Error details: {str(e)}")
                            print(f"DEBUG: Error type: {type(e)}")
                            import traceback
                            traceback.print_exc()
                            iteration_response.append(f"Error in iteration {iteration + 1}: {str(e)}")
                            break
                    elif response_text.startswith("COMPLETED:"):
                        print("\n=== Agent Execution Complete ===")
                        print(f"DEBUG: Time to close the paint app")
                        result = await session.call_tool("close_paint_app")
                        completed = True
                        break
                    else:
                        print(f"DEBUG: Bogus Response")
                        break

                    iteration += 1
    except Exception as e:
        print(f"Exception during execution: {e}")

# To run this async code
if __name__ == "__main__":
    asyncio.run(main())
