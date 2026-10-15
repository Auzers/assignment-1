"""The Part 1 coding agent: fix a software issue and submit a git patch."""

from __future__ import annotations

import json
from typing import Any

from assignment.agent.base import (
    DEFAULT_COMPACTION_KEEP_RECENT_STEPS,
    DEFAULT_COMPACTION_MAX_TOKENS,
    Agent,
    format_tool_output,
)
from assignment.agent.tools import EXECUTE_TOOL, SEND_MESSAGE_TOOL
from assignment.env import Environment

class CodeAgent(Agent):
    """An agent that fixes a software issue and submits a git patch."""

    def __init__(
        self,
        task: str,
        environment: Environment,
        model: str | None = None,
        logs_save_path: str | None = None,
        step_limit: int = 100,
        skills_path: str | None = None,
        auto_stop_environment: bool = True,
        compact_threshold_tokens: int | None = None,
        compaction_keep_recent_steps: int = DEFAULT_COMPACTION_KEEP_RECENT_STEPS,
        compaction_max_tokens: int = DEFAULT_COMPACTION_MAX_TOKENS,
    ):
        super().__init__(
            environment=environment,
            model=model,
            logs_save_path=logs_save_path,
            step_limit=step_limit,
            skills_path=skills_path,
            auto_stop_environment=auto_stop_environment,
            compact_threshold_tokens=compact_threshold_tokens,
            compaction_keep_recent_steps=compaction_keep_recent_steps,
            compaction_max_tokens=compaction_max_tokens,
        )
        self.task = task
        self.submitted_patch = ""

        # TODO(Part 1.3): Make the `execute` and `send_message` tools available
        # to the agent.
        self.tools.extend([EXECUTE_TOOL, SEND_MESSAGE_TOOL])

        # TODO(1.1.b): Construct the system prompt and task_prompt. These
        # should be usable by the `Agent.build_prompt` method.
        system_information = json.dumps(
            {
                "machine": self.env.machine,
                "release": self.env.release,
                "system": self.env.system,
                "version": self.env.version,
            },
            indent=2,
        )
        self.system_prompt = (
            "You are a coding agent working in a terminal environment. "
            "Inspect the repository, make only the changes needed for the task, "
            "and verify the result. Continue using the available tools until the "
            "task is complete.\n\n"
            f"The default working directory is {self.env.cwd}.\n\n"
            f"<system_information>\n{system_information}\n</system_information>"
        )
        self.task_prompt = (
            "Complete the following software task:\n\n"
            f"<task>\n{self.task}\n</task>"
        )
        # TODO(1.4): If any skills are available to the agent, make their
        # descriptions/metadata available to the agent in the prompt.

    def execute_tool_calls(
        self, tool_calls: list[dict[str, Any]]
    ) -> list[dict[str, str]]:
        """Execute ``execute`` and ``send_message`` calls in the code sandbox."""

        # TODO(Part 1.3): Parse each call, execute recognized tools, and return
        # one message per call (there may be multiple tool calls in one agent
        # response!). Malformed JSON and unknown tools must become recoverable
        # observations relayed to the agent instead of exceptions.

        observations: list[dict[str, str]] = []
        for tool_call in tool_calls:
            call_id = str(tool_call.get("id",""))
            function = tool_call.get("function") # run 中已经保证了一定有 function

            if not isinstance(function, dict):
                content = "Error: malformd tool call; funciton must be an object"
            else:
                name = function.get("name")
                raw_arguments = function.get("arguments")

                if not isinstance(name, str):
                    content = (
                        "Error: malformed tool call; function name must be a string."
                    )
                elif not isinstance(raw_arguments, str):
                    content = "Error: malformed tool call; arguments must be a JSON string."
                else:
                    try:
                        arguments = json.loads(raw_arguments)
                    except json.JSONDecodeError as exc:
                        content = f"Error: invalid JSON arguments: {exc}"
                    else:
                        if not isinstance(arguments, dict):
                            content = "Error: tool arguments must be a JSON object."
                        elif name == "execute":
                            if "command" not in arguments:
                                content = "Error: execute requires a command"
                            else:
                                execute_options = {
                                    key: arguments[key]
                                    for key in ("shell", "cwd","timeout","env")
                                    if key in arguments
                                }
                                output = self.env.execute(
                                    arguments["command"],
                                    **execute_options,
                                )
                                content = format_tool_output(output)
                        elif name == "send_message":
                            summary = arguments.get("summary")
                            if not isinstance(summary, str):
                                content = (
                                    "Error: send_message requires a string summary."
                                )

                            else:
                                self.finished = True
                                content = summary
                        else:
                            content = f"Error: unknown tool {name!r}."
        
            observations.append(
                {
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": content,
                }
            )
        return observations
                            

                            
                        
                        
            



