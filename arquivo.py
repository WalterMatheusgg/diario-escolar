from pathlib import Path
from banco import export_all_alunos, export_all_disciplinas, export_all_matriculas, export_all_notas
import csv

# Garantir que a pasta arquivos existe
BASE = Path(__file__).parent / 'arquivos'
BASE.mkdir(exist_ok=True)  # Cria a pasta se não existir

def export_to_csv(filename, headers, rows):
    p = BASE / filename
    with p.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
    return p

def export_alunos():
    rows = export_all_alunos()
    headers = ['matricula','nome','data_nascimento','cpf','email','telefone','endereco','serie','idade']
    return export_to_csv('alunos.csv', headers, rows)

def export_disciplinas():
    rows = export_all_disciplinas()
    headers = ['id','nome','professor','turno','sala','serie']
    return export_to_csv('disciplinas.csv', headers, rows)

def export_matriculas():
    rows = export_all_matriculas()
    headers = ['id','matricula','disciplina_id','disciplina_nome']
    return export_to_csv('matriculas.csv', headers, rows)

def export_notas():
    rows = export_all_notas()
    headers = ['id','matricula','disciplina_id','disciplina_nome','avaliacao','valor']
    return export_to_csv('notas.csv', headers, rows)