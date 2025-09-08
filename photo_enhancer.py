import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os
import sys
from typing import Tuple, Optional

class MelhoradorFotografico:
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
        """Aplica correção de gamma para melhorar exposição"""
        if gamma == 1.0:
            return img
        
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
        return cv2.LUT(img, table)
    
    def reduzir_ruido(self, img: np.ndarray, intensidade: float) -> np.ndarray:
        """Remove ruído da imagem usando filtro bilateral"""
        if intensidade <= 0:
            return img
        
        # Parâmetros ajustados baseados na intensidade
        d = int(5 + intensidade * 4)  # Diâmetro do kernel
        sigma_color = 50 + intensidade * 30
        sigma_space = 50 + intensidade * 30
        
        return cv2.bilateralFilter(img, d, sigma_color, sigma_space)
    
    def melhorar_sombras_realces(self, img: np.ndarray, intensidade: float) -> np.ndarray:
        """Melhora detalhes em sombras e realces"""
        if intensidade <= 0:
            return img
        
        # Converte para LAB para trabalhar apenas com luminância
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Aplica CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=1.0 + intensidade * 2, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Reconstrói a imagem
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    def ajustar_vibrancia(self, pil_img: Image.Image, vibrancia: float) -> Image.Image:
        """Ajusta vibrância sem supersaturar tons de pele"""
        if vibrancia == 1.0:
            return pil_img
        
        # Converte para HSV para trabalhar com saturação
        hsv = pil_img.convert('HSV')
        h, s, v = hsv.split()
        
        # Ajusta saturação de forma não-linear
        s_array = np.array(s)
        # Protege tons de pele (geralmente na faixa 10-40 graus no HSV)
        h_array = np.array(h)
        
        # Máscara para tons de pele (aproximação)
        tons_pele = ((h_array >= 5) & (h_array <= 25)) | ((h_array >= 160) & (h_array <= 180))
        
        # Aplica vibrância reduzida em tons de pele
        fator_pele = 1.0 + (vibrancia - 1.0) * 0.3
        fator_outros = vibrancia
        
        s_array = s_array.astype(float)
        s_array[tons_pele] *= fator_pele
        s_array[~tons_pele] *= fator_outros
        s_array = np.clip(s_array, 0, 255).astype(np.uint8)
        
        s_nova = Image.fromarray(s_array)
        hsv_nova = Image.merge('HSV', (h, s_nova, v))
        
        return hsv_nova.convert('RGB')
    
    def detectar_qualidade_imagem(self, img: np.ndarray) -> dict:
        """Analisa a qualidade da imagem para ajustar processamento"""
        # Calcula métricas de qualidade
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detecta borramento (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Analisa distribuição de histograma
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_norm = hist / hist.sum()
        
        # Detecta subexposição/superexposição
        pixels_escuros = np.sum(hist_norm[:50])
        pixels_claros = np.sum(hist_norm[200:])
        
        # Calcula ruído estimado
        ruido = np.std(cv2.medianBlur(gray, 5) - gray)
        
        return {
            "nitidez": laplacian_var,
            "subexposta": pixels_escuros > 0.3,
            "superexposta": pixels_claros > 0.3,
            "ruido": ruido,
            "contraste_baixo": np.std(gray) < 40
        }
    
    def ajustar_automatico(self, config: dict, qualidade: dict) -> dict:
        """Ajusta parâmetros baseado na qualidade detectada"""
        config_auto = config.copy()
        
        # Se imagem borrada, aumenta nitidez
        if qualidade["nitidez"] < 100:
            config_auto["nitidez"] *= 1.2
        
        # Se subexposta, aumenta brilho e sombras
        if qualidade["subexposta"]:
            config_auto["brilho"] *= 1.1
            config_auto["sombras"] *= 1.5
        
        # Se superexposta, reduz brilho
        if qualidade["superexposta"]:
            config_auto["brilho"] *= 0.95
        
        # Se muito ruído, reduz nitidez e aumenta redução de ruído
        if qualidade["ruido"] > 8:
            config_auto["nitidez"] *= 0.9
            config_auto["ruido"] *= 1.3
        
        # Se contraste baixo, aumenta contraste
        if qualidade["contraste_baixo"]:
            config_auto["contraste"] *= 1.15
        
        return config_auto
    
    def aplicar_filtro_cinematico(self, img: np.ndarray, intensidade: float = 0.3) -> np.ndarray:
        """Aplica um filtro cinematográfico sutil"""
        if intensidade <= 0:
            return img
        
        # Cria uma curva S suave para look cinematográfico
        img_float = img.astype(np.float32) / 255.0
        
        # Aplica curva S
        img_float = np.power(img_float, 0.9)  # Lift nas sombras
        img_float = np.clip(img_float * 1.05, 0, 1)  # Pequeno boost geral
        
        # Adiciona um toque quente nas sombras e frio nos realces
        lab = cv2.cvtColor((img_float * 255).astype(np.uint8), cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Toque quente/frio baseado na luminância
        l_norm = l.astype(np.float32) / 255.0
        a = a.astype(np.float32)
        b = b.astype(np.float32)
        
        # Sombras mais quentes (vermelho-amarelo)
        mascara_sombras = l_norm < 0.3
        a[mascara_sombras] += intensidade * 5
        b[mascara_sombras] += intensidade * 3
        
        # Realces ligeiramente mais frios
        mascara_realces = l_norm > 0.7
        a[mascara_realces] -= intensidade * 2
        b[mascara_realces] -= intensidade * 1
        
        a = np.clip(a, 0, 255).astype(np.uint8)
        b = np.clip(b, 0, 255).astype(np.uint8)
        
        lab_nova = cv2.merge([l, a, b])
        return cv2.cvtColor(lab_nova, cv2.COLOR_LAB2BGR)
    
    def melhorar_foto_familia(self, caminho_imagem: str, salvar_como: str, 
                            intensidade: str = "medio", auto_ajuste: bool = True) -> bool:
        """
        Melhora fotos de família com processamento fotográfico avançado
        
        Args:
            caminho_imagem: Caminho para a imagem original
            salvar_como: Caminho onde salvar a imagem processada
            intensidade: "leve", "medio" ou "forte"
            auto_ajuste: Se deve ajustar automaticamente baseado na qualidade
        
        Returns:
            bool: True se processamento foi bem-sucedido
        """
        if intensidade not in self.ajustes:
            raise ValueError("Escolha a intensidade entre: leve, medio ou forte")
        
        # Carrega imagem
        img = cv2.imread(caminho_imagem)
        if img is None:
            print(f"⚠️ Não consegui abrir {caminho_imagem}")
            return False
        
        print(f"📸 Processando {os.path.basename(caminho_imagem)}...")
        
        config = self.ajustes[intensidade].copy()
        
        # Análise automática de qualidade
        if auto_ajuste:
            qualidade = self.detectar_qualidade_imagem(img)
            config = self.ajustar_automatico(config, qualidade)
            print(f"🔍 Qualidade detectada - Nitidez: {qualidade['nitidez']:.1f}, "
                  f"Ruído: {qualidade['ruido']:.1f}")
        
        # Redução de ruído (OpenCV)
        img_denoised = self.reduzir_ruido(img, config["ruido"])
        
        # Correção de gamma
        img_gamma = self.corrigir_gamma(img_denoised, config["gamma"])
        
        # Melhoria de sombras e realces
        img_sombras = self.melhorar_sombras_realces(img_gamma, config["sombras"])
        
        # Filtro cinematográfico sutil
        img_cinema = self.aplicar_filtro_cinematico(img_sombras, 0.2 if intensidade != "leve" else 0.1)
        
        # Converte para PIL para ajustes finais
        img_rgb = cv2.cvtColor(img_cinema, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        
        # Ajustes fotográficos refinados
        # Vibrância inteligente (protege tons de pele)
        if config["vibrancia"] != 1.0:
            pil_img = self.ajustar_vibrancia(pil_img, config["vibrancia"])
        
        # Contraste e brilho
        pil_img = ImageEnhance.Contrast(pil_img).enhance(config["contraste"])
        pil_img = ImageEnhance.Brightness(pil_img).enhance(config["brilho"])
        
        # Nitidez com máscara inteligente
        if config["nitidez"] > 1.0:
            # Aplica nitidez apenas em áreas com detalhes (evita ruído)
            img_array = np.array(pil_img)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Detecta bordas para aplicar nitidez seletiva
            edges = cv2.Canny(gray, 50, 150)
            edges_dilated = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=1)
            mask = edges_dilated.astype(float) / 255.0
            
            # Aplica nitidez
            img_sharp = ImageEnhance.Sharpness(pil_img).enhance(config["nitidez"])
            img_sharp_array = np.array(img_sharp)
            
            # Combina usando a máscara
            for canal in range(3):
                img_array[:,:,canal] = (
                    img_array[:,:,canal] * (1 - mask) + 
                    img_sharp_array[:,:,canal] * mask
                ).astype(np.uint8)
            
            pil_img = Image.fromarray(img_array)
        
        # Ajuste final de micro-contraste
        pil_img = self.aplicar_micro_contraste(pil_img, 0.1 if intensidade != "leve" else 0.05)
        
        # Salva com qualidade máxima
        pil_img.save(salvar_como, quality=95, optimize=True)
        
        print(f"✅ {salvar_como} salvo com sucesso ({intensidade})")
        return True
    
    def aplicar_micro_contraste(self, pil_img: Image.Image, intensidade: float) -> Image.Image:
        """Aplica micro-contraste para mais definição"""
        if intensidade <= 0:
            return pil_img
        
        # Converte para array
        img_array = np.array(pil_img).astype(np.float32)
        
        # Aplica filtro passa-alta sutil
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]]) * intensidade
        kernel[1, 1] = 1 + intensidade * 8
        
        # Aplica o filtro em cada canal
        for canal in range(img_array.shape[2]):
            img_array[:,:,canal] = cv2.filter2D(img_array[:,:,canal], -1, kernel)
        
        # Garante que os valores estão no range correto
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    def analisar_temperatura_cor(self, img: np.ndarray) -> float:
        """Analisa a temperatura de cor da imagem"""
        # Converte para RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Calcula médias dos canais
        r_mean = np.mean(img_rgb[:,:,0])
        g_mean = np.mean(img_rgb[:,:,1])
        b_mean = np.mean(img_rgb[:,:,2])
        
        # Calcula razão azul/vermelho (indicador de temperatura)
        if r_mean > 0:
            temp_ratio = b_mean / r_mean
            return temp_ratio
        return 1.0
    
    def corrigir_balance_branco(self, img: np.ndarray, intensidade: float = 0.3) -> np.ndarray:
        """Aplica correção automática de balanço de branco"""
        if intensidade <= 0:
            return img
        
        # Método Gray World para correção automática
        img_float = img.astype(np.float32)
        
        # Calcula médias dos canais
        mean_b = np.mean(img_float[:,:,0])
        mean_g = np.mean(img_float[:,:,1])
        mean_r = np.mean(img_float[:,:,2])
        
        # Calcula média geral
        mean_gray = (mean_b + mean_g + mean_r) / 3.0
        
        # Calcula fatores de correção
        if mean_b > 0 and mean_g > 0 and mean_r > 0:
            scale_b = mean_gray / mean_b
            scale_g = mean_gray / mean_g
            scale_r = mean_gray / mean_r
            
            # Aplica correção suave
            img_float[:,:,0] = img_float[:,:,0] * (1 + (scale_b - 1) * intensidade)
            img_float[:,:,1] = img_float[:,:,1] * (1 + (scale_g - 1) * intensidade)
            img_float[:,:,2] = img_float[:,:,2] * (1 + (scale_r - 1) * intensidade)
        
        return np.clip(img_float, 0, 255).astype(np.uint8)
    
    def processar_pasta(self, pasta_entrada: str = "fotos", 
                       pasta_saida: str = "fotos_melhoradas", 
                       intensidade: str = "medio",
                       auto_ajuste: bool = True) -> None:
        """Processa todas as imagens de uma pasta"""
        
        if not os.path.exists(pasta_entrada):
            print(f"❌ Pasta '{pasta_entrada}' não encontrada!")
            return
        
        os.makedirs(pasta_saida, exist_ok=True)
        
        extensoes = [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]
        arquivos_processados = 0
        
        print(f"🚀 Iniciando processamento com intensidade '{intensidade}'")
        print(f"📁 Pasta entrada: {pasta_entrada}")
        print(f"📁 Pasta saída: {pasta_saida}")
        print(f"🤖 Auto-ajuste: {'Ativado' if auto_ajuste else 'Desativado'}")
        print("-" * 50)
        
        for arquivo in sorted(os.listdir(pasta_entrada)):
            if any(arquivo.lower().endswith(ext) for ext in extensoes):
                entrada = os.path.join(pasta_entrada, arquivo)
                
                # Preserva nome original mas adiciona sufixo se necessário
                nome, ext = os.path.splitext(arquivo)
                if entrada == os.path.join(pasta_saida, arquivo):
                    nome_saida = f"{nome}_melhorada{ext}"
                else:
                    nome_saida = arquivo
                
                saida = os.path.join(pasta_saida, nome_saida)
                
                try:
                    if self.melhorar_foto_familia(entrada, saida, intensidade, auto_ajuste):
                        arquivos_processados += 1
                except Exception as e:
                    print(f"❌ Erro ao processar {arquivo}: {str(e)}")
        
        print("-" * 50)
        print(f"🎉 {arquivos_processados} fotos processadas e salvas em '{pasta_saida}'")
        
        if arquivos_processados == 0:
            print("💡 Dica: Verifique se há imagens válidas na pasta de entrada")

