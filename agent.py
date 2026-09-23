import os
from dotenv import load_dotenv
from loguru import logger
from pipecat.transports.base_transport import TransportParams
from pipecat.transports.smallwebrtc.transport import SmallWebRTCTransport
from pipecat.services.google.llm import GoogleLLMService
from pipecat.services.sarvam.stt import SarvamSTTService
from pipecat.services.sarvam.tts import SarvamTTSService
from pipecat.services.groq.llm import GroqLLMService    
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.pipeline.runner import PipelineRunner
from pipecat.frames.frames import EndFrame
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.runner.types import SmallWebRTCRunnerArguments
from pipecat.runner.run import main

load_dotenv()
def require_env(n):
    v=os.getenv(n)
    if not v: raise RuntimeError(f"Missing {n}")
    return v

async def bot(session_args: SmallWebRTCRunnerArguments):
    sarvam_key = require_env("SARVAM_API_KEY")
    gemini_key = require_env("GEMINI_API_KEY")
    groq_key = require_env("GROQ_API_KEY")
    transport = SmallWebRTCTransport(
        webrtc_connection=session_args.webrtc_connection,
        params=TransportParams(audio_in_enabled=True, audio_out_enabled=True),
    )
    stt = SarvamSTTService(api_key=sarvam_key, model="saaras:v3", language_code="hi-IN")
    # llm = GoogleLLMService(api_key=gemini_key, model="gemini-3.6-flash")
    llm = GroqLLMService(
    api_key=groq_key,
    settings=GroqLLMService.Settings(model="openai/gpt-oss-120b")
)

    # MOST STABLE COMBO - v2 + anushka
    tts = SarvamTTSService(api_key=sarvam_key, model="bulbul:v3", speaker="anushka")

    context = LLMContext([{"role":"system","content":"You are helpful voice assistant. Reply very short in Hindi."}])
    context_aggregator = LLMContextAggregatorPair(context)
    pipeline = Pipeline([transport.input(), stt, context_aggregator.user(), llm, tts, transport.output(), context_aggregator.assistant()])
    task = PipelineTask(pipeline, params=PipelineParams(allow_interruptions=True))

    @transport.event_handler("on_client_connected")
    async def on_client_connected(t,c): logger.info("client connected")
    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(t,c): await task.queue_frame(EndFrame())

    runner = PipelineRunner()
    await runner.run(task)

if __name__ == "__main__":
    main()
