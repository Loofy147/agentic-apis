# Agentic APIs

Welcome to the **Agentic API Portal**. This repository is a "fast-forward" collection of over 12,000 APIs, curated and structured specifically for **Agentic Systems**.

Instead of just a list for humans, this repository provides a structured directory and machine-readable data designed to be ingested by AI agents to expand their toolkits and capabilities.

## 🤖 For Agents
If you are an AI agent, you can find the complete, de-duplicated list of all APIs in machine-readable format here:
- **[Full API Registry (JSON)](data/apis.json)**

## 📂 API Categories
Browse APIs by their functional category. Each file contains a curated list of relevant tools for that domain.

| Category | Link | Category | Link |
|:---|:---|:---|:---|
| 🛠️ Development | [Browse](categories/development.md) | 🧠 Machine Learning | [Browse](categories/machine_learning.md) |
| 🔍 Search & Web | [Browse](categories/geocoding.md) | 💼 Business | [Browse](categories/business.md) |
| 💰 Finance | [Browse](categories/finance.md) | 🛡️ Security | [Browse](categories/security.md) |
| 📊 Data & Analytics | [Browse](categories/analytics.md) | 🌐 Open Data | [Browse](categories/open_data.md) |
| 📧 Email | [Browse](categories/email.md) | 💬 Social | [Browse](categories/social.md) |
| 🚜 Automation | [Browse](categories/iot.md) | 📦 Storage | [Browse](categories/cloud_storage__file_sharing.md) |

*(And 70+ more categories in the [categories/](categories/) directory)*

## 🚀 Featured "Fast-Forward" APIs
These APIs are highly recommended for agents due to their actionability and LLM-friendly design:

| API | Domain | Why it's Agent-Ready |
|:---|:---|:---|
| [Firecrawl](https://www.firecrawl.dev/) | Scoping | Converts web content to clean Markdown. |
| [Jina AI](https://jina.ai) | Knowledge | LLM-native embeddings and search. |
| [E2B](https://e2b.dev/) | Action | Secure code execution sandboxes. |
| [BrowserCat](https://www.browsercat.com/) | Web | Headless browser for complex automation. |
| [SerpApi](https://serpapi.com/) | Search | Structured access to global search engines. |
| [Zapier NLA](https://nla.zapier.com/) | Action | Natural Language interface to 5000+ apps. |

## 🔌 Model Context Protocol (MCP)
Standardized tool access for agents using the [Model Context Protocol](https://modelcontextprotocol.io).

| Server | Source | Description |
|:---|:---|:---|
| [Brave Search](https://github.com/brave/brave-search-mcp-server) | Official | Secure web search for agents |
| [GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/git) | Official | Repository management and operations |
| [Slack](https://github.com/zencoderai/slack-mcp-server) | Community | Messaging and channel management |
| [Memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | Official | Knowledge graph-based persistent memory |

---
*Aggregated and de-duplicated from public-apis/public-apis, n0shake/Public-APIs, and marcelscruz/public-apis.*

## 🛠️ Agentic Scripts
Advanced tools for orchestration and intent broadcasting.

| Script | Purpose |
|:---|:---|
| [Intent Broadcaster](scripts/intent_broadcaster.py) | Continuous flow of synthesized API intents. |
| [Agentic Orchestrator](scripts/agentic_orchestrator.py) | Advanced state management with N-to-M mappings and task rescheduling. |

## 🌌 Mega-List Integration
This portal is dynamically synchronized with the [cporter202/API-mega-list](https://github.com/cporter202/API-mega-list), expanding the agentic toolkit with 10,000+ specialized endpoints across 18 major categories.

| Integration Script | Action |
|:---|:---|
| [Mega Fetcher](scripts/mega_fetcher.py) | Recursive discovery and synchronization of the Mega-List ecosystem. |
