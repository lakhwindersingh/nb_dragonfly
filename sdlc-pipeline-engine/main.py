#!/usr/bin/env python3
"""
Entrypoint script for SDLC Pipeline Engine
"""
import asyncio

from SDLCConfigurationAndExecutionEngine import main as engine_main

if __name__ == "__main__":
    asyncio.run(engine_main())
