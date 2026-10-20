# Persistência de dados simulados na OntoCISMAP

## Requisitos
- Python 3.10 ou superior recomendado
- Pacotes de `requirements.txt`

## Execução
Abra um terminal dentro da pasta `ontocismap_persistencia` e execute:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Instale dependências e execute:
```bash
pip install -r requirements.txt
python main.py
```

O resultado será salvo em `files/output.ttl`.

## Observação de modelagem
O código usa as classes e as propriedades nativas encontradas no TTL enviado para representar gestantes, aplicações, instrumentos e perguntas/respostas. Como o TTL fornecido não contém propriedades de dados para todos os campos tabulares (idade, município, renda etc.) nem propriedades específicas para vincular uma resposta à aplicação e à gestante, esses valores são preservados em um namespace auxiliar `http://example.org/OntoCISMAP/dados#`. Para uma versão final estritamente alinhada ao modelo ontológico, recomenda-se revisar essas propriedades auxiliares com a orientadora e incorporá-las formalmente à ontologia, ou mapear os campos às classes e relações existentes quando houver correspondência conceitual inequívoca.

Os identificadores das perguntas são derivados do padrão encontrado na ontologia: `pergunta01_edimburgo`, `pergunta01_pittsburgh`, `pergunta01_ohip14`, `pergunta01_audit`, `pergunta01_fergstron` e `pergunta01_ipaq`. Se uma linha usar um número de pergunta que não exista na ontologia, o programa interromperá a execução e indicará a pergunta ausente.
