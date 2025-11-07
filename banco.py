from pathlib import Path
import sqlite3
import os

# Garantir que a pasta database existe
DB_DIR = Path(__file__).parent / "database"
DB_DIR.mkdir(exist_ok=True)  # Cria a pasta se não existir
DB_PATH = DB_DIR / "escola_realista.db"

def get_conn():
    """Cria uma nova conexão com o banco"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except Exception as e:
        print(f"Erro ao conectar com o banco: {e}")
        raise

def init_db():
    """Inicializa o banco de dados"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            matricula TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            data_nascimento TEXT,
            cpf TEXT,
            email TEXT,
            telefone TEXT,
            endereco TEXT,
            serie TEXT,
            idade INTEGER
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            professor TEXT,
            turno TEXT,
            sala TEXT,
            serie TEXT
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS matriculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL,
            disciplina_id INTEGER NOT NULL,
            FOREIGN KEY(matricula) REFERENCES alunos(matricula) ON DELETE CASCADE,
            FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
            UNIQUE(matricula, disciplina_id)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL,
            disciplina_id INTEGER NOT NULL,
            avaliacao TEXT NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY(matricula) REFERENCES alunos(matricula) ON DELETE CASCADE,
            FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
            UNIQUE(matricula, disciplina_id, avaliacao)
        );
        """)
        conn.commit()
        print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
    finally:
        conn.close()

def gerar_matricula_sequencial():
    """Gera matrícula automaticamente"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT matricula FROM alunos ORDER BY matricula DESC LIMIT 1")
        row = cur.fetchone()
        if not row:
            return '20250001'
        try:
            last = int(row[0])
            return str(last + 1)
        except:
            return '20250001'
    finally:
        conn.close()

# Alunos
def adicionar_aluno(matricula, nome, data_nasc, cpf, email, telefone, endereco, serie, idade):
    """Adiciona um novo aluno"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO alunos(matricula, nome, data_nascimento, cpf, email, telefone, endereco, serie, idade) VALUES(?,?,?,?,?,?,?,?,?)",
                    (matricula, nome, data_nasc, cpf, email, telefone, endereco, serie, idade))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Matrícula {matricula} já existe!")
        return False
    except Exception as e:
        print(f"Erro ao adicionar aluno: {e}")
        return False
    finally:
        conn.close()

def listar_alunos():
    """Lista todos os alunos"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT matricula, nome, data_nascimento, cpf, email, telefone, endereco, serie, idade FROM alunos ORDER BY nome")
        return cur.fetchall()
    finally:
        conn.close()

def obter_aluno(matricula):
    """Obtém um aluno específico"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT matricula, nome, data_nascimento, cpf, email, telefone, endereco, serie, idade FROM alunos WHERE matricula = ?", (matricula,))
        return cur.fetchone()
    finally:
        conn.close()

# Disciplinas
def adicionar_disciplina(nome, professor, turno, sala, serie):
    """Adiciona uma nova disciplina"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO disciplinas(nome, professor, turno, sala, serie) VALUES(?,?,?,?,?)", 
                    (nome, professor, turno, sala, serie))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao adicionar disciplina: {e}")
        return False
    finally:
        conn.close()

def listar_disciplinas():
    """Lista todas as disciplinas"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, nome, professor, turno, sala, serie FROM disciplinas ORDER BY nome")
        return cur.fetchall()
    finally:
        conn.close()

def obter_disciplina(did):
    """Obtém uma disciplina específica"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, nome, professor, turno, sala, serie FROM disciplinas WHERE id = ?", (did,))
        return cur.fetchone()
    finally:
        conn.close()

# Matrículas
def matricular_aluno(matricula, disciplina_id):
    """Matricula um aluno em uma disciplina"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO matriculas(matricula, disciplina_id) VALUES(?,?)", 
                    (matricula, disciplina_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("Aluno já matriculado nesta disciplina!")
        return False
    except Exception as e:
        print(f"Erro ao matricular aluno: {e}")
        return False
    finally:
        conn.close()

def listar_matriculas_por_aluno(matricula):
    """Lista matrículas de um aluno"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT m.id, m.disciplina_id, d.nome FROM matriculas m
                       JOIN disciplinas d ON d.id = m.disciplina_id WHERE m.matricula = ?""", 
                    (matricula,))
        return cur.fetchall()
    finally:
        conn.close()

def listar_matriculados_na_disciplina(disciplina_id):
    """Lista alunos matriculados em uma disciplina"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT m.id, m.matricula, a.nome FROM matriculas m
                       JOIN alunos a ON a.matricula = m.matricula WHERE m.disciplina_id = ?""", 
                    (disciplina_id,))
        return cur.fetchall()
    finally:
        conn.close()

# Notas
def adicionar_nota(matricula, disciplina_id, avaliacao, valor):
    """Adiciona uma nota"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO notas(matricula, disciplina_id, avaliacao, valor) VALUES(?,?,?,?)", 
                    (matricula, disciplina_id, avaliacao, valor))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("Nota já cadastrada para esta avaliação!")
        return False
    except Exception as e:
        print(f"Erro ao adicionar nota: {e}")
        return False
    finally:
        conn.close()

def listar_notas_por_aluno(matricula):
    """Lista notas de um aluno"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT n.id, n.disciplina_id, d.nome, n.avaliacao, n.valor FROM notas n
                       JOIN disciplinas d ON d.id = n.disciplina_id WHERE n.matricula = ? ORDER BY d.nome""", 
                    (matricula,))
        return cur.fetchall()
    finally:
        conn.close()

def listar_notas_por_aluno_e_disciplina(matricula, disciplina_id):
    """Lista notas de um aluno em uma disciplina específica"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT avaliacao, valor FROM notas WHERE matricula = ? AND disciplina_id = ?""", 
                    (matricula, disciplina_id))
        return cur.fetchall()
    finally:
        conn.close()

def calcular_media_por_aluno_e_disciplina(matricula, disciplina_id):
    """Calcula a média de um aluno em uma disciplina"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT AVG(valor) FROM notas WHERE matricula = ? AND disciplina_id = ?""", 
                    (matricula, disciplina_id))
        r = cur.fetchone()
        return r[0] if r else None
    finally:
        conn.close()

# Export helpers
def export_all_alunos():
    """Exporta todos os alunos"""
    return listar_alunos()

def export_all_disciplinas():
    """Exporta todas as disciplinas"""
    return listar_disciplinas()

def export_all_matriculas():
    """Exporta todas as matrículas"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT m.id, m.matricula, m.disciplina_id, d.nome FROM matriculas m 
                       JOIN disciplinas d ON d.id = m.disciplina_id""")
        return cur.fetchall()
    finally:
        conn.close()

def export_all_notas():
    """Exporta todas as notas"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT n.id, n.matricula, n.disciplina_id, d.nome, n.avaliacao, n.valor FROM notas n 
                       JOIN disciplinas d ON d.id = n.disciplina_id""")
        return cur.fetchall()
    finally:
        conn.close()