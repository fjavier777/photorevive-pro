# 📷 Sistema Avançado de Melhoria Fotográfica

Um sistema profissional de processamento de imagens para melhorar fotos de família com técnicas fotográficas avançadas e inteligência artificial.

## ✨ Funcionalidades

### 🎯 Melhorias Automáticas
- **Análise Inteligente de Qualidade** - Detecta problemas e ajusta automaticamente
- **Redução de Ruído Adaptativa** - Remove ruído preservando detalhes importantes
- **Correção de Exposição** - Gamma e realce de sombras/highlights com CLAHE
- **Vibrância Inteligente** - Intensifica cores protegendo tons de pele
- **Nitidez Seletiva** - Aplica nitidez apenas em bordas, evitando amplificar ruído
- **Micro-contraste** - Adiciona definição sem perder naturalidade
- **Filtro Cinematográfico** - Toque profissional com balanço de cores

### 🔧 Processamento Técnico
- **Correção de Gamma** para melhor exposição
- **CLAHE** (Contrast Limited Adaptive Histogram Equalization)
- **Filtro Bilateral** para redução inteligente de ruído
- **Processamento HSV/LAB** para ajustes precisos de cor
- **Detecção de Bordas** para nitidez seletiva
- **Análise de Histograma** para detecção automática de problemas

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/melhorador-fotografico.git
cd melhorador-fotografico

# Instale as dependências
pip install -r requirements.txt
```

### Instalação Manual
```bash
pip install opencv-python pillow numpy
```

## 📖 Como Usar

### Uso Básico
```bash
# Processa todas as imagens da pasta 'fotos'
python melhorador_fotografico.py

# Escolhe intensidade específica
python melhorador_fotografico.py medio
python melhorador_fotografico.py forte
python melhorador_fotografico.py leve
```

### Uso Avançado
```bash
# Pasta customizada
python melhorador_fotografico.py medio minhas_fotos resultado_final

# Desativar ajuste automático
python melhorador_fotografico.py medio fotos saida false

# Ver todas as opções
python melhorador_fotografico.py --help
```

### Estrutura de Pastas
```
projeto/
├── melhorador_fotografico.py
├── fotos/                    # Suas fotos originais
│   ├── foto1.jpg
│   ├── foto2.png
│   └── ...
└── fotos_melhoradas/        # Fotos processadas (criada automaticamente)
    ├── foto1.jpg
    ├── foto2.png
    └── ...
```

## ⚙️ Parâmetros de Intensidade

### 🟢 Leve
- Melhorias sutis e naturais
- Ideal para fotos já bem expostas
- Preserva ao máximo o aspecto original

### 🟡 Médio (Padrão)
- Equilíbrio entre melhoria e naturalidade
- Recomendado para a maioria das fotos
- Corrige problemas comuns automaticamente

### 🔴 Forte
- Melhorias mais agressivas
- Para fotos com problemas significativos
- Pode alterar mais o aspecto original

## 🎛️ Ajustes Automáticos

O sistema analisa automaticamente cada foto e detecta:

- **Borramento** - Aumenta nitidez quando necessário
- **Subexposição** - Melhora brilho e recupera sombras
- **Superexposição** - Reduz brilho e protege realces
- **Ruído Excessivo** - Aplica redução mais intensa
- **Contraste Baixo** - Aumenta contraste automaticamente

## 📊 Formatos Suportados

### Entrada
- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)
- BMP (.bmp)

### Saída
- JPEG com qualidade otimizada (95%)
- Compressão inteligente preservando qualidade

## 🔍 Análise de Qualidade

O sistema fornece informações detalhadas sobre cada foto:

```
📸 Processando IMG_001.jpg...
🔍 Qualidade detectada - Nitidez: 156.7, Ruído: 4.2
✅ IMG_001.jpg salvo com sucesso (medio)
```

### Métricas
- **Nitidez**: Variância Laplaciana (>100 = boa, <50 = borrada)
- **Ruído**: Desvio padrão do ruído estimado (<5 = limpa, >10 = ruidosa)

## 💡 Dicas de Uso

### Para Melhores Resultados
1. **Use fotos em alta resolução** - Mais detalhes = melhor processamento
2. **Organize por tipo** - Fotos similares em lotes separados
3. **Teste intensidades** - Comece com "medio" e ajuste conforme necessário
4. **Backup original** - Sempre mantenha as fotos originais

### Casos Específicos
- **Fotos antigas/escaneadas**: Use intensidade "forte"
- **Fotos do celular em boa luz**: Use intensidade "leve"
- **Fotos internas/com flash**: Use intensidade "medio"
- **Fotos com muito ruído**: Ative sempre o auto-ajuste

## 🏗️ Arquitetura Técnica

```python
MelhoradorFotografico
├── Análise de Qualidade
│   ├── detectar_qualidade_imagem()
│   └── ajustar_automatico()
├── Pré-processamento
│   ├── reduzir_ruido()
│   ├── corrigir_gamma()
│   └── melhorar_sombras_realces()
├── Ajustes Fotográficos
│   ├── ajustar_vibrancia()
│   ├── aplicar_filtro_cinematico()
│   └── aplicar_micro_contraste()
└── Pós-processamento
    ├── nitidez_seletiva()
    └── otimizacao_final()
