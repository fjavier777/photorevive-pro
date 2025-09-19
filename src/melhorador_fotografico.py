import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
from typing import Optional
import shutil

class MelhoradorFotografico:

    def __init__(self):
        """Inicializa a classe com as configurações de intensidade."""
        self.ajustes = {
            "leve": {"cor": 1.05, "contraste": 1.05, "brilho": 1.02, "nitidez": 1.05, "gamma": 1.0, "ruido": 0.3, "vibrancia": 1.03, "sombras": 0.05},
            "medio": {"cor": 1.15, "contraste": 1.1, "brilho": 1.05, "nitidez": 1.1, "gamma": 1.05, "ruido": 0.5, "vibrancia": 1.08, "sombras": 0.1},
            "forte": {"cor": 1.25, "contraste": 1.2, "brilho": 1.1, "nitidez": 1.2, "gamma": 1.1, "ruido": 0.7, "vibrancia": 1.15, "sombras": 0.15}
        }

    # --- NOVOS MÉTODOS DE PROCESSAMENTO POR ESTILO ---

    def _processar_estilo_vibrante(self, img: np.ndarray, config: dict) -> Image.Image:
        """Pipeline de processamento direto e de alto impacto (baseado no script simples)."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)

        pil_img = ImageEnhance.Color(pil_img).enhance(config["cor"])
        pil_img = ImageEnhance.Contrast(pil_img).enhance(config["contraste"])
        pil_img = ImageEnhance.Brightness(pil_img).enhance(config["brilho"])
        pil_img = ImageEnhance.Sharpness(pil_img).enhance(config["nitidez"])

        return pil_img

    def _processar_estilo_profissional(self, img: np.ndarray, config: dict) -> Image.Image:
        """Pipeline de processamento técnico e sutil (baseado no script avançado)."""
        img_denoised = self.reduzir_ruido(img, config["ruido"])
        img_gamma = self.corrigir_gamma(img_denoised, config["gamma"])
        img_sombras = self.melhorar_sombras_realces(img_gamma, config["sombras"])
        img_cinema = self.aplicar_filtro_cinematico(img_sombras, 0.2 if config["contraste"] > 1.1 else 0.1)

        img_rgb = cv2.cvtColor(img_cinema, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)

        if config["vibrancia"] != 1.0:
            pil_img = self.ajustar_vibrancia(pil_img, config["vibrancia"])

        pil_img = ImageEnhance.Contrast(pil_img).enhance(config["contraste"])
        pil_img = ImageEnhance.Brightness(pil_img).enhance(config["brilho"])

        if config["nitidez"] > 1.0:
            pil_img = self.aplicar_nitidez_seletiva(pil_img, config["nitidez"])

        pil_img = self.aplicar_micro_contraste(pil_img, 0.1 if config["contraste"] > 1.1 else 0.05)

        return pil_img

    # --- MÉTODO PRINCIPAL DE MELHORIA (DISPATCHER) ---

    def melhorar_foto_familia(self, caminho_imagem: str, salvar_como: str,
                            intensidade: str = "medio", auto_ajuste: bool = True,
                            estilo: str = 'profissional') -> bool:
        """Método principal que escolhe o pipeline de processamento correto."""
        if intensidade not in self.ajustes:
            raise ValueError("Intensidade inválida.")

        img = cv2.imread(caminho_imagem)
        if img is None:
            if "previews_temp" not in salvar_como: print(f"⚠️ Não consegui abrir {caminho_imagem}")
            return False

        is_preview = "previews_temp" in salvar_como
        if not is_preview: print(f"📸 Processando {os.path.basename(caminho_imagem)}...")

        config = self.ajustes[intensidade].copy()
        if auto_ajuste:
            qualidade = self.detectar_qualidade_imagem(img)
            config = self.ajustar_automatico(config, qualidade)
            if not is_preview: print(f"🔍 Qualidade detectada - Nitidez: {qualidade['nitidez']:.1f}, Ruído: {qualidade['ruido']:.1f}")

        if estilo == 'vibrante':
            pil_img_final = self._processar_estilo_vibrante(img, config)
        else: # Padrão é o profissional
            pil_img_final = self._processar_estilo_profissional(img, config)

        pil_img_final.save(salvar_como, quality=95, optimize=True)
        if not is_preview: print(f"✅ {os.path.basename(salvar_como)} salvo com sucesso (Estilo: {estilo.capitalize()}, Intensidade: {intensidade})")
        return True

    # --- MÉTODOS INTERATIVOS ATUALIZADOS ---

    def solicitar_estilo_ao_usuario(self, caminho_foto: str, pasta_saida: str) -> str:
        """Etapa 1: Gera previews dos dois estilos e pede para o usuário escolher."""
        print("\n--- ETAPA 1: ESCOLHA DO ESTILO DE MELHORIA ---")
        estilos = ["vibrante", "profissional"]
        pasta_previews = os.path.join(pasta_saida, "previews_temp")
        os.makedirs(pasta_previews, exist_ok=True)

        for estilo in estilos:
            nome_base, ext = os.path.splitext(os.path.basename(caminho_foto))
            caminho_preview = os.path.join(pasta_previews, f"{nome_base}_estilo_{estilo}{ext}")
            self.melhorar_foto_familia(caminho_foto, caminho_preview, "medio", auto_ajuste=False, estilo=estilo)

        # Exibição
        img_vibrante = cv2.imread(os.path.join(pasta_previews, f"{nome_base}_estilo_vibrante{ext}"))
        img_profissional = cv2.imread(os.path.join(pasta_previews, f"{nome_base}_estilo_profissional{ext}"))

        cv2.imshow("Estilo VIBRANTE (Cores Fortes)", self._redimensionar_para_preview(img_vibrante))
        cv2.imshow("Estilo PROFISSIONAL (Técnico e Sutil)", self._redimensionar_para_preview(img_profissional))

        print("✅ Duas janelas foram abertas para sua avaliação.")
        print("   -> Pressione qualquer tecla para fechar e continuar.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        while True:
            print("\n" + "="*50)
            print("Qual estilo de melhoria você prefere?")
            escolha = input("Digite o número (1-Vibrante, 2-Profissional) e pressione Enter: ")
            if escolha == "1": return "vibrante"
            elif escolha == "2": return "profissional"
            else: print("❌ Opção inválida.")

    def solicitar_intensidade_para_estilo(self, caminho_foto: str, pasta_saida: str, estilo: str) -> str:
        """Etapa 2: Gera previews de intensidade (L, M, F) para o estilo já escolhido."""
        print(f"\n--- ETAPA 2: ESCOLHA DA INTENSIDADE PARA O ESTILO '{estilo.upper()}' ---")
        intensidades = ["leve", "medio", "forte"]
        pasta_previews = os.path.join(pasta_saida, "previews_temp")

        for intensidade in intensidades:
            nome_base, ext = os.path.splitext(os.path.basename(caminho_foto))
            caminho_preview = os.path.join(pasta_previews, f"{nome_base}_{intensidade}{ext}")
            self.melhorar_foto_familia(caminho_foto, caminho_preview, intensidade, auto_ajuste=False, estilo=estilo)

        # Exibição
        for intensidade in intensidades:
            nome_base, ext = os.path.splitext(os.path.basename(caminho_foto))
            img = cv2.imread(os.path.join(pasta_previews, f"{nome_base}_{intensidade}{ext}"))
            cv2.imshow(f"Intensidade - {intensidade.upper()}", self._redimensionar_para_preview(img))

        print("✅ Três novas janelas foram abertas para sua avaliação.")
        print("   -> Pressione qualquer tecla para fechar e continuar.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        intensidade_escolhida = None
        while True:
            print("\n" + "="*50)
            print("Qual intensidade final você deseja aplicar?")
            escolha = input("Digite o número (1-Leve, 2-Medio, 3-Forte) e pressione Enter: ")
            if escolha == "1": intensidade_escolhida = "leve"; break
            elif escolha == "2": intensidade_escolhida = "medio"; break
            elif escolha == "3": intensidade_escolhida = "forte"; break
            else: print("❌ Opção inválida.")

        if os.path.exists(pasta_previews):
            try:
                shutil.rmtree(pasta_previews)
                print("✅ Pasta de previews temporária foi removida.")
            except Exception as e:
                print(f"⚠️ Não foi possível remover a pasta de previews: {e}")

        return intensidade_escolhida

    def processar_pasta(self, pasta_entrada: str = "fotos",
                       pasta_saida: str = "fotos_melhoradas",
                       intensidade: str = "medio",
                       auto_ajuste: bool = True,
                       modo_interativo: bool = False) -> None:
        """Orquestra todo o processo de melhoria."""
        if not os.path.exists(pasta_entrada):
            print(f"❌ Pasta '{pasta_entrada}' não encontrada!"); return
        os.makedirs(pasta_saida, exist_ok=True)

        intensidade_final = intensidade
        estilo_final = 'profissional' # Estilo padrão para modo não-interativo

        if modo_interativo:
            info_representativa = self.encontrar_foto_representativa(pasta_entrada)
            if info_representativa:
                caminho_representativo = info_representativa['caminho']
                estilo_final = self.solicitar_estilo_ao_usuario(caminho_representativo, pasta_saida)
                intensidade_final = self.solicitar_intensidade_para_estilo(caminho_representativo, pasta_saida, estilo_final)
                print(f"\n👍 Seleção final: Estilo '{estilo_final.upper()}' com intensidade '{intensidade_final.upper()}'")
            else:
                print("⚠️ Não foi possível iniciar o modo interativo.")

        extensoes = [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]
        arquivos_processados = 0
        print(f"\n🚀 Iniciando processamento em lote...")
        print(f"📁 Pasta entrada: {pasta_entrada}")
        print(f"📁 Pasta saída: {pasta_saida}")
        print("-" * 50)

        for arquivo in sorted(os.listdir(pasta_entrada)):
            if any(arquivo.lower().endswith(ext) for ext in extensoes):
                entrada = os.path.join(pasta_entrada, arquivo)
                saida = os.path.join(pasta_saida, arquivo)
                try:
                    self.melhorar_foto_familia(entrada, saida, intensidade_final, auto_ajuste, estilo_final)
                    arquivos_processados += 1
                except Exception as e:
                    print(f"❌ Erro ao processar {arquivo}: {str(e)}")

        print("-" * 50)
        print(f"🎉 {arquivos_processados} fotos processadas e salvas em '{pasta_saida}'")

    # --- MÉTODOS AUXILIARES ---
    # (Todos os outros métodos como `reduzir_ruido`, `corrigir_gamma`, etc. continuam aqui)

    def _redimensionar_para_preview(self, img, max_altura=800):
        if img is None: return None
        altura, largura, _ = img.shape
        if altura > max_altura:
            escala = max_altura / altura
            nova_largura = int(largura * escala)
            return cv2.resize(img, (nova_largura, max_altura))
        return img

    def _extrair_metricas_fotograficas(self, img: np.ndarray) -> dict:
        if img is None: return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return {"brilho": np.mean(gray), "contraste": np.std(gray), "saturacao": np.mean(hsv[:, :, 1]), "nitidez": cv2.Laplacian(gray, cv2.CV_64F).var(), "temp_cor": self.analisar_temperatura_cor(img)}

    def encontrar_foto_representativa(self, pasta_entrada: str) -> Optional[dict]:
        print("\n🔎 Analisando o lote para encontrar a foto mais representativa...")
        extensoes = [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]
        estatisticas_fotos = []
        arquivos = sorted(os.listdir(pasta_entrada))
        for arquivo in arquivos:
            if any(arquivo.lower().endswith(ext) for ext in extensoes):
                caminho_completo = os.path.join(pasta_entrada, arquivo)
                img = cv2.imread(caminho_completo)
                metricas = self._extrair_metricas_fotograficas(img)
                if metricas:
                    metricas["caminho"] = caminho_completo
                    estatisticas_fotos.append(metricas)
        if not estatisticas_fotos:
            print("⚠️ Nenhuma foto encontrada para análise.")
            return None
        metricas_chaves = list(estatisticas_fotos[0].keys())
        metricas_chaves.remove("caminho")
        media_geral = {chave: np.mean([d[chave] for d in estatisticas_fotos]) for chave in metricas_chaves}
        metricas_normalizadas = []
        for foto_stats in estatisticas_fotos:
            distancia_total = 0
            for chave in metricas_chaves:
                valor = foto_stats[chave]
                media = media_geral[chave]
                if media > 1e-6:
                    distancia_normalizada = ((valor - media) / media) ** 2
                    distancia_total += distancia_normalizada
            metricas_normalizadas.append({"caminho": foto_stats["caminho"], "distancia": np.sqrt(distancia_total)})
        foto_representativa = min(metricas_normalizadas, key=lambda x: x['distancia'])
        print(f"✅ Análise concluída. A foto mais representativa é: {os.path.basename(foto_representativa['caminho'])}")
        return foto_representativa

    def corrigir_gamma(self, img: np.ndarray, gamma: float) -> np.ndarray:
        if gamma == 1.0: return img
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
        return cv2.LUT(img, table)

    def reduzir_ruido(self, img: np.ndarray, intensidade: float) -> np.ndarray:
        if intensidade <= 0: return img
        d = int(5 + intensidade * 4)
        sigma_color = 50 + intensidade * 30
        sigma_space = 50 + intensidade * 30
        return cv2.bilateralFilter(img, d, sigma_color, sigma_space)

    def melhorar_sombras_realces(self, img: np.ndarray, intensidade: float) -> np.ndarray:
        if intensidade <= 0: return img
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=1.0 + intensidade * 2, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def ajustar_vibrancia(self, pil_img: Image.Image, vibrancia: float) -> Image.Image:
        if vibrancia == 1.0: return pil_img
        hsv = pil_img.convert('HSV')
        h, s, v = hsv.split()
        s_array = np.array(s, dtype=np.float32)
        h_array = np.array(h)
        tons_pele = ((h_array >= 5) & (h_array <= 25)) | ((h_array >= 160) & (h_array <= 180))
        fator_pele = 1.0 + (vibrancia - 1.0) * 0.3
        s_array[tons_pele] *= fator_pele
        s_array[~tons_pele] *= vibrancia
        s_array = np.clip(s_array, 0, 255).astype(np.uint8)
        s_nova = Image.fromarray(s_array)
        hsv_nova = Image.merge('HSV', (h, s_nova, v))
        return hsv_nova.convert('RGB')

    def aplicar_nitidez_seletiva(self, pil_img: Image.Image, fator: float) -> Image.Image:
        img_array = np.array(pil_img)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edges_dilated = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=1)
        mask = edges_dilated.astype(float) / 255.0
        img_sharp = ImageEnhance.Sharpness(pil_img).enhance(fator)
        img_sharp_array = np.array(img_sharp)
        for canal in range(3):
            img_array[:,:,canal] = (img_array[:,:,canal] * (1 - mask) + img_sharp_array[:,:,canal] * mask).astype(np.uint8)
        return Image.fromarray(img_array)

    def detectar_qualidade_imagem(self, img: np.ndarray) -> dict:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        pixels_escuros = np.sum(hist[0:50]) / img.size
        pixels_claros = np.sum(hist[200:256]) / img.size
        ruido = np.std(cv2.medianBlur(gray, 5) - gray)
        return {"nitidez": laplacian_var, "subexposta": pixels_escuros > 0.3, "superexposta": pixels_claros > 0.3, "ruido": ruido, "contraste_baixo": np.std(gray) < 40}

    def ajustar_automatico(self, config: dict, qualidade: dict) -> dict:
        config_auto = config.copy()
        if qualidade["nitidez"] < 100: config_auto["nitidez"] *= 1.2
        if qualidade["subexposta"]: config_auto["brilho"] *= 1.1; config_auto["sombras"] *= 1.5
        if qualidade["superexposta"]: config_auto["brilho"] *= 0.95
        if qualidade["ruido"] > 8: config_auto["nitidez"] *= 0.9; config_auto["ruido"] *= 1.3
        if qualidade["contraste_baixo"]: config_auto["contraste"] *= 1.15
        return config_auto

    def aplicar_filtro_cinematico(self, img: np.ndarray, intensidade: float = 0.3) -> np.ndarray:
        if intensidade <= 0: return img
        img_float = img.astype(np.float32) / 255.0
        img_float = np.power(img_float, 0.9)
        img_float = np.clip(img_float * 1.05, 0, 1)
        lab = cv2.cvtColor((img_float * 255).astype(np.uint8), cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l_norm, a, b = l.astype(np.float32) / 255.0, a.astype(np.float32), b.astype(np.float32)
        mascara_sombras = l_norm < 0.3
        a[mascara_sombras] += intensidade * 5; b[mascara_sombras] += intensidade * 3
        mascara_realces = l_norm > 0.7
        a[mascara_realces] -= intensidade * 2; b[mascara_realces] -= intensidade * 1
        a, b = np.clip(a, 0, 255).astype(np.uint8), np.clip(b, 0, 255).astype(np.uint8)
        lab_nova = cv2.merge([l, a, b])
        return cv2.cvtColor(lab_nova, cv2.COLOR_LAB2BGR)

    def aplicar_micro_contraste(self, pil_img: Image.Image, intensidade: float) -> Image.Image:
        if intensidade <= 0: return pil_img
        img_array = np.array(pil_img)
        img_float = img_array.astype(np.float32)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        img_details = cv2.filter2D(img_float, -1, kernel)
        img_final = cv2.addWeighted(img_float, 1 - intensidade, img_details, intensidade, 0)
        img_final = np.clip(img_final, 0, 255).astype(np.uint8)
        return Image.fromarray(img_final)

    def analisar_temperatura_cor(self, img: np.ndarray) -> float:
        r_mean, b_mean = np.mean(img[:,:,2]), np.mean(img[:,:,0])
        if r_mean > 1e-6: return b_mean / r_mean
        return 1.0
