from rdflib import URIRef, Literal, RDFS
from model.rdf_utils import ONTO, DADOS, add_field_values, new_individual, local_id

INSTRUMENTOS = {
    "EPDS": ("AplicacaoDaEscalaDeEdimburgo", "participaDa_aplicacaoDaEscalaDeEdimburgo", "EscalaDeEdimburgo", "eReferenteA_escalaDeEdimburgo"),
    "PSQI": ("AplicacaoDaEscalaDePittsburgh", "participaDa_aplicacaoDaEscalaDePittsburgh", "EscalaDePittsburgh", "eReferenteA_escalaDePittsburgh"),
    "OHIP14": ("AplicacaoDaEscalaOHIP14", "participaDa_aplicacaoDaEscalaOhip", "EscalaOHIP14", "eReferenteA_escalaOhip14"),
    "AUDIT": ("AplicacaoDoQuestionarioAUDIT", "participaDa_aplicacaoDoQuestionarioAudit", "QuestionarioAUDIT", "eReferenteAo_questionarioAudit"),
    "FERGSTRON": ("AplicacaoDoTesteDeFergstron", "participaDa_aplicacaoDoTesteDeFergstron", "TesteDeFergstron", "eReferenteAo_testeDeFergstron"),
    "FAGERSTROM": ("AplicacaoDoTesteDeFergstron", "participaDa_aplicacaoDoTesteDeFergstron", "TesteDeFergstron", "eReferenteAo_testeDeFergstron"),
    "FAGER": ("AplicacaoDoTesteDeFergstron", "participaDa_aplicacaoDoTesteDeFergstron", "TesteDeFergstron", "eReferenteAo_testeDeFergstron"),
    "IPAQ": ("AplicacaoDoQuestionarioInternacionalDeAtividadeFisica", "participaDe_aplicacaoDoIpaq", "QuestionarioInternacionalDeAtividadeFisica", "eReferenteAo_ipaq"),
}

class AplicacaoMapper:
    def __init__(self, dataframe, graph):
        self.df = dataframe
        self.graph = graph

    def map(self):
        for _, series in self.df.iterrows():
            row = series.to_dict()
            instrument = row["Instrumento"].strip().upper().replace("-", "").replace(" ", "")
            if instrument not in INSTRUMENTOS:
                raise ValueError(f"Instrumento não mapeado: {row['Instrumento']!r}")
            class_name, gestante_prop, questionnaire_class, questionnaire_prop = INSTRUMENTOS[instrument]
            app = new_individual(self.graph, row["Aplicacao_ID"], class_name)
            gestante = ONTO[local_id(row["Gestante_ID"])]
            questionnaire = ONTO[questionnaire_class]
            # Relação nativa prevista na ontologia: Gestante participa da aplicação.
            self.graph.add((gestante, ONTO[gestante_prop], app))
            # Relação nativa entre a aplicação e o instrumento/questionário.
            self.graph.add((app, ONTO[questionnaire_prop], questionnaire))
            self.graph.add((app, RDFS.label, Literal(f"Aplicação {row['Aplicacao_ID']} - {row['Instrumento']}", lang="pt-BR")))
            add_field_values(self.graph, app, row, excluded=("Aplicacao_ID",))
