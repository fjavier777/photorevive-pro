#!/usr/bin/env python3
"""
Script de Configuração Automática
Sistema de Melhoria Fotográfica v2.0

Este script configura automaticamente toda a estrutura do projeto.
Execute: python setup_project.py
"""

import os
import sys
import subprocess
from pathlib import Path
import json

def run_command(command, check=True, shell=True):
    """Executa comando no sistema"""
    try:
        result = subprocess.run(command, shell=shell, check=check, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def create_file(path, content):
    """Cria arquivo com conteúdo"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Criado: {path}")

def create_directory(path):
    """Cria diretório"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"📁 Pasta: {path}")

def create_init_file(path):
    """Cria arquivo __init__.py"""
    create_file(Path(path) / "__init__.py", "# Package initialization\n")

def create_gitkeep(path):
    """Cria arquivo .gitkeep para manter pasta no git"""
    create_file(Path(path) / ".gitkeep", "# Keep this directory in git\n")

def setup_project_structure():
    """Cria estrutura completa do projeto"""
    
    print("🏗️ Criando estrutura de pastas...")
    
    # Estrutura principal
    directories = [
        "src", "src/processadores", "src/utils", "src/config",
        "tests", "tests/test_images",
        "examples", "examples/imagens_exemplo", 
        "docs", "docs/imagens",
        "scripts",
        "data", "data/temp", "data/cache", "data/profiles",
        "gui",
        "fotos", "fotos_melhoradas",
        ".vscode", ".github", ".github/workflows",
        "logs"
    ]
    
    for directory in directories:
        create_directory(directory)
    
    # Arquivos __init__.py
    init_files = [
        "src", "src/processadores", "src/utils", "src/config",
        "tests", "gui"
    ]
    
    for init_path in init_files:
        create_init_file(init_path)
    
    # Arquivos .gitkeep
    gitkeep_dirs = [
        "fotos", "fotos_melhoradas", "data/temp", 
        "data/cache", "examples/imagens_exemplo",
        "tests/test_images", "logs"
    ]
    
    for gitkeep_dir in gitkeep_dirs:
        create_gitkeep(gitkeep_dir)

def create_requirements_files():
    """Cria arquivos de requirements"""
    
    print("\n📦 Criando arquivos de dependências...")
    
    requirements = """# Processamento de imagem
opencv-python>=4.8.0
Pillow>=10.0.0
numpy>=1.24.0

# Dependências opcionais para melhor performance
opencv-contrib-python>=4.8.0  # Para algoritmos extras do OpenCV
scipy>=1.10.0                  # Para processamento científico avançado

# Para desenvolvimento (opcional)
matplotlib>=3.7.0              # Para visualização de histogramas
tqdm>=4.65.0                  # Para barras de progresso
"""
    
    requirements_dev = """# Dependências principais
-r requirements.txt

# Desenvolvimento
black>=23.0.0           # Code formatter
flake8>=6.0.0          # Linter
pylint>=2.17.0         # Code analysis
mypy>=1.0.0            # Type checking

# Testing
pytest>=7.4.0          # Testing framework
pytest-cov>=4.1.0     # Coverage
pytest-mock>=3.11.0   # Mocking

# Documentation
sphinx>=7.0.0          # Documentation generator
sphinx-rtd-theme>=1.3.0

# Development tools
pre-commit>=3.3.0      # Git hooks
bump2version>=1.0.0    # Version management
twine>=4.0.0           # PyPI uploads
"""
    
    requirements_gui = """# GUI Dependencies
-r requirements.txt

# Interface gráfica
tkinter             # Built-in GUI (usually included)
PyQt5>=5.15.0      # Alternative GUI framework
Pillow>=10.0.0     # Image handling for GUI
"""
    
    create_file("requirements.txt", requirements)
    create_file("requirements-dev.txt", requirements_dev)
    create_file("requirements-gui.txt", requirements_gui)

def create_vscode_config():
    """Cria configurações do VSCode"""
    
    print("\n⚙️ Criando configurações do VSCode...")
    
    settings = {
        "python.defaultInterpreterPath": "./venv/bin/python",
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.linting.flake8Enabled": True,
        "python.formatting.provider": "black",
        "python.formatting.blackArgs": ["--line-length=88"],
        "python.testing.pytestEnabled": True,
        "python.testing.pytestArgs": ["tests/"],
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
            "**/node_modules": True,
            "fotos/**": True,
            "fotos_melhoradas/**": True,
            "data/temp/**": True,
            "data/cache/**": True
        },
        "python.analysis.extraPaths": ["src/"],
        "editor.rulers": [88],
        "editor.formatOnSave": True,
        "files.trimTrailingWhitespace": True,
        "files.insertFinalNewline": True
    }
    
    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Debug Main",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/main.py",
                "args": ["medio"],
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}",
                "env": {"PYTHONPATH": "${workspaceFolder}/src"}
            },
            {
                "name": "Run Tests",
                "type": "python",
                "request": "launch",
                "module": "pytest",
                "args": ["tests/", "-v"],
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}"
            }
        ]
    }
    
    tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Run Tests",
                "type": "shell",
                "command": "python",
                "args": ["-m", "pytest", "tests/", "-v"],
                "group": "test",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                }
            },
            {
                "label": "Format Code",
                "type": "shell",
                "command": "black",
                "args": ["src/", "tests/", "examples/"],
                "group": "build"
            }
        ]
    }
    
    extensions = {
        "recommendations": [
            "ms-python.python",
            "ms-python.flake8", 
            "ms-python.black-formatter",
            "ms-python.pylint",
            "ms-python.mypy-type-checker",
            "ms-vscode.makefile-tools",
            "redhat.vscode-yaml",
            "yzhang.markdown-all-in-one"
        ]
    }
    
    create_file(".vscode/settings.json", json.dumps(settings, indent=2))
    create_file(".vscode/launch.json", json.dumps(launch, indent=2))
    create_file(".vscode/tasks.json", json.dumps(tasks, indent=2))
    create_file(".vscode/extensions.json", json.dumps(extensions, indent=2))