```

## 🔬 Algoritmos Utilizados

### Redução de Ruído
- **Filtro Bilateral**: Preserva bordas enquanto suaviza ruído
- **Parâmetros Adaptativos**: Ajustados conforme nível de ruído detectado

### Melhoria de Contraste
- **CLAHE**: Equalização adaptativa limitada por contraste
- **Micro-contraste**: Filtros passa-alta sutis para definição

### Correção de Cor
- **Espaço LAB**: Separação de luminância e cromaticidade
- **Proteção de Tons de Pele**: Máscara HSV para preservar naturalidade

### Nitidez Inteligente
- **Detecção de Bordas Canny**: Identifica áreas com detalhes
- **Aplicação Seletiva**: Nitidez apenas onde é necessária

## 🐛 Solução de Problemas

### Erros Comuns

**"Não consegui abrir [arquivo]"**
- Verifique se o arquivo não está corrompido
- Confirme se o formato é suportado
- Teste com outro arquivo para isolar o problema

**"Pasta 'fotos' não encontrada"**
- Crie a pasta 'fotos' no mesmo diretório do script
- Ou especifique o caminho correto como parâmetro

**Resultado muito artificial**
- Use intensidade "leve" em vez de "forte"
- Desative o auto-ajuste com parâmetro "false"

**Processamento muito lento**
- Reduza a resolução das imagens se necessário
- Processe lotes menores por vez
- Considere usar uma máquina com mais RAM/CPU

### Log de Debugging

Para debug avançado, modifique o código para incluir mais logs:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribuindo

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Áreas para Contribuição
- **Novos algoritmos** de processamento de imagem
- **Melhorias de performance** e otimização
- **Interface gráfica** (GUI) com tkinter/PyQt
- **Suporte a mais formatos** (RAW, HEIC, etc.)
- **Processamento em lote** com paralelização
- **Análise mais avançada** de qualidade de imagem

## 📝 Changelog

### v2.0.0 (Atual)
- ✅ Sistema completo de análise automática
- ✅ Vibrância inteligente com proteção de tons de pele
- ✅ Nitidez seletiva baseada em detecção de bordas
- ✅ Filtro cinematográfico profissional
- ✅ Interface melhorada com feedback detalhado

### v1.0.0
- ✅ Processamento básico com PIL
- ✅ Ajustes de contraste, brilho, cor e nitidez
- ✅ Processamento em lote

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **OpenCV Community** - Pela excelente biblioteca de visão computacional
- **Pillow Team** - Pelo processamento de imagem em Python
- **NumPy Developers** - Pela computação científica eficiente

## 📞 Suporte

- **Issues**: Para bugs e solicitações de features
- **Discussões**: Para dúvidas gerais e ideias
- **Wiki**: Para documentação avançada e tutoriais

---

⭐ **Se este projeto foi útil, considere dar uma estrela!** ⭐

**Desenvolvido com ❤️ para preservar suas memórias fotográficas**