from rdflib import Literal, RDFS
from model.rdf_utils import ONTO, DADOS, add_field_values, new_individual, local_id

QUESTION_SUFFIX = {
    "EPDS": "edimburgo",
    "PSQI": "pittsburgh",
    "OHIP14": "ohip14",
    "AUDIT": "audit",
    "FERGSTRON": "fergstron",
    "FAGERSTROM": "fergstron",
    "FAGER": "fergstron",
    "IPAQ": "ipaq",
}

class RespostaMapper:
    def __init__(self, dataframe, graph):
        self.df = dataframe
        self.graph = graph

    def map(self):
        for _, series in self.df.iterrows():
            row = series.to_dict()
            instrument = row["Instrumento"].strip().upper().replace("-", "").replace(" ", "")
            suffix = QUESTION_SUFFIX.get(instrument)
            if not suffix:
                raise ValueError(f"Instrumento não mapeado nas respostas: {row['Instrumento']!r}")
            question_local = f"pergunta{int(row['Numero_Pergunta']):02d}_{suffix}"
            question = ONTO[question_local]
            # Falha cedo se o identificador da pergunta não existir na ontologia de entrada.
            if (question, None, None) not in self.graph:
                raise ValueError(f"Pergunta não encontrada na ontologia: {question_local}")
            answer = new_individual(self.graph, row["Resposta_ID"], "Resposta")
            # Na ontologia, atende tem domínio Pergunta e alcance Resposta.
            self.graph.add((question, ONTO.atende, answer))
            self.graph.add((answer, RDFS.label, Literal(f"Resposta {row['Resposta_ID']}", lang="pt-BR")))
            # As relações de rastreabilidade com a aplicação e a gestante ficam em propriedades auxiliares,
            # pois o TTL fornecido não define propriedades específicas para esses dois vínculos da resposta.
            self.graph.add((answer, DADOS["pertenceAAplicacao"], ONTO[local_id(row["Aplicacao_ID"])]))
            self.graph.add((answer, DADOS["respondidaPorGestante"], ONTO[local_id(row["Gestante_ID"])]))
            add_field_values(self.graph, answer, row, excluded=("Resposta_ID",))