def create_gitignore():
    """Cria arquivo .gitignore"""
    
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
.AppleDouble
.LSOverride
Thumbs.db
ehthumbs.db
Desktop.ini

# Projeto específico
fotos/
fotos_melhoradas/
data/temp/
data/cache/
logs/*.log

# Imagens grandes (descomente se necessário)
*.jpg
*.jpeg
*.png
*.tiff
*.bmp
*.gif
*.webp
*.raw

# Mantém exemplos pequenos (descomente se necessário)
# !examples/imagens_exemplo/*.jpg
# !examples/imagens_exemplo/*.png

# Arquivos temporários
*.tmp
*.bak
*.backup
*~
"""
    
    create_file(".gitignore", gitignore_content)

def create_main_files():
    """Cria arquivos principais"""
    
    print("\n📄 Criando arquivos principais...")
    
    main_py = '''#!/usr/bin/env python3
"""
Sistema Avançado de Melhoria Fotográfica
Entry point principal da aplicação
"""

import sys
import os
import argparse

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from melhorador_fotografico import MelhoradorFotografico

def main():
    parser = argparse.ArgumentParser(
        description='Sistema Avançado de Melhoria Fotográfica v2.0'
    )
    
    parser.add_argument('intensidade', nargs='?', default='medio',
                       choices=['leve', 'medio', 'forte'],
                       help='Intensidade do processamento')
    
    parser.add_argument('pasta_entrada', nargs='?', default='fotos',
                       help='Pasta com fotos originais')
    
    parser.add_argument('pasta_saida', nargs='?', default='fotos_melhoradas',
                       help='Pasta para fotos processadas')
    
    parser.add_argument('--no-auto', action='store_true',
                       help='Desativar ajuste automático')
    
    args = parser.parse_args()
    auto_ajuste = not args.no_auto
    
    print("🎨 Sistema de Melhoria Fotográfica v2.0")
    print("=" * 40)
    
    try:
        melhorador = MelhoradorFotografico()
        melhorador.processar_pasta(
            args.pasta_entrada, args.pasta_saida, 
            args.intensidade, auto_ajuste
        )
        print("\\n✅ Processamento concluído!")
        
    except KeyboardInterrupt:
        print("\\n⏹️ Interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    # Código da classe principal (versão simplificada para o setup)
    melhorador_py = '''"""
Sistema Avançado de Melhoria Fotográfica
Classe principal com processamento inteligente
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
from typing import Dict, Tuple, Optional

class MelhoradorFotografico:
    """Melhorador fotográfico com análise automática"""
    
    def __init__(self):
        self.ajustes = {
            "leve": {
                "cor": 1.05, "contraste": 1.05, "brilho": 1.02, "nitidez": 1.05,
                "gamma": 1.0, "ruido": 0.3, "vibrancia": 1.03, "sombras": 0.05
            },
            "medio": {
                "cor": 1.15, "contraste": 1.1, "brilho": 1.05, "nitidez": 1.1,
                "gamma": 1.05, "ruido": 0.5, "vibrancia": 1.08, "sombras": 0.1
            },
            "forte": {
                "cor": 1.25, "contraste": 1.2, "brilho": 1.1, "nitidez": 1.2,
                "gamma": 1.1, "ruido": 0.7, "vibrancia": 1.15, "sombras": 0.15
            }
        }
    
    def corrigir_gamma(self, img: np.ndarray, gamma: float) -> np.ndarray:
        """Aplica correção de gamma"""
        if gamma == 1.0:
            return img
        
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
        return cv2.LUT(img, table)
    
    def detectar_qualidade_imagem(self, img: np.ndarray) -> dict:
        """Analisa qualidade da imagem"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Nitidez (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Histograma
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_norm = hist / hist.sum()
        
        # Análise de exposição
        pixels_escuros = np.sum(hist_norm[:50])
        pixels_claros = np.sum(hist_norm[200:])
        
        # Ruído estimado
        ruido = np.std(cv2.medianBlur(gray, 5) - gray)
        
        return {
            "nitidez": laplacian_var,
            "subexposta": pixels_escuros > 0.3,
            "superexposta": pixels_claros > 0.3,
            "ruido": ruido,
            "contraste_baixo": np.std(gray) < 40
        }
    
    def melhorar_foto_familia(self, caminho_imagem: str, salvar_como: str,
                            intensidade: str = "medio", auto_ajuste: bool = True) -> bool:
        """Melhora foto com processamento avançado"""
        
        if intensidade not in self.ajustes:
            raise ValueError("Intensidade deve ser: leve, medio ou forte")
        
        img = cv2.imread(caminho_imagem)
        if img is None:
            print(f"⚠️ Erro ao abrir: {caminho_imagem}")
            return False
        
        print(f"📸 Processando {os.path.basename(caminho_imagem)}...")
        config = self.ajustes[intensidade].copy()
        
        # Análise automática
        if auto_ajuste:
            qualidade = self.detectar_qualidade_imagem(img)
            print(f"  🔍 Nitidez: {qualidade['nitidez']:.1f}, Ruído: {qualidade['ruido']:.1f}")
        
        # Processamento básico
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        
        # Aplicar melhorias
        pil_img = ImageEnhance.Color(pil_img).enhance(config["cor"])
        pil_img = ImageEnhance.Contrast(pil_img).enhance(config["contraste"])
        pil_img = ImageEnhance.Brightness(pil_img).enhance(config["brilho"])
        pil_img = ImageEnhance.Sharpness(pil_img).enhance(config["nitidez"])
        
        # Salvar
        pil_img.save(salvar_como, quality=95, optimize=True)
        print(f"  ✅ Salvo como: {os.path.basename(salvar_como)}")
        return True
    
    def processar_pasta(self, pasta_entrada: str = "fotos",
                       pasta_saida: str = "fotos_melhoradas",
                       intensidade: str = "medio",
                       auto_ajuste: bool = True) -> None:
        """Processa pasta completa"""
        
        if not os.path.exists(pasta_entrada):
            print(f"❌ Pasta '{pasta_entrada}' não encontrada!")
            print("💡 Crie a pasta e adicione suas fotos")
            return
        
        os.makedirs(pasta_saida, exist_ok=True)
        
        extensoes = [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"]
        arquivos_processados = 0
        
        print(f"🚀 Processamento: {intensidade}")
        print(f"📁 Entrada: {pasta_entrada}")
        print(f"📁 Saída: {pasta_saida}")
        print("-" * 40)
        
        for arquivo in sorted(os.listdir(pasta_entrada)):
            if any(arquivo.lower().endswith(ext) for ext in extensoes):
                entrada = os.path.join(pasta_entrada, arquivo)
                saida = os.path.join(pasta_saida, arquivo)
                
                try:
                    if self.melhorar_foto_familia(entrada, saida, intensidade, auto_ajuste):
                        arquivos_processados += 1
                except Exception as e:
                    print(f"❌ Erro em {arquivo}: {e}")
        
        print("-" * 40)
        print(f"🎉 {arquivos_processados} fotos processadas!")
        
        if arquivos_processados == 0:
            print("💡 Adicione fotos (.jpg, .png, etc.) na pasta de entrada")
'''
    
    create_file("main.py", main_py)
    create_file("src/melhorador_fotografico.py", melhorador_py)

def create_makefile():
    """Cria Makefile com comandos úteis"""
    
    makefile_content = '''.PHONY: help install install-dev test clean lint format run

GREEN=\\033[0;32m
YELLOW=\\033[1;33m
NC=\\033[0m

help: ## Mostrar comandos disponíveis
	@echo "$(GREEN)Comandos disponíveis:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\\n", $1, $2}'

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
	@echo "$(YELLOW)Ative com: source venv/bin/activate (Linux/Mac) ou venv\\Scripts\\activate (Windows)$(NC)"

example: ## Executar exemplo
	@echo "$(GREEN)Executando exemplo...$(NC)"
	python examples/exemplo_basico.py
'''
    
    create_file("Makefile", makefile_content)

def create_basic_tests():
    """Cria testes básicos"""
    
    test_content = '''"""Testes básicos do melhorador fotográfico"""

import pytest
import sys
import os
import tempfile
import numpy as np
from pathlib import Path
from PIL import Image

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from melhorador_fotografico import MelhoradorFotografico

class TestMelhoradorFotografico:
    
    def setup_method(self):
        """Configuração para cada teste"""
        self.melhorador = MelhoradorFotografico()
    
    def test_inicializacao(self):
        """Testa inicialização da classe"""
        assert self.melhorador is not None
        assert hasattr(self.melhorador, 'ajustes')
        assert 'leve' in self.melhorador.ajustes
        assert 'medio' in self.melhorador.ajustes
        assert 'forte' in self.melhorador.ajustes
    
    def test_configuracoes_intensidade(self):
        """Testa configurações de intensidade"""
        leve = self.melhorador.ajustes['leve']
        forte = self.melhorador.ajustes['forte']
        
        # Forte deve ter valores maiores
        assert forte['cor'] > leve['cor']
        assert forte['contraste'] > leve['contraste']
        assert forte['nitidez'] > leve['nitidez']
    
    def test_corrigir_gamma(self):
        """Testa correção de gamma"""
        img_test = np.ones((50, 50, 3), dtype=np.uint8) * 128
        
        # Gamma > 1 escurece
        img_dark = self.melhorador.corrigir_gamma(img_test, 1.2)
        assert np.mean(img_dark) < np.mean(img_test)
        
        # Gamma < 1 clareia
        img_light = self.melhorador.corrigir_gamma(img_test, 0.8)
        assert np.mean(img_light) > np.mean(img_test)
    
    def test_detectar_qualidade(self):
        """Testa detecção de qualidade"""
        img_test = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        qualidade = self.melhorador.detectar_qualidade_imagem(img_test)
        
        assert 'nitidez' in qualidade
        assert 'ruido' in qualidade
        assert 'subexposta' in qualidade
        assert 'superexposta' in qualidade
        assert qualidade['ruido'] >= 0
    
    def test_melhorar_foto_inexistente(self):
        """Testa com arquivo inexistente"""
        resultado = self.melhorador.melhorar_foto_familia(
            "arquivo_inexistente.jpg", 
            "saida.jpg", 
            "leve"
        )
        assert resultado == False
    
    @pytest.fixture
    def imagem_temp(self):
        """Fixture: cria imagem temporária"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            img = Image.new('RGB', (100, 100), color='blue')
            img.save(tmp.name, 'JPEG')
            yield tmp.name
            os.unlink(tmp.name)
    
    def test_processar_imagem_real(self, imagem_temp):
        """Testa processamento com imagem real"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as saida:
            resultado = self.melhorador.melhorar_foto_familia(
                imagem_temp, saida.name, 'leve'
            )
            
            assert resultado == True
            assert os.path.exists(saida.name)
            assert os.path.getsize(saida.name) > 0
            
            os.unlink(saida.name)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
    
    create_file("tests/test_melhorador.py", test_content)

def create_examples():
    """Cria exemplos de uso"""
    
    exemplo_basico = '''"""Exemplo básico de uso"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from melhorador_fotografico import MelhoradorFotografico

def main():
    print("📷 Exemplo Básico")
    print("=" * 30)
    
    melhorador = MelhoradorFotografico()
    
    # Verificar se há imagens de exemplo
    pasta_exemplo = Path(__file__).parent / "imagens_exemplo"
    
    if not pasta_exemplo.exists() or not any(pasta_exemplo.iterdir()):
        print("❌ Adicione imagens em examples/imagens_exemplo/")
        print("💡 Formatos suportados: .jpg, .png, .tiff, .bmp")
        return
    
    # Processar exemplos
    pasta_saida = Path(__file__).parent / "resultado_exemplo"
    
    print(f"🔄 Processando imagens...")
    melhorador.processar_pasta(
        str(pasta_exemplo),
        str(pasta_saida),
        "medio",
        auto_ajuste=True
    )
    
    print(f"\\n✅ Resultado em: {pasta_saida}")
    print("💡 Compare as imagens antes e depois!")

if __name__ == "__main__":
    main()
'''
    
    create_file("examples/exemplo_basico.py", exemplo_basico)

def setup_virtual_environment():
    """Configura ambiente virtual"""
    
    print("\\n🐍 Configurando ambiente virtual...")
    
    # Verificar se Python está disponível
    success, stdout, stderr = run_command("python --version", check=False)
    if not success:
        success, stdout, stderr = run_command("python3 --version", check=False)
        if not success:
            print("❌ Python não encontrado!")
            return False
    
    python_cmd = "python" if "python --version" else "python3"
    print(f"✅ Python encontrado: {stdout.strip()}")
    
    # Criar ambiente virtual
    if not Path("venv").exists():
        print("🔧 Criando ambiente virtual...")
        success, _, stderr = run_command(f"{python_cmd} -m venv venv")
        if not success:
            print(f"❌ Erro ao criar venv: {stderr}")
            return False
        print("✅ Ambiente virtual criado!")
    else:
        print("✅ Ambiente virtual já existe!")
    
    return True

def install_dependencies():
    """Instala dependências básicas"""
    
    print("\\n📦 Instalando dependências...")
    
    # Detectar comando pip do ambiente virtual
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Linux/Mac
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Instalar requirements básicos
    if Path("requirements.txt").exists():
        success, stdout, stderr = run_command(f"{pip_cmd} install -r requirements.txt")
        if success:
            print("✅ Dependências básicas instaladas!")
        else:
            print(f"⚠️ Algumas dependências falharam: {stderr}")
            return False
    
    return True

def initialize_git():
    """Inicializa repositório Git"""
    
    print("\\n📝 Configurando Git...")
    
    if not Path(".git").exists():
        success, _, _ = run_command("git --version", check=False)
        if not success:
            print("⚠️ Git não encontrado - pulando inicialização")
            return False
        
        run_command("git init")
        print("✅ Repositório Git inicializado!")
        
        # Commit inicial
        run_command("git add .", check=False)
        run_command('git commit -m "Configuração inicial do projeto"', check=False)
        print("✅ Commit inicial criado!")
    else:
        print("✅ Repositório Git já existe!")
    
    return True

def create_sample_images():
    """Cria imagens de exemplo para teste"""
    
    print("\\n🖼️ Criando imagens de exemplo...")
    
    try:
        from PIL import Image, ImageDraw
        import numpy as np
        
        exemplo_dir = Path("examples/imagens_exemplo")
        
        # Imagem colorida simples
        img1 = Image.new('RGB', (300, 200), color='lightblue')
        draw1 = ImageDraw.Draw(img1)
        draw1.rectangle([50, 50, 250, 150], fill='red', outline='darkred', width=3)
        draw1.text((120, 90), "EXEMPLO", fill='white')
        img1.save(exemplo_dir / "exemplo_colorido.jpg", quality=85)
        
        # Imagem com gradiente
        img2 = Image.new('RGB', (300, 200))
        pixels = []
        for y in range(200):
            for x in range(300):
                r = int(255 * x / 300)
                g = int(255 * y / 200)
                b = 128
                pixels.append((r, g, b))
        img2.putdata(pixels)
        img2.save(exemplo_dir / "exemplo_gradiente.png")
        
        print("✅ Imagens de exemplo criadas!")
        
    except ImportError:
        print("⚠️ PIL não disponível - imagens de exemplo não criadas")
        # Criar arquivos placeholder
        (exemplo_dir / "README.txt").write_text(
            "Adicione suas imagens de teste aqui\\n"
            "Formatos suportados: .jpg, .jpeg, .png, .tiff, .bmp"
        )

def print_final_instructions():
    """Exibe instruções finais"""
    
    print("\\n" + "="*60)
    print("🎉 PROJETO CONFIGURADO COM SUCESSO!")
    print("="*60)
    
    print("\\n📋 PRÓXIMOS PASSOS:")
    
    if os.name == 'nt':  # Windows
        print("\\n1️⃣ Ativar ambiente virtual:")
        print("   venv\\Scripts\\activate")
    else:  # Linux/Mac
        print("\\n1️⃣ Ativar ambiente virtual:")
        print("   source venv/bin/activate")
    
    print("\\n2️⃣ Instalar dependências (se necessário):")
    print("   pip install -r requirements.txt")
    
    print("\\n3️⃣ Testar instalação:")
    print("   python main.py --help")
    
    print("\\n4️⃣ Executar testes:")
    print("   pytest tests/ -v")
    
    print("\\n5️⃣ Abrir no VSCode:")
    print("   code .")
    
    print("\\n📁 ESTRUTURA CRIADA:")
    print("   ├── src/              # Código principal")
    print("   ├── tests/            # Testes automatizados") 
    print("   ├── examples/         # Exemplos de uso")
    print("   ├── fotos/            # Suas fotos (adicione aqui)")
    print("   ├── fotos_melhoradas/ # Resultado processado")
    print("   └── .vscode/          # Configurações VSCode")
    
    print("\\n🚀 COMANDOS ÚTEIS:")
    print("   make help          # Ver todos os comandos")
    print("   make test          # Executar testes")
    print("   make format        # Formatar código")
    print("   make clean         # Limpar temporários")
    
    print("\\n💡 PARA COMEÇAR:")
    print("   1. Adicione fotos na pasta 'fotos/'")
    print("   2. Execute: python main.py")
    print("   3. Veja resultados em 'fotos_melhoradas/'")
    
    print("\\n📖 DOCUMENTAÇÃO:")
    print("   README.md          # Documentação completa")
    print("   examples/          # Exemplos práticos")

def main():
    """Função principal do setup"""
    
    print("🚀 CONFIGURADOR AUTOMÁTICO")
    print("Sistema de Melhoria Fotográfica v2.0")
    print("="*50)
    
    try:
        # 1. Criar estrutura
        setup_project_structure()
        
        # 2. Criar arquivos de configuração
        create_requirements_files()
        create_vscode_config()
        create_gitignore()
        
        # 3. Criar arquivos principais
        create_main_files()
        create_makefile()
        
        # 4. Criar testes e exemplos
        create_basic_tests()
        create_examples()
        
        # 5. Configurar ambiente virtual
        if setup_virtual_environment():
            install_dependencies()
        
        # 6. Inicializar Git
        initialize_git()
        
        # 7. Criar imagens de exemplo
        create_sample_images()
        
        # 8. Instruções finais
        print_final_instructions()
        
    except KeyboardInterrupt:
        print("\\n⏹️ Configuração interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Erro durante configuração: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()