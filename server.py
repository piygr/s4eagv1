# basic import
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
#from pywinauto.application import Application
#import win32gui
#import win32con
import time
#from win32api import GetSystemMetrics

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
# instantiate an MCP server client

mcp = FastMCP("Calculator")

driver = None

# DEFINE TOOLS

# addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

# division tool
@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1 / 3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers division"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

# create thumbnail
@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]


@mcp.tool()
def open_paint_app_in_browser() -> str:
    """This ACTION opens paint app in browser which can be used to draw any shapes eg rectangle, circle, ellipse etc.
    It can also be used to write text. """
    print("CALLED: open_paint_app_in_browser() -> bool:")

    #chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--headless")
    #driver = webdriver.Chrome(
    #    service=Service(ChromeDriverManager().install()),
    #    options=chrome_options
    #)
    start_url = "https://jspaint.app/"
    import subprocess, pyautogui

    # Example: Open Pages app
    subprocess.run(["open", "-a", "Google Chrome"])
    time.sleep(5)
    pyautogui.write(start_url, interval=0.05)
    pyautogui.press('enter')
    #driver.get(start_url)
    time.sleep(10)
    return f"The paint app was successfully opened in the browser."

@mcp.tool()
def create_rectangle_in_paint_app() -> str:
    """This ACTION creates a rectangle in the paint app if the paint app is open. If paint app is not open, the rectangle is not created.
    Make sure the paint app is open before making this action call.
    By default, the upper left corner of the rectangle is at position (150, 300) and lower right corer of the rectangle is at (400, 500).
    """

    #if not driver:
    #    return "Failed to create rectangle as paint app was not opened."

    print("CALLED: create_rectangle_in_paint_app() -> bool:")

    print("Clicking on the Rectangle button on the panel..")
    import pyautogui
    pyautogui.leftClick(14, 325)
    time.sleep(0.3)

    print("Creating a Rectangle..")
    # Move to source point (x1, y1) and click-hold
    pyautogui.moveTo(150, 300)  # replace with your source coords
    pyautogui.mouseDown()

    # Drag to destination point (x2, y2)
    pyautogui.moveTo(400, 500, duration=1)  # smooth drag
    pyautogui.mouseUp()
    time.sleep(1)

    return f"The rectangle with upper left corner (x: {150}, y: {300}) and bottom right corner (x: {400}, y: {500}) is created successfully."


@mcp.tool()
def write_inside_rectangle_in_paint_app(upperLeftX: int, upperLeftY: int, bottomRightX: int, bottomRightY, value: str) -> str:
    """This ACTION writes value inside the rectangle with upper left position (upperLeftX, upperLeftY)
    and bottom right position (bottomRightX, bottomRightY).
    Make sure the paint app is open. In case the paint app is not open, it fails to write the text.

    """
    #if not driver:
    #    return "Failed to write text as paint app was not opened."
    
    print("CALLED: write_inside_rectangle_in_paint_app(value: list) -> bool:")

    print("Clicking on the Text button on the panel..")

    import pyautogui
    pyautogui.moveTo(39, 280)
    time.sleep(0.3)
    pyautogui.leftClick()
    time.sleep(0.3)

    print("Creating a Text Box inside the rectangle..")
    # Move to source point (x1, y1) and click-hold
    pyautogui.moveTo(175, 320)  # replace with your source coords
    pyautogui.mouseDown()

    # Drag to destination point (x2, y2)
    pyautogui.moveTo(360, 460, duration=1)  # smooth drag
    pyautogui.mouseUp()
    time.sleep(0.3)

    print(f"Writing value {value} received from the calculation in the Text Box..")
    pyautogui.write(value, interval=0.05)


    #print("Qutiing browser in 2 seconds")

    time.sleep(10)
    #driver.quit()
    return f"the {value} is written inside the text box with upper left position at (x: {upperLeftX}, y: {upperLeftY}) and " \
           f"bottom left position at (x: {bottomRightX}, y: {bottomRightY}) successfully"

'''
@mcp.tool()
def close_paint_app():
    #"This function closes the browser and paint app"
    #driver.quit()
    return True
    
'''


# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
