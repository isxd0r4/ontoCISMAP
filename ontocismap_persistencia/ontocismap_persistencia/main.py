from pathlib import Path
from rdflib import Graph
from handlers.csv_handler import read_csv, FILES_DIR
from mappers.gestante_mapper import GestanteMapper
from mappers.aplicacao_mapper import AplicacaoMapper
from mappers.resposta_mapper import RespostaMapper

BASE_DIR = Path(__file__).resolve().parent
ONTOLOGY_FILE = FILES_DIR / "ontoCISMAPo.ttl"
OUTPUT_FILE = FILES_DIR / "output.ttl"

def main():
    print("1/5 - Lendo os arquivos CSV...")
    gestantes_df = read_csv("gestantes_nos.csv")
    aplicacoes_df = read_csv("aplicacoes_ontocismap.csv")
    respostas_df = read_csv("respostas_ontocismap.csv")
    print(f"Gestantes: {len(gestantes_df)} | aplicações: {len(aplicacoes_df)} | respostas: {len(respostas_df)}")

    print("2/5 - Carregando a ontologia operacional...")
    graph = Graph()
    graph.parse(str(ONTOLOGY_FILE), format="turtle")
    triples_before = len(graph)
    print(f"Triplas existentes na ontologia: {triples_before}")

    print("3/5 - Criando indivíduos de gestantes e aplicações...")
    GestanteMapper(gestantes_df, graph).map()
    AplicacaoMapper(aplicacoes_df, graph).map()

    print("4/5 - Criando indivíduos de respostas...")
    RespostaMapper(respostas_df, graph).map()

    print("5/5 - Salvando o grafo no formato TTL...")
    graph.serialize(destination=str(OUTPUT_FILE), format="turtle", encoding="utf-8")
    print(f"Arquivo gerado: {OUTPUT_FILE}")
    print(f"Triplas adicionadas: {len(graph) - triples_before}")
    print(f"Total de triplas no arquivo final: {len(graph)}")

if __name__ == "__main__":
    main()
