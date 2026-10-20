from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD
import re

ONTO = Namespace("http://example.org/OntoCISMAP#")
GUFO = Namespace("http://purl.org/nemo/gufo#")
# Namespace auxiliar para campos dos CSVs que ainda não possuem uma propriedade
# de dados correspondente explicitamente definida na ontologia operacional.
DADOS = Namespace("http://example.org/OntoCISMAP/dados#")

def local_id(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_-]", "_", str(value).strip())
    if not value:
        raise ValueError("Foi encontrado um identificador vazio.")
    return value

def add_field_values(graph: Graph, subject: URIRef, row: dict, excluded=()) -> None:
    """Preserva campos do CSV como propriedades auxiliares, sem inventar relações ontológicas."""
    for key, value in row.items():
        if key in excluded or value is None or str(value).strip() == "":
            continue
        predicate = DADOS[local_id(key)]
        text = str(value).strip()
        if key.lower() in {"idade", "idade_gestacional_semanas", "numero_gestacoes", "numero_partos", "numero_abortos", "preNatal_Consultas".lower(), "numero_pergunta"}:
            try:
                graph.add((subject, predicate, Literal(int(float(text)), datatype=XSD.integer)))
                continue
            except ValueError:
                pass
        graph.add((subject, predicate, Literal(text, lang="pt-BR")))

def new_individual(graph: Graph, identifier: str, class_name: str) -> URIRef:
    uri = ONTO[local_id(identifier)]
    graph.add((uri, RDF.type, OWL.NamedIndividual))
    graph.add((uri, RDF.type, ONTO[class_name]))
    # Mantém também o tipo gUFO compatível com o estereótipo da classe.
    if class_name == "Gestante":
        graph.add((uri, RDF.type, GUFO.FunctionalComplex))
    elif class_name.startswith("Aplicacao"):
        graph.add((uri, RDF.type, GUFO.Relator))
    elif class_name == "Resposta":
        graph.add((uri, RDF.type, GUFO.Quality))
    return uri
