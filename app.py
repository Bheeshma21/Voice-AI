from dotenv import load_dotenv
load_dotenv()

import os
import subprocess
import sys
import traceback

# --------------------------------------------------
# Create Chroma DB automatically if it doesn't exist
# --------------------------------------------------
if not os.path.exists("rag/chroma_db/chroma.sqlite3"):
    print("Chroma database not found.")
    print("Running ingest.py to create embeddings...")

    subprocess.run(
        ["python", "rag/ingest.py"],
        check=True
    )

    print("Chroma database created successfully.")

print("DEBUG: importing AgentServer, cli, Agent from livekit.agents")
try:
    from livekit.agents import AgentServer, cli, Agent
    print("DEBUG: successfully imported AgentServer, cli, Agent from livekit.agents")
except Exception:
    print("DEBUG: FAILED importing AgentServer, cli, Agent from livekit.agents")
    traceback.print_exc()
    sys.exit(1)

print("DEBUG: importing create_session from pipeline.session")
try:
    from pipeline.session import create_session
    print("DEBUG: successfully imported create_session from pipeline.session")
except Exception:
    print("DEBUG: FAILED importing create_session from pipeline.session")
    traceback.print_exc()
    sys.exit(1)

print("DEBUG: importing build_graph from agents.graph")
try:
    from agents.graph import build_graph
    print("DEBUG: successfully imported build_graph from agents.graph")
except Exception:
    print("DEBUG: FAILED importing build_graph from agents.graph")
    traceback.print_exc()
    sys.exit(1)

print("DEBUG: creating AgentServer instance")
try:
    server = AgentServer()
    print("DEBUG: successfully created AgentServer instance")
except Exception:
    print("DEBUG: FAILED creating AgentServer instance")
    traceback.print_exc()
    sys.exit(1)


class VoiceAgent(Agent):

    def __init__(self):

        super().__init__(
            instructions="""
            You are a helpful voice assistant.

            Use the provided information to answer.
            Keep responses short and natural.
            Wait after answering.
            """
        )

        self.graph = build_graph()

    async def on_user_turn_completed(
        self,
        turn_ctx,
        new_message
    ):

        query = new_message.content[0]

        print("USER:", query)

        result = self.graph.invoke(
            {
                "query": query,
                "response": ""
            }
        )

        turn_ctx.add_message(
            role="system",
            content=result["response"]
        )


@server.rtc_session()
async def my_agent(ctx):

    session = create_session()

    await session.start(
        room=ctx.room,
        agent=VoiceAgent()
    )


if __name__ == "__main__":

    cli.run_app(server)