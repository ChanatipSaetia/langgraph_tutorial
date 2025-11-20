from langchain.agents import create_agent
from src.langgraph_tutorial.llm_config import model
from langgraph.graph.state import CompiledStateGraph
import asyncio
from urllib.parse import parse_qs, urlparse
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken
from pydantic import AnyUrl
from langchain_mcp_adapters.client import MultiServerMCPClient


async def handle_redirect(auth_url: str) -> None:
    print(f"Visit: {auth_url}")


async def handle_callback() -> tuple[str, str | None]:
    callback_url = input("Paste callback URL: ")
    # Parse the main URL
    main_params = parse_qs(urlparse(callback_url).query)
    redirect_to = main_params.get("redirectTo", [None])[0]
    if redirect_to:
        # Decode and parse the redirectTo URL
        decoded_redirect = redirect_to
        if "%" in redirect_to:
            from urllib.parse import unquote

            decoded_redirect = unquote(redirect_to)
        redirect_params = parse_qs(urlparse(decoded_redirect).query)
        code = redirect_params.get("code", [""])[0]
        state = redirect_params.get("state", [None])[0]
        return code, state
    return "", None


class InMemoryTokenStorage(TokenStorage):
    """Demo In-memory token storage implementation."""

    def __init__(self):
        self.tokens: OAuthToken | None = None
        self.client_info: OAuthClientInformationFull | None = None

    async def get_tokens(self) -> OAuthToken | None:
        """Get stored tokens."""
        return self.tokens

    async def set_tokens(self, tokens: OAuthToken) -> None:
        """Store tokens."""
        self.tokens = tokens

    async def get_client_info(self) -> OAuthClientInformationFull | None:
        """Get stored client information."""
        return self.client_info

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        """Store client information."""
        self.client_info = client_info


class CanvaMCPClient:
    def __init__(self):
        self.storage = InMemoryTokenStorage()
        self.oauth_auth = OAuthClientProvider(
            server_url="https://mcp.canva.com/mcp",
            client_metadata=OAuthClientMetadata(
                client_name="Example MCP Client",
                redirect_uris=[AnyUrl("http://localhost:8000/callback")],
                grant_types=["authorization_code", "refresh_token"],
                response_types=["code"],
                scope="user",
            ),
            storage=self.storage,
            redirect_handler=handle_redirect,
            callback_handler=handle_callback,
        )
        self.client = MultiServerMCPClient(
            {
                "canva": {
                    "url": "https://mcp.canva.com/mcp",
                    "transport": "streamable_http",
                    "auth": self.oauth_auth,
                }
            }
        )
        self.tools = None

    async def login_and_fetch_tools(self):
        self.tools = await self.client.get_tools()
        return self.tools


canva_client = CanvaMCPClient()
asyncio.run(canva_client.login_and_fetch_tools())


async def init_creator_agent() -> CompiledStateGraph:
    """
    Initialize the creator agent with a specific prompt and tools from CanvaMCPClient.
    Returns:
        The creator agent instance.
    """
    tools = await canva_client.login_and_fetch_tools()
    creator_prompt = (
        "You are a Creator who will create a poster or design anything in Canva."
    )
    creator_agent = create_agent(
        model,
        tools=tools,
        system_prompt=creator_prompt,
    )
    return creator_agent
