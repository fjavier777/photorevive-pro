#!/usr/bin/env python3
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
        print("\n✅ Processamento concluído!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
