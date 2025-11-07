
import datetime, re

def validar_nome(nome):
    return isinstance(nome, str) and nome.strip() != '' and len(nome.strip()) >= 3

def validar_data_nascimento(data_str):
    if not isinstance(data_str, str): return False
    if not re.match(r'\d{2}/\d{2}/\d{4}$', data_str): return False
    try:
        d = datetime.datetime.strptime(data_str, '%d/%m/%Y').date()
        return d <= datetime.date.today()
    except:
        return False

def calcular_idade_por_data(data_str):
    d = datetime.datetime.strptime(data_str, '%d/%m/%Y').date()
    today = datetime.date.today()
    anos = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
    return anos

def validar_cpf(cpf):
    # validação apenas dígitos e tamanho 11
    if not isinstance(cpf, str): return False
    s = re.sub(r'[^0-9]', '', cpf)
    return len(s) == 11

def validar_email(email):
    if not isinstance(email, str): return False
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email) is not None

def validar_telefone(telefone):
    if not isinstance(telefone, str): return False
    s = re.sub(r'[^0-9]', '', telefone)
    return 8 <= len(s) <= 13

def validar_nota(valor):
    try:
        v = float(valor)
        return 0.0 <= v <= 10.0
    except:
        return False
