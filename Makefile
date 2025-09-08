.PHONY: help install install-dev test clean lint format run

GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m

help: ## Mostrar comandos disponíveis
	@echo "$(GREEN)Comandos disponíveis:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $1, $2}'

install: ## Instalar dependências básicas
	@echo "$(GREEN)Instalando dependências...$(NC)"
	pip install -r requirements.txt

install-dev: ## Instalar dependências de desenvolvimento  
	@echo "$(GREEN)Instalando dependências de desenvolvimento...$(NC)"
	pip install -r requirements-dev.txt

test: ## Executar testes
	@echo "$(GREEN)Executando testes...$(NC)"
	pytest tests/ -v

lint: ## Verificar código
	@echo "$(GREEN)Verificando código...$(NC)"
	flake8 src/ tests/ --max-line-length=88
	@echo "✅ Linting concluído"

format: ## Formatar código
	@echo "$(GREEN)Formatando código...$(NC)"
	black src/ tests/ examples/ scripts/
	@echo "✅ Formatação concluída"

clean: ## Limpar arquivos temporários
	@echo "$(GREEN)Limpando arquivos temporários...$(NC)"
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info/
	rm -rf data/temp/* data/cache/*
	@echo "✅ Limpeza concluída"

run: ## Executar aplicação
	@echo "$(GREEN)Executando aplicação...$(NC)"
	python main.py

setup-env: ## Configurar ambiente virtual
	@echo "$(GREEN)Configurando ambiente...$(NC)"
	python -m venv venv
	@echo "$(YELLOW)Ative com: source venv/bin/activate (Linux/Mac) ou venv\Scripts\activate (Windows)$(NC)"

example: ## Executar exemplo
	@echo "$(GREEN)Executando exemplo...$(NC)"
	python examples/exemplo_basico.py
