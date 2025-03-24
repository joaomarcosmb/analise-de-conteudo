import os
import json
from pathlib import Path


class FileHandler:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        # Criar diretório de saída se não existir
        os.makedirs(self.output_dir, exist_ok=True)

    def load_documents(self):
        """Carrega documentos do diretório de entrada"""
        documents = {}

        for file_path in Path(self.input_dir).glob('*.txt'):
            doc_id = file_path.stem
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            documents[doc_id] = content

        print(f"Carregados {len(documents)} documentos.")
        return documents

    def save_results(self, results):
        """Salva os resultados da análise"""
        # Salvar resultados em JSON
        results_path = os.path.join(self.output_dir, 'results.json')
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # Salvar síntese em texto
        synthesis_path = os.path.join(self.output_dir, 'synthesis.txt')
        with open(synthesis_path, 'w', encoding='utf-8') as f:
            f.write(results['synthesis'])

        print(f"Resultados salvos em {self.output_dir}")
