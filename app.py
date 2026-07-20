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

# Wrap imports to catch exceptions
try:
    from livekit.agents import AgentServer, cli, Agent
    print("DEBUG: Imported AgentServer, cli, Agent")
except Exception as e:
    print(f"EXCEPTION in livekit.agents import: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    from pipeline.session import create_session
    print("DEBUG: Imported create_session")
except Exception as e:
    print(f"EXCEPTION in pipeline.session import: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    from agents.graph import build_graph
    print("DEBUG: Imported build_graph")
except Exception as e:
    print(f"EXCEPTION in agents.graph import: {e}")
    traceback.print_exc()
    sys.exit(1)

server = AgentServer()


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

