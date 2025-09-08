"""Testes básicos do melhorador fotográfico"""

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
