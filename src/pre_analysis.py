import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import spacy


class PreAnalysis:
    def __init__(self, file_handler, config):
        self.file_handler = file_handler
        self.config = config

        nltk.download('stopwords')
        nltk.download('punkt_tab')
        nltk.download('punkt')
        self.stop_words = set(stopwords.words('portuguese'))

        self.nlp = spacy.load('pt_core_news_md')

    def process(self):
        """Etapa de pré-análise"""
        print('Inicianto pré-análise')

        documents = self.file_handler.load_documents()

        corpus = self._prepare_corpus(documents)

        corpus = self._initial_analysis(corpus)

        return corpus

    def _prepare_corpus(self, documents):
        """Prepara o corpus para análise"""
        corpus = []

        for doc_id, content in documents.items():
            clean_text = self._clean_text(content)

            sentences = sent_tokenize(clean_text)

            # Análise linguística básica
            doc_analysis = self.nlp(clean_text)

            corpus.append({
                'id': doc_id,
                'raw_text': content,
                'clean_text': clean_text,
                'sentences': sentences,
                'doc_analysis': doc_analysis
            })

        return corpus

    def _clean_text(self, text):
        """Limpa o texto removendo caracteres indesejados"""
        # Remover caracteres especiais
        text = re.sub(r'[^\w\s]', ' ', text)

        # Remover espaços extras
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def _initial_analysis(self, corpus):
        """Realiza análise inicial do corpus"""
        for doc in corpus:
            words = word_tokenize(doc['clean_text'].lower())
            filtered_words = [w for w in words if w not in self.stop_words]

            # Calcular frequência
            word_freq = {}
            for word in filtered_words:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1

            doc['word_freq'] = word_freq

            # Identificar entidades nomeadas
            doc['entities'] = [(ent.text, ent.label_) for ent in doc['doc_analysis'].ents]

        return corpus
