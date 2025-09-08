"""
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
