import Tool.SendEmailTool
from Tool.SendEmailTool import mcp


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=9000)