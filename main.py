from src.pre_analysis import PreAnalysis
from src.exploration import ContentExploration
from src.interpretation import Interpretation
from src.utils.file_handler import FileHandler
from src.utils.config import Config


def main():
    config = Config("config.yaml")

    file_handler = FileHandler(config.get("input_dir"), config.get("output_dir"))

    pre_analysis = PreAnalysis(file_handler, config)
    corpus = pre_analysis.process()

    exploration = ContentExploration(corpus, config)
    categorized_data = exploration.process()

    interpretation = Interpretation(categorized_data, config)
    results = interpretation.process()

    file_handler.save_results(results)

    print("Análise de conteúdo concluída com sucesso!")


if __name__ == "__main__":
    main()
