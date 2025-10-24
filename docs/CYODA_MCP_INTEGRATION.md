# 🔗 Cyoda MCP Integration Guide

## What is Cyoda?

**Cyoda** is an enterprise-grade data platform that provides a unified framework for managing entities, workflows, and integrations across complex systems. Think of it as a "data operating system" for enterprises.

## 🚀 Getting Started with Cyoda MCP

### Step 1: Request Cyoda Environment

Cyoda provides a conversational AI assistant to provision environments.

**Go to:** https://ai.cyoda.net/

**Chat with the AI:**

```
You: Deploy me a Cyoda environment please

AI: I'm provisioning a new Cyoda environment for you...
    Environment ID: abc-123-xyz
    Status: Creating...

    Your environment will be ready in 2-3 minutes.
```

**Wait for confirmation** that your environment is ready.

---

### Step 2: Get API Credentials

Once your environment is provisioned, request credentials:

```
You: Please give me credentials for my Cyoda environment

AI: Here are your credentials:

    Environment: https://your-env.cyoda.net
    Client ID: your_client_id_here
    Client Secret: your_client_secret_here

    Keep these secure! Don't share them publicly.
```

**Save these credentials** - you'll need them for the next step.

---

### Step 3: Install Cyoda MCP Python Package

**Official Package:** https://pypi.org/project/mcp-cyoda/
IDE/AI Assistant Integration
Add this to your MCP configuration (e.g., in Cursor, Claude Desktop, or other MCP-compatible tools):
```json
{
  "mcpServers": {
    "cyoda": {
      "command": "mcp-cyoda",
      "env": {
        "CYODA_CLIENT_ID": "your-client-id-here",
        "CYODA_CLIENT_SECRET": "your-client-secret-here",
        "CYODA_HOST": "client-123.eu.cyoda.net"
      }
    }
  }
}
```
