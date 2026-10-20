from model.rdf_utils import ONTO, add_field_values, new_individual

class GestanteMapper:
    def __init__(self, dataframe, graph):
        self.df = dataframe
        self.graph = graph

    def map(self):
        for _, series in self.df.iterrows():
            row = series.to_dict()
            gestante_id = row["Gestante_ID"]
            gestante = new_individual(self.graph, gestante_id, "Gestante")
            label = row.get("Gestante_Label") or gestante_id
            from rdflib import RDFS, Literal
            self.graph.add((gestante, RDFS.label, Literal(label, lang="pt-BR")))
            add_field_values(self.graph, gestante, row, excluded=("Gestante_ID", "Gestante_Label"))