def main():
    """Função principal com interface melhorada"""
    melhorador = MelhoradorFotografico()
    
    # Parsing de argumentos
    intensidade = "medio"
    auto_ajuste = True
    pasta_entrada = "fotos"
    pasta_saida = "fotos_melhoradas"
    
    if len(sys.argv) > 1:
        intensidade = sys.argv[1].lower()
        if intensidade not in ["leve", "medio", "forte"]:
            print("❌ Intensidade deve ser: leve, medio ou forte")
            print("💡 Exemplo: python script.py medio")
            return
    
    if len(sys.argv) > 2:
        pasta_entrada = sys.argv[2]
    
    if len(sys.argv) > 3:
        pasta_saida = sys.argv[3]
    
    if len(sys.argv) > 4:
        auto_ajuste = sys.argv[4].lower() == "true"
    
    # Mostra ajuda se solicitado
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["-h", "--help", "help"]:
        print("📷 Sistema Avançado de Melhoria Fotográfica")
        print("=" * 50)
        print("Uso: python script.py [intensidade] [pasta_entrada] [pasta_saida] [auto_ajuste]")
        print()
        print("Parâmetros:")
        print("  intensidade:    leve, medio, forte (padrão: medio)")
        print("  pasta_entrada:  pasta com fotos originais (padrão: fotos)")
        print("  pasta_saida:    pasta para fotos melhoradas (padrão: fotos_melhoradas)")
        print("  auto_ajuste:    true/false - ajuste automático (padrão: true)")
        print()
        print("Melhorias aplicadas:")
        print("  ✓ Redução inteligente de ruído")
        print("  ✓ Correção de gamma adaptativa")
        print("  ✓ Melhoria de sombras e realces")
        print("  ✓ Vibrância com proteção de tons de pele")
        print("  ✓ Nitidez seletiva (apenas em bordas)")
        print("  ✓ Micro-contraste para definição")
        print("  ✓ Filtro cinematográfico sutil")
        print("  ✓ Análise automática de qualidade")
        print()
        print("Exemplos:")
        print("  python script.py")
        print("  python script.py forte")
        print("  python script.py medio minhas_fotos fotos_processadas")
        return
    
    # Executa o processamento
    try:
        melhorador.processar_pasta(pasta_entrada, pasta_saida, intensidade, auto_ajuste)
    except KeyboardInterrupt:
        print("\n⏹️ Processamento interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main()