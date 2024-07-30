import asyncio
import os

try:
    from asyncio import WindowsSelectorEventLoopPolicy
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
except ImportError:
    pass  # Not needed on non-Windows systems
