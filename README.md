# Análise de Conteúdo Automatizada com PLN e IA

Este projeto implementa uma versão automatizada da técnica de Análise de Conteúdo de Laurence Bardin utilizando Processamento de Linguagem Natural (PLN) e Inteligência Artificial. A ferramenta auxilia pesquisadores na análise sistemática de conteúdo textual, seguindo as três fases principais propostas por Bardin: pré-análise, exploração do material e tratamento dos resultados/interpretação.

O uso da Inteligência Artificial é feito de forma local, isto é, o LLM (Large Language Model) é operado em uma máquina proprietária (localmente), garantindo o controle e a segurança dos dados analisados. 

## 🎯 Características Principais

- Implementação automatizada das três fases da Análise de Conteúdo de Bardin
- Processamento de textos em português utilizando spaCy
- Análise semântica avançada com modelos de IA
- Geração de visualizações e relatórios
- Configuração flexível via arquivo YAML
- Suporte a múltiplos formatos de entrada

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- spaCy (PLN)
- NLTK
- scikit-learn
- pandas
- numpy
- matplotlib
- wordcloud
- OpenAI API (opcional)

Nota: O modelo utilizado neste exemplo é o Gemma 3, o modelo de linguagem de código aberto do Google. A ferramenta utilizada para rodar o LLM localmente foi o [Ollama](https://ollama.com/).

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/joaomarcosmb/analise-de-conteudo
cd analise-de-conteudo
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Baixe o modelo do spaCy para português:
```bash
python -m spacy download pt_core_news_md
```

## ⚙️ Configuração

O arquivo `config.yaml` permite personalizar diversos aspectos da análise:

- Diretórios de entrada/saída
- Parâmetros de processamento de texto
- Configurações de visualização
- Ajustes dos algoritmos de PLN e IA

## 🔍 Como Usar

1. Coloque seus arquivos de texto para análise no diretório de entrada especificado em `config.yaml`

2. Execute o script principal:
```bash
python main.py
```

3. Os resultados serão gerados no diretório de saída configurado

## 📊 Estrutura do Projeto

```
.
├── data/               # Diretório para dados de entrada e saída
├── src/               # Código fonte do projeto
│   ├── pre_analysis/  # Implementação da fase de pré-análise
│   ├── exploration/   # Implementação da fase de exploração
│   ├── interpretation/# Implementação da fase de interpretação
│   └── utils/        # Utilitários e funções auxiliares
├── config.yaml        # Arquivo de configuração
├── main.py           # Script principal
└── requirements.txt  # Dependências do projeto
```

## 📝 Fases da Análise

### 1. Pré-análise
- Leitura flutuante automatizada
- Preparação do material
- Normalização do texto
- Tokenização e lematização
- Remoção de stopwords

### 2. Exploração do Material
- Identificação automática de unidades de registro
- Categorização assistida por IA
- Análise de frequência
- Extração de temas
- Geração de visualizações

### 3. Tratamento dos Resultados e Interpretação
- Análise estatística
- Geração de insights
- Visualização de resultados
- Exportação de relatórios

## 📈 Saídas

O sistema gera os seguintes tipos de análises e visualizações:

- Nuvens de palavras
- Boxplot da distribuição de relevância por tema
- Heatmap da distribuição de temas por documento
- Gráfico de barras dos temas mais relevantes
- Relatórios detalhados em formato estruturado

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests ou abrir issues para discutir melhorias.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 📚 Referência

- BARDIN, L. Análise de conteúdo. São Paulo: Edições 70, 2011.