from dotenv import load_dotenv
load_dotenv()

from livekit.agents import AgentServer, cli, Agent

from pipeline.session import create_session
from agents.graph import build_graph


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


        # give RAG result back as context
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