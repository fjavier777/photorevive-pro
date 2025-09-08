"""Exemplo básico de uso"""

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
    
    print(f"\n✅ Resultado em: {pasta_saida}")
    print("💡 Compare as imagens antes e depois!")

if __name__ == "__main__":
    main()
