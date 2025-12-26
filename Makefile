.PHONY: help install setup frontend-install embed-tools start-cli start-ui start-all stop clean docker-build docker-up docker-down vllm-install vllm-serve

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)BlacksmithAI - AI-Powered Penetration Testing Framework$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation Targets
install: ## Install all Python dependencies
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	cd blacksmithAI && uv sync

setup: install docker-build frontend-install ## Complete initial setup (install deps, build docker, install frontend)
	@echo "$(GREEN)✓ Setup complete!$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Configure .env file: cp blacksmithAI/.env.example blacksmithAI/.env"
	@echo "  2. Edit blacksmithAI/config.json for your LLM provider"
	@echo "  3. Run 'make embed-tools' to index tool documentation"
	@echo "  4. Run 'make start-cli' or 'make start-ui' to begin"

frontend-install: ## Install frontend dependencies
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	cd frontend && pnpm install

# Docker Targets
docker-build: ## Build mini-kali Docker image
	@echo "$(BLUE)Building mini-kali Docker image...$(NC)"
	cd blacksmithAI && docker compose build

docker-up: ## Start mini-kali Docker container
	@echo "$(BLUE)Starting mini-kali Docker container...$(NC)"
	cd blacksmithAI && docker compose up -d
	@echo "$(GREEN)✓ mini-kali container started$(NC)"

docker-down: ## Stop mini-kali Docker container
	@echo "$(BLUE)Stopping mini-kali Docker container...$(NC)"
	cd blacksmithAI && docker compose down
	@echo "$(GREEN)✓ mini-kali container stopped$(NC)"

docker-logs: ## View Docker container logs
	cd blacksmithAI && docker compose logs -f

# Configuration Targets
embed-tools: ## Embed tool documentation for AI agents
	@echo "$(BLUE)Embedding tool documentation...$(NC)"
	uv run blacksmithAI/blacksmithAI/update_tool_documentation.py
	@echo "$(GREEN)✓ Tool documentation embedded$(NC)"

# VLLM Targets
vllm-install: ## Install VLLM for local LLM support
	@echo "$(BLUE)Installing VLLM...$(NC)"
	cd blacksmithAI && uv add vllm
	cd blacksmithAI && uv add huggingface_hub
	@echo "$(GREEN)✓ VLLM installed$(NC)"
	@echo "$(YELLOW)Next: Run 'make vllm-serve' to start the VLLM server$(NC)"

vllm-serve: ## Start VLLM server (make sure VLLM is installed first)
	@echo "$(BLUE)Starting VLLM server...$(NC)"
	@echo "$(YELLOW)Using model: mistralai/Devstral-2-123B-Instruct-2512$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop$(NC)"
	cd blacksmithAI && uv run vllm serve mistralai/Devstral-2-123B-Instruct-2512 \
		--host 0.0.0.0 \
		--port 8000 \
		--max-model-len 8192 \
		--gpu-memory-utilization 0.75

vllm-serve-small: ## Start VLLM server with smaller model (7B)
	@echo "$(BLUE)Starting VLLM server with Mistral 7B...$(NC)"
	@echo "$(YELLOW)Using model: mistralai/Mistral-7B-Instruct-v0.3$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop$(NC)"
	cd blacksmithAI && uv run vllm serve mistralai/Mistral-7B-Instruct-v0.3 \
		--host 0.0.0.0 \
		--port 8000 \
		--max-model-len 32768 \
		--gpu-memory-utilization 0.9

# Runtime Targets
start-cli: docker-up ## Start BlacksmithAI in CLI mode
	@echo "$(BLUE)Starting BlacksmithAI CLI...$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to exit$(NC)"
	cd blacksmithAI && uv run main.py

start-ui: docker-up ## Start BlacksmithAI Web UI (requires 3 terminals)
	@echo "$(BLUE)Starting BlacksmithAI Web UI...$(NC)"
	@echo "$(RED)This requires multiple terminals. Please run these commands manually:$(NC)"
	@echo ""
	@echo "$(YELLOW)Terminal 1:$(NC) cd blacksmithAI && docker compose up -d"
	@echo "$(YELLOW)Terminal 2:$(NC) cd frontend && pnpm build && pnpm start"
	@echo "$(YELLOW)Terminal 3:$(NC) cd blacksmithAI && uv run langgraph dev"
	@echo ""
	@echo "$(GREEN)Then access http://localhost:3000$(NC)"

