import yaml


class Config:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)

    def _load_config(self, config_path):
        """Carrega configurações do arquivo YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            print(f"Erro ao carregar configurações: {str(e)}")
            # Configurações padrão
            return {
                "input_dir": "data/input",
                "output_dir": "data/output",
                "llm_endpoint": "http://0.0.0.0:11434/v1",
                "num_clusters": 5,
                "stop_words": []
            }

    def get(self, key, default=None):
        """Obtém valor de configuração"""
        return self.config.get(key, default)
