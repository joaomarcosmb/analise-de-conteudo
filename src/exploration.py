from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.llm.llm_client import LLMClient


class ContentExploration:
    def __init__(self, corpus, config):
        self.corpus = corpus
        self.config = config
        self.llm = LLMClient(config.get("llm_endpoint"))

    def process(self):
        """Executa a etapa de exploração do material"""
        print("Iniciando exploração do material...")

        tfidf_matrix, feature_names = self._extract_features()

        themes = self._identify_themes(tfidf_matrix, feature_names)

        categorized_data = self._categorize_content(themes)

        return categorized_data

    def _extract_features(self):
        """Extrai características usando TF-IDF"""
        documents = [doc['clean_text'] for doc in self.corpus]

        # Criar vetorizador TF-IDF
        vectorizer = TfidfVectorizer(
            max_features=1000,
            min_df=1,
            max_df=1.0,
            stop_words=self.config.get("stop_words", [])
        )

        # Transformar documentos em matriz TF-IDF
        tfidf_matrix = vectorizer.fit_transform(documents)

        # Obter nomes das características
        feature_names = vectorizer.get_feature_names_out()

        return tfidf_matrix, feature_names

    def _identify_themes(self, tfidf_matrix, feature_names):
        """Identifica temas usando clustering"""
        num_clusters = self.config.get("num_clusters", 5)
        num_documents = len(self.corpus)

        if num_clusters > num_documents:
            raise ValueError(
                f"O número de clusters ({num_clusters}) não pode ser maior que o número de documentos ({num_documents}). "
                f"Por favor, ajuste o parâmetro 'num_clusters' no arquivo de configuração para um valor menor ou igual a {num_documents}."
            )

        # Aplicar K-means
        km = KMeans(n_clusters=num_clusters, random_state=42)
        km.fit(tfidf_matrix)

        # Obter os termos mais importantes para cada cluster
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]

        themes = []
        for i in range(num_clusters):
            theme_terms = [feature_names[ind] for ind in order_centroids[i, :10]]

            # Usar LLM para nomear o tema
            theme_name = self._name_theme_with_llm(theme_terms)

            themes.append({
                'id': i,
                'name': theme_name,
                'terms': theme_terms
            })

        return themes

    def _name_theme_with_llm(self, terms):
        """Usa o LLM para nomear um tema com base nos termos mais relevantes"""
        prompt = f"""
        Com base nos seguintes termos extraídos de entrevistas em português brasileiro:
        {', '.join(terms)}

        Sugira um nome conciso para este tema ou categoria que melhor represente estes termos.
        Responda apenas com o nome do tema, sem explicações adicionais.
        """

        response = self.llm.generate(prompt=prompt)
        theme_name = response.strip()

        return theme_name

    def _categorize_content(self, themes):
        """Categoriza o conteúdo em temas identificados"""
        categorized_data = []

        for doc in self.corpus:
            doc_themes = {}

            # Para cada tema, verificar relevância no documento
            for theme in themes:
                relevance_score = self._calculate_theme_relevance(doc, theme)
                doc_themes[theme['name']] = relevance_score

            # Usar LLM para análise mais profunda
            llm_analysis = self._analyze_with_llm(doc, themes)

            categorized_data.append({
                'id': doc['id'],
                'themes': doc_themes,
                'llm_analysis': llm_analysis
            })

        return categorized_data

    def _calculate_theme_relevance(self, doc, theme):
        """Calcula a relevância de um tema para um documento"""
        relevance = 0
        for term in theme['terms']:
            if term in doc['word_freq']:
                relevance += doc['word_freq'][term]

        return relevance

    def _analyze_with_llm(self, doc, themes):
        """Usa o LLM para análise mais profunda do documento"""
        theme_names = [theme['name'] for theme in themes]

        prompt = f"""
        Analise o seguinte trecho de entrevista em português brasileiro:

        "{doc['raw_text'][:1000]}..."

        Considerando os seguintes temas identificados: {', '.join(theme_names)}

        1. Quais temas estão presentes neste trecho?
        2. Quais são as principais opiniões ou percepções expressas pelo entrevistado?
        3. Identifique citações relevantes que exemplifiquem cada tema presente.

        Forneça uma análise concisa.
        """

        response = self.llm.generate(prompt=prompt)

        return response
