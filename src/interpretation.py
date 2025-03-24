import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from src.llm.llm_client import LLMClient
import os


class Interpretation:
    def __init__(self, categorized_data, config):
        self.categorized_data = categorized_data
        self.config = config
        self.llm = LLMClient(config.get('llm_endpoint'))

    def process(self):
        """Executa a etapa de interpretação e inferência"""
        print("Iniciando interpretação dos dados...")

        quant_analysis = self._quantitative_analysis()

        qual_analysis = self._qualitative_analysis()

        synthesis = self._synthesize_with_llm(quant_analysis, qual_analysis)

        visualizations = self._generate_visualizations()

        return {
            'quantitative_analysis': quant_analysis,
            'qualitative_analysis': qual_analysis,
            'synthesis': synthesis,
            'visualizations': visualizations
        }

    def _quantitative_analysis(self):
        """Realiza análise quantitativa dos dados categorizados"""
        theme_data = []

        for doc in self.categorized_data:
            for theme, score in doc['themes'].items():
                theme_data.append({
                    'document_id': doc['id'],
                    'theme': theme,
                    'relevance_score': score
                })

        df = pd.DataFrame(theme_data)

        # Análise por tema
        theme_summary = df.groupby('theme')['relevance_score'].agg(['mean', 'sum', 'count']).reset_index()
        theme_summary = theme_summary.sort_values('sum', ascending=False)

        # Análise por documento
        doc_summary = df.groupby('document_id')['relevance_score'].sum().reset_index()

        return {
            'theme_summary': theme_summary.to_dict('records'),
            'doc_summary': doc_summary.to_dict('records')
        }

    def _qualitative_analysis(self):
        """Realiza análise qualitativa dos dados categorizados"""
        insights = []

        for doc in self.categorized_data:
            doc_insights = doc['llm_analysis']
            insights.append({
                'document_id': doc['id'],
                'insights': doc_insights
            })

        return {
            'insights': insights
        }

    def _synthesize_with_llm(self, quant_analysis, qual_analysis):
        """Sintetiza os resultados usando o LLM"""
        # Preparar dados para o prompt
        top_themes = quant_analysis['theme_summary'][:5]

        prompt = f"""
        Com base na análise de conteúdo de entrevistas em português brasileiro, sintetize os principais resultados:

        Temas principais identificados:
        {', '.join([f"{theme['theme']} (relevância: {theme['sum']:.2f})" for theme in top_themes])}

        Alguns insights qualitativos das entrevistas:
        {qual_analysis['insights'][0]['insights'][:500]}...

        Por favor, forneça:
        1. Uma síntese dos principais achados
        2. Padrões ou tendências identificados
        3. Possíveis interpretações dos resultados
        4. Recomendações baseadas na análise

        Mantenha a síntese concisa e focada nos aspectos mais relevantes.
        """

        response = self.llm.generate(prompt=prompt)

        return response

    def _generate_visualizations(self):
        """Gera visualizações para os resultados"""
        visualization_paths = []
        
        # Ensure output directory exists
        os.makedirs('data/output', exist_ok=True)
        
        # Criar DataFrame com os dados dos temas
        theme_data = []
        for doc in self.categorized_data:
            for theme, score in doc['themes'].items():
                theme_data.append({
                    'theme': theme,
                    'relevance_score': score,
                    'document_id': doc['id']
                })
        df = pd.DataFrame(theme_data)
        
        # 1. Gráfico de barras dos temas mais relevantes
        plt.figure(figsize=(12, 6))
        theme_counts = df.groupby('theme')['relevance_score'].sum().sort_values(ascending=True)
        theme_counts.plot(kind='barh')
        plt.title('Relevância Total por Tema')
        plt.xlabel('Pontuação de Relevância')
        plt.ylabel('Temas')
        plt.tight_layout()
        bar_chart_path = 'data/output/theme_relevance_chart.png'
        plt.savefig(bar_chart_path)
        plt.close()
        visualization_paths.append(bar_chart_path)
        
        # 2. Nuvem de palavras baseada nos temas e suas relevâncias
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            prefer_horizontal=0.7
        )
        theme_scores = df.groupby('theme')['relevance_score'].sum().to_dict()
        wordcloud.generate_from_frequencies(theme_scores)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Nuvem de Palavras dos Temas')
        wordcloud_path = 'data/output/theme_wordcloud.png'
        plt.savefig(wordcloud_path)
        plt.close()
        visualization_paths.append(wordcloud_path)

        # 3. Heatmap da distribuição de temas por documento
        plt.figure(figsize=(12, 8))
        pivot_table = df.pivot_table(
            values='relevance_score',
            index='document_id',
            columns='theme',
            fill_value=0
        )
        plt.imshow(pivot_table, cmap='YlOrRd', aspect='auto')
        plt.colorbar(label='Relevância')
        plt.title('Distribuição de Temas por Documento')
        plt.xlabel('Temas')
        plt.ylabel('Documentos')
        plt.xticks(range(len(pivot_table.columns)), pivot_table.columns, rotation=45, ha='right')
        plt.tight_layout()
        heatmap_path = 'data/output/theme_distribution_heatmap.png'
        plt.savefig(heatmap_path)
        plt.close()
        visualization_paths.append(heatmap_path)

        # 4. Boxplot da distribuição de relevância por tema
        plt.figure(figsize=(12, 6))
        plt.boxplot([group['relevance_score'].values for name, group in df.groupby('theme')],
                   labels=df['theme'].unique())
        plt.xticks(rotation=45, ha='right')
        plt.title('Distribuição da Relevância por Tema')
        plt.ylabel('Pontuação de Relevância')
        plt.tight_layout()
        boxplot_path = 'data/output/theme_relevance_distribution.png'
        plt.savefig(boxplot_path)
        plt.close()
        visualization_paths.append(boxplot_path)
        
        return {
            'visualization_paths': visualization_paths
        }
