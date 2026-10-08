from MCPclient.MCPClient import call_mcp_tool
from langchain_core.tools import tool

def make_email_tool(token: str):
    """
    按当前用户的 token 生成一个 send_email_tool 工具
    """
    @tool
    def send_email_tool(to: str, subject: str, content: str) -> str:
        """
        当用户要求发送邮件、发送信息、发送通知时，使用该工具。
        参数：
        - to: 收件人邮箱
        - subject: 邮件主题
        - content: 邮件内容
        """
        result = call_mcp_tool(
            tool_name="send_email_tool",
            token=token,
            to=to,
            subject=subject,
            content=content,
        )
        return result
    return send_email_tool




if __name__ == "__main__":
    result = make_email_tool("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2Vyc0lkIjoyLCJuaWNrbmFtZSI6InNzIiwiZW1haWwiOiIyMjk3NDc0MjY1QHFxLmNvbSIsImVtYWlsX3Bhc3N3b3JkIjoib3BlZXR0cHlrdHFxZGlmYiIsInJvbGVzSWQiOjAsImV4cCI6MTc5MDEwMTQ4NiwiaWF0IjoxNzkwMDU4Mjg2fQ.J3n1Ou1d8tjOaW460_UJ7-pB7uWnH-uZ3ud8y-CfDXw")
    print(result)