
import hashlib
import re

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request

mcp = FastMCP("Exam Challenge Server")

EMAIL = "23f2005181@ds.study.iitm.ac.in"


@mcp.tool(
    name="solve_challenge",
    description="Solve the current exam challenge using its HTTP request header.",
)
def solve_challenge() -> str:
    request = get_http_request()

    challenge = request.headers.get("x-exam-challenge", "")

    # Reject missing or malformed challenges.
    if not re.fullmatch(r"[0-9a-f]{32}", challenge):
        raise ValueError("Missing or invalid X-Exam-Challenge header")

    result = hashlib.sha256(
        f"{challenge}:{EMAIL}".encode("utf-8")
    ).hexdigest()[:16]

    return result


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )
