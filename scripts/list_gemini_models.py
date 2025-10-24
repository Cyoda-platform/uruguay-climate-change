#!/usr/bin/env python3
"""List available Gemini models."""

import os
import google.generativeai as genai

# Configure API - use the approved key
api_key = os.getenv('GEMINI_API_KEY', '')
if not api_key:
    print("ERROR: GEMINI_API_KEY not set")
    exit(1)

print(f"Using API key: {api_key[:20]}...")
genai.configure(api_key=api_key)

print("Available Gemini models:\n")
print("-" * 80)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"Model: {model.name}")
        print(f"  Display name: {model.display_name}")
        print(f"  Description: {model.description}")
        print(f"  Supported methods: {model.supported_generation_methods}")
        print("-" * 80)