start-all: ## Quick start - runs CLI mode (assumes setup is done)
	@echo "$(BLUE)Quick starting BlacksmithAI...$(NC)"
	@echo "$(YELLOW)Make sure you have:$(NC)"
	@echo "  - Installed dependencies (run 'make install' if not)"
	@echo "  - Built Docker image (run 'make docker-build' if not)"
	@echo "  - Configured .env and config.json"
	@echo "  - Embedded tool docs (run 'make embed-tools' if not)"
	@echo ""
	@read -p "$(YELLOW)Continue? [y/N] $(NC)" -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		cd blacksmithAI && docker compose up -d; \
		cd blacksmithAI && uv run main.py; \
	fi

# Development Targets
dev-ui: docker-up ## Start LangGraph dev server
	@echo "$(BLUE)Starting LangGraph dev server...$(NC)"
	cd blacksmithAI && uv run langgraph dev

dev-frontend: ## Start frontend development server
	@echo "$(BLUE)Starting frontend development server...$(NC)"
	cd frontend && pnpm dev

# Utility Targets
stop: docker-down ## Stop all services
	@echo "$(BLUE)Stopping all services...$(NC)"
	@echo "$(GREEN)✓ All services stopped$(NC)"

clean: ## Clean up Docker containers and images
	@echo "$(BLUE)Cleaning up...$(NC)"
	cd blacksmithAI && docker compose down -v --rmi all --remove-orphans
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

status: ## Show status of Docker containers
	@echo "$(BLUE)Docker container status:$(NC)"
	cd blacksmithAI && docker compose ps

# Testing/Verification Targets
check-deps: ## Check if all dependencies are installed
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@command -v uv >/dev/null 2>&1 || echo "$(RED)✗ uv not found$(NC)"
	@command -v docker >/dev/null 2>&1 || echo "$(RED)✗ docker not found$(NC)"
	@command -v node >/dev/null 2>&1 || echo "$(RED)✗ node not found$(NC)"
	@command -v pnpm >/dev/null 2>&1 || echo "$(RED)✗ pnpm not found$(NC)"
	@echo "$(GREEN)✓ Dependency check complete$(NC)"

check-config: ## Check if configuration files exist
	@echo "$(BLUE)Checking configuration...$(NC)"
	@test -f blacksmithAI/.env && echo "$(GREEN)✓ .env file exists$(NC)" || echo "$(RED)✗ .env file not found (copy from .env.example)$(NC)"
	@test -f blacksmithAI/config.json && echo "$(GREEN)✓ config.json exists$(NC)" || echo "$(RED)✗ config.json not found$(NC)"

# Documentation Targets
docs: ## Open documentation in browser (if available)
	@echo "$(BLUE)Opening documentation...$(NC)"
	@command -v xdg-open >/dev/null 2>&1 && xdg-open README.md || \
	command -v open >/dev/null 2>&1 && open README.md || \
	echo "Please open README.md in your browser"

# Quick Reference
quickstart: ## Display quick start guide
	@echo "$(BLUE)Quick Start Guide$(NC)"
	@echo ""
	@echo "$(GREEN)1. First Time Setup:$(NC)"
	@echo "   make setup"
	@echo "   cp blacksmithAI/.env.example blacksmithAI/.env"
	@echo "   # Edit .env with your API keys"
	@echo "   make embed-tools"
	@echo ""
	@echo "$(GREEN)2. Start CLI Mode:$(NC)"
	@echo "   make start-cli"
	@echo ""
	@echo "$(GREEN)3. Start Web UI Mode (requires 3 terminals):$(NC)"
	@echo "   Terminal 1: make docker-up"
	@echo "   Terminal 2: cd frontend && pnpm build && pnpm start"
	@echo "   Terminal 3: cd blacksmithAI && uv run langgraph dev"
	@echo "   # Open http://localhost:3000"
	@echo ""
	@echo "$(GREEN)4. Using VLLM (Local LLM):$(NC)"
	@echo "   make vllm-install"
	@echo "   make vllm-serve"
	@echo "   # Update config.json to use provider: 'vllm'"
	@echo ""
	@echo "$(YELLOW)For more help: make help$(NC)"
