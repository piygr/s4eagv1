# Assignment 4 EAG1

**s4eagv1** is a MCP project to learn the basics of MCO protocol to use LLM and interact with browser based paint app.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)

## Overview

This project includes the following key components:

- **server.py**: The MCP server which exposes mcp tools to be used by LLM Orchestrator and the client (talk2mcp.py)
- **talk2mcp.py**: It's an LLM based Orchestrator and agent which utilises the mathematical tools exposed by mcp server and showcases the result inside a rectangle created in browser based paint app.
- **logs**
```
Successfully retrieved 22 tools
Creating system prompt...
Added description for tool: 1. add(a: integer, b: integer) - Add two numbers
Added description for tool: 2. add_list(l: array) - Add all numbers in a list
Added description for tool: 3. subtract(a: integer, b: integer) - Subtract two numbers
Added description for tool: 4. multiply(a: integer, b: integer) - Multiply two numbers
Added description for tool: 5. divide(a: integer, b: integer) - Divide two numbers
Added description for tool: 6. power(a: integer, b: integer) - Power of two numbers
Added description for tool: 7. sqrt(a: integer) - Square root of a number
Added description for tool: 8. cbrt(a: integer) - Cube root of a number
Added description for tool: 9. factorial(a: integer) - factorial of a number
Added description for tool: 10. log(a: integer) - log of a number
Added description for tool: 11. remainder(a: integer, b: integer) - remainder of two numbers division
Added description for tool: 12. sin(a: integer) - sin of a number
Added description for tool: 13. cos(a: integer) - cos of a number
Added description for tool: 14. tan(a: integer) - tan of a number
Added description for tool: 15. mine(a: integer, b: integer) - special mining tool
Added description for tool: 16. create_thumbnail(image_path: string) - Create a thumbnail from an image
Added description for tool: 17. strings_to_chars_to_int(string: string) - Return the ASCII values of the characters in a word
Added description for tool: 18. int_list_to_exponential_sum(int_list: array) - Return sum of exponentials of numbers in a list
Added description for tool: 19. fibonacci_numbers(n: integer) - Return the first n Fibonacci Numbers
Added description for tool: 20. open_paint_app_in_browser() - This ACTION opens paint app in browser which can be used to draw any shapes eg rectangle, circle, ellipse etc.
    It can also be used to write text.
Added description for tool: 21. create_rectangle_in_paint_app() - This ACTION creates a rectangle in the paint app if the paint app is open. If paint app is not open, the rectangle is not created.
    Make sure the paint app is open before making this action call.
    By default, the upper left corner of the rectangle is at position (150, 300) and lower right corer of the rectangle is at (400, 500).

Added description for tool: 22. write_inside_rectangle_in_paint_app(upperLeftX: integer, upperLeftY: integer, bottomRightX: integer, bottomRightY: string, value: string) - This ACTION writes value inside the rectangle with upper left position (upperLeftX, upperLeftY)
    and bottom right position (bottomRightX, bottomRightY).
    Make sure the paint app is open. In case the paint app is not open, it fails to write the text.


Successfully created tools description
Starting iteration loop...

--- Iteration 1, Completed False ---
Preparing to generate LLM response...
Starting LLM generation...
LLM generation completed
LLM Response: FUNCTION_CALL: strings_to_chars_to_int|INDIA
DEBUG: Split parts: ['strings_to_chars_to_int', 'INDIA']
DEBUG: Function name: strings_to_chars_to_int
DEBUG: Raw parameters: ['INDIA']
DEBUG: Found tool: strings_to_chars_to_int
DEBUG: Tool schema: {'properties': {'string': {'title': 'String', 'type': 'string'}}, 'required': ['string'], 'title': 'strings_to_chars_to_intArguments', 'type': 'object'}
DEBUG: Schema properties: {'string': {'title': 'String', 'type': 'string'}}
DEBUG: Converting parameter string with value INDIA to type string
DEBUG: Final arguments: {'string': 'INDIA'}
DEBUG: Calling tool strings_to_chars_to_int
[04/03/25 15:56:56] INFO     Processing request of type CallToolRequest                                                                                                                        server.py:534
DEBUG: Raw result: meta=None content=[TextContent(type='text', text='73', annotations=None), TextContent(type='text', text='78', annotations=None), TextContent(type='text', text='68', annotations=None), TextContent(type='text', text='73', annotations=None), TextContent(type='text', text='65', annotations=None)] isError=False
DEBUG: Result has content attribute
DEBUG: Final iteration result: ['73', '78', '68', '73', '65']

--- Iteration 2, Completed False ---
Preparing to generate LLM response...
Starting LLM generation...
LLM generation completed
LLM Response: FUNCTION_CALL: int_list_to_exponential_sum|[73, 78, 68, 73, 65]
DEBUG: Split parts: ['int_list_to_exponential_sum', '[73, 78, 68, 73, 65]']
DEBUG: Function name: int_list_to_exponential_sum
DEBUG: Raw parameters: ['[73, 78, 68, 73, 65]']
DEBUG: Found tool: int_list_to_exponential_sum
DEBUG: Tool schema: {'properties': {'int_list': {'items': {}, 'title': 'Int List', 'type': 'array'}}, 'required': ['int_list'], 'title': 'int_list_to_exponential_sumArguments', 'type': 'object'}
DEBUG: Schema properties: {'int_list': {'items': {}, 'title': 'Int List', 'type': 'array'}}
DEBUG: Converting parameter int_list with value [73, 78, 68, 73, 65] to type array
DEBUG: Final arguments: {'int_list': [73, 78, 68, 73, 65]}
DEBUG: Calling tool int_list_to_exponential_sum
[04/03/25 15:56:57] INFO     Processing request of type CallToolRequest                                                                                                                        server.py:534
DEBUG: Raw result: meta=None content=[TextContent(type='text', text='7.599822246093079e+33', annotations=None)] isError=False
DEBUG: Result has content attribute
DEBUG: Final iteration result: ['7.599822246093079e+33']

--- Iteration 3, Completed False ---
Preparing to generate LLM response...
Starting LLM generation...
LLM generation completed
LLM Response: CALCULATED_ANSWER: [7.599822246093079e+33]
ACTION: open_paint_app_in_browser|_
DEBUG: Calculated answer is  [7.599822246093079e+33]
ACTION: open_paint_app_in_browser|_.
Now, let's display it as mentioned.


--- Iteration 4, Completed False ---
Preparing to generate LLM response...
Starting LLM generation...
LLM generation completed
LLM Response: ACTION: open_paint_app_in_browser|_

DEBUG: Raw action info:  open_paint_app_in_browser|_
DEBUG: Split parts: ['open_paint_app_in_browser', '_']
DEBUG: Action name: open_paint_app_in_browser
DEBUG: Raw parameters: ['_']
DEBUG: Found tool: open_paint_app_in_browser
DEBUG: Tool schema: {'properties': {}, 'title': 'open_paint_app_in_browserArguments', 'type': 'object'}
DEBUG: Schema properties: {}
DEBUG: Final arguments: {}
DEBUG: Calling tool open_paint_app_in_browser
[04/03/25 15:56:59] INFO     Processing request of type CallToolRequest                                                                                                                        server.py:534
DEBUG: Raw result: meta=None content=[TextContent(type='text', text='The paint app was successfully opened in the browser.', annotations=None)] isError=False
DEBUG: Result has content attribute
DEBUG: Final iteration result: ['The paint app was successfully opened in the browser.']

--- Iteration 5, Completed False ---
Preparing to generate LLM response...
Starting LLM generation...
LLM generation completed
LLM Response: ACTION: create_rectangle_in_paint_app|_

DEBUG: Raw action info:  create_rectangle_in_paint_app|_
DEBUG: Split parts: ['create_rectangle_in_paint_app', '_']
DEBUG: Action name: create_rectangle_in_paint_app
DEBUG: Raw parameters: ['_']
DEBUG: Found tool: create_rectangle_in_paint_app
DEBUG: Tool schema: {'properties': {}, 'title': 'create_rectangle_in_paint_appArguments', 'type': 'object'}
DEBUG: Schema properties: {}
DEBUG: Final arguments: {}
DEBUG: Calling tool create_rectangle_in_paint_app
[04/03/25 15:57:20] INFO     Processing request of type CallToolRequest                                                                                                                        server.py:534
DEBUG: Raw result: meta=None content=[TextContent(type='text', text='The rectangle with upper left corner (x: 150, y: 300) and bottom right corner (x: 400, y: 500) is created successfully.', annotations=None)] isError=False
DEBUG: Result has content attribute
DEBUG: Final iteration result: ['The rectangle with upper left corner (x: 150, y: 300) and bottom right corner (x: 400, y: 500) is created successfully.']

--- Iteration 6, Completed False ---
Preparing to generate LLM response...
Starting LLM generation...
LLM generation completed
LLM Response: ACTION: write_inside_rectangle_in_paint_app|150|300|400|500|7.599822246093079e+33

DEBUG: Raw action info:  write_inside_rectangle_in_paint_app|150|300|400|500|7.599822246093079e+33
DEBUG: Split parts: ['write_inside_rectangle_in_paint_app', '150', '300', '400', '500', '7.599822246093079e+33']
DEBUG: Action name: write_inside_rectangle_in_paint_app
DEBUG: Raw parameters: ['150', '300', '400', '500', '7.599822246093079e+33']
DEBUG: Found tool: write_inside_rectangle_in_paint_app
DEBUG: Tool schema: {'properties': {'upperLeftX': {'title': 'Upperleftx', 'type': 'integer'}, 'upperLeftY': {'title': 'Upperlefty', 'type': 'integer'}, 'bottomRightX': {'title': 'Bottomrightx', 'type': 'integer'}, 'bottomRightY': {'title': 'bottomRightY', 'type': 'string'}, 'value': {'title': 'Value', 'type': 'string'}}, 'required': ['upperLeftX', 'upperLeftY', 'bottomRightX', 'bottomRightY', 'value'], 'title': 'write_inside_rectangle_in_paint_appArguments', 'type': 'object'}
DEBUG: Schema properties: {'upperLeftX': {'title': 'Upperleftx', 'type': 'integer'}, 'upperLeftY': {'title': 'Upperlefty', 'type': 'integer'}, 'bottomRightX': {'title': 'Bottomrightx', 'type': 'integer'}, 'bottomRightY': {'title': 'bottomRightY', 'type': 'string'}, 'value': {'title': 'Value', 'type': 'string'}}
DEBUG: Final arguments: {'upperLeftX': '150', 'upperLeftY': '300', 'bottomRightX': '400', 'bottomRightY': '500', 'value': '7.599822246093079e+33'}
DEBUG: Calling tool write_inside_rectangle_in_paint_app
[04/03/25 15:57:25] INFO     Processing request of type CallToolRequest                                                                                                                        server.py:534
DEBUG: Raw result: meta=None content=[TextContent(type='text', text='the 7.599822246093079e+33 is written inside the text box with upper left position at (x: 150, y: 300) and bottom left position at (x: 400, y: 500) successfully', annotations=None)] isError=False
DEBUG: Result has content attribute
DEBUG: Final iteration result: ['the 7.599822246093079e+33 is written inside the text box with upper left position at (x: 150, y: 300) and bottom left position at (x: 400, y: 500) successfully']

--- Iteration 7, Completed False ---
Preparing to generate LLM response...
Starting LLM generation...
LLM generation completed
LLM Response: COMPLETED: [True]

=== Agent Execution Complete ===
DEBUG: Time to close the paint app
```

## Installation

To set up this project on your local machine, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/piygr/s4eagv1.git
