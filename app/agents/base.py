"""
Base Agent — Abstract base class for all LLM agents.

Every agent in the system inherits from BaseAgent[TIn, TOut],
providing a uniform execution interface and LangGraph integration.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar, TypedDict

from langgraph.graph import END, START, StateGraph

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")

logger = logging.getLogger(__name__)


class AgentInvokeState(TypedDict, total=False):
    payload: Any
    result: Any


class BaseAgent(ABC, Generic[TIn, TOut]):
    """
    Abstract base for all pipeline agents.

    Subclasses implement `run_async(payload: TIn) -> TOut`.
    Execution can go directly or through a LangGraph StateGraph
    for observability and tracing.
    """

    name: str
    llm_client: Optional[Any] = None

    def __init__(self, llm_client: Optional[Any] = None, **kwargs):
        super().__init__(**kwargs)
        if llm_client is not None:
            self.llm_client = llm_client
        self._compiled_invoke_graph = None

    @abstractmethod
    async def run_async(self, payload: TIn) -> TOut:
        """Main execution logic — must be implemented by subclasses."""
        raise NotImplementedError

    def _get_invoke_graph(self):
        """Lazily build a single-node LangGraph for tracing."""
        if self._compiled_invoke_graph is not None:
            return self._compiled_invoke_graph

        async def _node(state: AgentInvokeState) -> AgentInvokeState:
            return {"result": await self.run_async(state["payload"])}

        builder = StateGraph(AgentInvokeState)
        builder.add_node("invoke_agent", _node)
        builder.add_edge(START, "invoke_agent")
        builder.add_edge("invoke_agent", END)
        self._compiled_invoke_graph = builder.compile()
        return self._compiled_invoke_graph

    async def run_via_langgraph_async(self, payload: TIn) -> TOut:
        """Execute through LangGraph for observability."""
        graph = self._get_invoke_graph()
        final_state = await graph.ainvoke({"payload": payload})
        return final_state["result"]

    async def _call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> str:
        """Centralized helper for raw LLM calls with error handling."""
        if not self.llm_client:
            raise RuntimeError(f"[{self.name}] LLM client not configured")

        # Implementation: calls self.llm_client with retry & rate limiting
        raise NotImplementedError("See production implementation")

    async def _call_llm_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type,
        temperature: float = 0.0,
    ):
        """Structured output via Instructor — returns a Pydantic model instance."""
        if not self.llm_client:
            raise RuntimeError(f"[{self.name}] LLM client not configured")

        # Implementation: uses Instructor for guaranteed schema compliance
        raise NotImplementedError("See production implementation")
