import tkinter as tk
from tkinter import ttk, messagebox
from banco import init_db, gerar_matricula_sequencial, adicionar_aluno, listar_alunos, obter_aluno, adicionar_disciplina, listar_disciplinas, obter_disciplina, matricular_aluno, listar_matriculas_por_aluno, listar_matriculados_na_disciplina, adicionar_nota, listar_notas_por_aluno, calcular_media_por_aluno_e_disciplina
from validacao import validar_nome, validar_data_nascimento, calcular_idade_por_data, validar_cpf, validar_email, validar_telefone, validar_nota
from arquivo import export_alunos, export_disciplinas, export_matriculas, export_notas

# Inicializar o banco de dados ANTES de criar a aplicação
init_db()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sistema de Gestão Escolar - Versão Realista (Atualizado)')
        self.geometry('1050x700')
        self.create_widgets()

    def create_widgets(self):
        tab = ttk.Notebook(self)
        tab.pack(fill='both', expand=True, padx=8, pady=8)

        self.frame_alunos = ttk.Frame(tab)
        tab.add(self.frame_alunos, text='Alunos')
        self._build_alunos(self.frame_alunos)
        
        self.frame_d = ttk.Frame(tab)
        tab.add(self.frame_d, text='Disciplinas')
        self._build_disciplinas(self.frame_d)
        
        self.frame_m = ttk.Frame(tab)
        tab.add(self.frame_m, text='Matrículas')
        self._build_matriculas(self.frame_m)
        
        self.frame_n = ttk.Frame(tab)
        tab.add(self.frame_n, text='Notas')
        self._build_notas(self.frame_n)
        
        self.frame_v = ttk.Frame(tab)
        tab.add(self.frame_v, text='Visualizar')
        self._build_visualizar(self.frame_v)

    # ---------------- Alunos ----------------
    def _build_alunos(self, parent):
        frm = ttk.Frame(parent, padding=10)
        frm.pack(fill='x')
        
        labels = ['Nome completo','Data nascimento (DD/MM/AAAA)','CPF','E-mail','Telefone','Endereço','Série/Turma','Responsável','Observações']
        vars = []
        self.aluno_vars = {}
        
        for i, lab in enumerate(labels):
            ttk.Label(frm, text=lab+':').grid(row=i, column=0, sticky='w', pady=2)
            v = tk.StringVar()
            if lab == 'Observações':
                ttk.Entry(frm, textvariable=v, width=80).grid(row=i, column=1, columnspan=3, sticky='w', padx=4)
            else:
                ttk.Entry(frm, textvariable=v, width=50).grid(row=i, column=1, sticky='w', padx=4)
            vars.append(v)
        
        # Mapear variáveis
        self.aluno_vars['nome'] = vars[0]
        self.aluno_vars['data'] = vars[1]
        self.aluno_vars['cpf'] = vars[2]
        self.aluno_vars['email'] = vars[3]
        self.aluno_vars['tel'] = vars[4]
        self.aluno_vars['end'] = vars[5]
        self.aluno_vars['serie'] = vars[6]
        self.aluno_vars['responsavel'] = vars[7]
        self.aluno_vars['obs'] = vars[8]
        
        ttk.Button(frm, text='Gerar matrícula', command=self.gerar_matricula).grid(row=0, column=4, padx=6)
        ttk.Button(frm, text='Salvar aluno', command=self.salvar_aluno).grid(row=9, column=1, sticky='w', pady=6)
        
        self.lbl_mat = ttk.Label(frm, text='Matrícula: -')
        self.lbl_mat.grid(row=0, column=5, padx=10)

    def gerar_matricula(self):
        m = gerar_matricula_sequencial()
        self.lbl_mat.config(text=f'Matrícula: {m}')

    def salvar_aluno(self):
        nome = self.aluno_vars['nome'].get().strip()
        data = self.aluno_vars['data'].get().strip()
        cpf = self.aluno_vars['cpf'].get().strip()
        email = self.aluno_vars['email'].get().strip()
        tel = self.aluno_vars['tel'].get().strip()
        end = self.aluno_vars['end'].get().strip()
        serie = self.aluno_vars['serie'].get().strip()
        responsavel = self.aluno_vars['responsavel'].get().strip()
        obs = self.aluno_vars['obs'].get().strip()
        
        if not validar_nome(nome):
            messagebox.showerror('Erro', 'Nome inválido.')
            return
        
        if not validar_data_nascimento(data):
            messagebox.showerror('Erro', 'Data de nascimento inválida.')
            return
        
        if not validar_cpf(cpf):
            messagebox.showerror('Erro', 'CPF inválido (apenas 11 dígitos).')
            return
        
        if not validar_email(email):
            messagebox.showerror('Erro', 'E-mail inválido.')
            return
        
        if not validar_telefone(tel):
            messagebox.showerror('Erro', 'Telefone inválido.')
            return
        
        idade = calcular_idade_por_data(data)
        matricula_text = self.lbl_mat.cget("text")
        
        # Extrair matrícula do texto do label
        if 'Matrícula: ' in matricula_text and matricula_text != 'Matrícula: -':
            matricula = matricula_text.replace('Matrícula: ', '')
        else:
            matricula = gerar_matricula_sequencial()
        
        try:
            # Concatenação endereço e observação
            endereco_completo = end
            if responsavel:
                endereco_completo += f' | Responsável: {responsavel}'
            if obs:
                endereco_completo += f' | Obs: {obs}'
                
            adicionar_aluno(matricula, nome, data, cpf, email, tel, endereco_completo, serie, idade)
            messagebox.showinfo('Sucesso', f'Aluno {nome} cadastrado com matrícula {matricula}.')
            
            for var in self.aluno_vars.values():
                var.set('')
            self.lbl_mat.config(text='Matrícula: -')
            self.atualizar_todos()
            
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao cadastrar aluno: {e}')

    # DIISSCIIPLINNAAA
    def _build_disciplinas(self, parent):
        frm = ttk.Frame(parent, padding=10)
        frm.pack(fill='x')
        
        ttk.Label(frm, text='Nome da disciplina:').grid(row=0, column=0, sticky='w')
        self.disc_nome = tk.StringVar()
        ttk.Entry(frm, textvariable=self.disc_nome, width=40).grid(row=0, column=1, sticky='w')
        
        ttk.Label(frm, text='Professor:').grid(row=1, column=0, sticky='w')
        self.disc_prof = tk.StringVar()
        ttk.Entry(frm, textvariable=self.disc_prof, width=30).grid(row=1, column=1, sticky='w')
        
        ttk.Label(frm, text='Turno:').grid(row=2, column=0, sticky='w')
        self.disc_turno = tk.StringVar()
        ttk.Combobox(frm, textvariable=self.disc_turno, values=['Manhã','Tarde','Noite'], state='readonly').grid(row=2, column=1, sticky='w')
        
        ttk.Label(frm, text='Sala:').grid(row=3, column=0, sticky='w')
        self.disc_sala = tk.StringVar()
        ttk.Entry(frm, textvariable=self.disc_sala, width=10).grid(row=3, column=1, sticky='w')
        
        ttk.Label(frm, text='Série/Turma:').grid(row=4, column=0, sticky='w')
        self.disc_serie = tk.StringVar()
        ttk.Entry(frm, textvariable=self.disc_serie, width=20).grid(row=4, column=1, sticky='w')
        
        ttk.Button(frm, text='Salvar disciplina', command=self.salvar_disciplina).grid(row=5, column=1, pady=6, sticky='w')

    def salvar_disciplina(self):
        nome = self.disc_nome.get().strip()
        prof = self.disc_prof.get().strip()
        turno = self.disc_turno.get().strip()
        sala = self.disc_sala.get().strip()
        serie = self.disc_serie.get().strip()
        
        if not nome or not prof or not turno or not sala or not serie:
            messagebox.showerror('Erro', 'Todos os campos são obrigatórios.')
            return
        
        try:
            adicionar_disciplina(nome, prof, turno, sala, serie)
            messagebox.showinfo('Sucesso', f'Disciplina {nome} adicionada.')
            
            self.disc_nome.set('')
            self.disc_prof.set('')
            self.disc_turno.set('')
            self.disc_sala.set('')
            self.disc_serie.set('')
            self.atualizar_todos()
            
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao adicionar disciplina: {e}')

    # ---------------- Matrículas ----------------
    def _build_matriculas(self, parent):
        frm = ttk.Frame(parent, padding=10)
        frm.pack(fill='x')
        
        ttk.Label(frm, text='Aluno (matrícula):').grid(row=0, column=0, sticky='w')
        self.cb_matriculas_m = ttk.Combobox(frm, values=[m for m, *_ in listar_alunos()], state='readonly', width=25)
        self.cb_matriculas_m.grid(row=0, column=1, sticky='w')
        self.cb_matriculas_m.bind('<<ComboboxSelected>>', self._filtrar_disciplinas_por_serie)
        
        self.lbl_nome_m = ttk.Label(frm, text='')
        self.lbl_nome_m.grid(row=0, column=2, sticky='w', padx=8)
        
        ttk.Label(frm, text='Disciplina:').grid(row=1, column=0, sticky='w')
        self.cb_disciplinas_m = ttk.Combobox(frm, values=[f"{d[0]} - {d[1]}" for d in listar_disciplinas()], state='readonly', width=60)
        self.cb_disciplinas_m.grid(row=1, column=1, columnspan=3, sticky='w')
        
        ttk.Button(frm, text='Matricular', command=self.matricular).grid(row=2, column=1, sticky='w', pady=6)
        ttk.Button(frm, text='Ver matrículas do aluno', command=self.ver_matriculas_aluno).grid(row=3, column=1, sticky='w', pady=6)
        
        self.lst_matriculas = tk.Listbox(parent, height=8)
        self.lst_matriculas.pack(fill='both', padx=10, pady=6, expand=False)

    def _filtrar_disciplinas_por_serie(self, event=None):
        mat = self.cb_matriculas_m.get().strip()
        if not mat:
            return
        
        aluno = obter_aluno(mat)
        if aluno:
            nome = aluno[1]
            serie = aluno[7]
            self.lbl_nome_m.config(text=f'Nome: {nome} | Série: {serie}')
            
            # Filtrar disciplinas por série
            all_disc = listar_disciplinas()
            vals = [f"{d[0]} - {d[1]}" for d in all_disc if (d[5] == serie or d[5] == '' or serie == '')]
            self.cb_disciplinas_m['values'] = vals
        else:
            self.lbl_nome_m.config(text='')

    def matricular(self):
        mat = self.cb_matriculas_m.get().strip()
        disc = self.cb_disciplinas_m.get().strip()
        
        if not mat or not disc:
            messagebox.showerror('Erro', 'Selecione aluno e disciplina.')
            return
        
        try:
            disciplina_id = int(disc.split(' - ')[0])
            matricular_aluno(mat, disciplina_id)
            messagebox.showinfo('Sucesso', 'Aluno matriculado.')
            self.atualizar_todos()
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao matricular: {e}')

    def ver_matriculas_aluno(self):
        self.lst_matriculas.delete(0, 'end')
        mat = self.cb_matriculas_m.get().strip()
        
        if not mat:
            messagebox.showerror('Erro', 'Selecione a matrícula.')
            return
        
        rows = listar_matriculas_por_aluno(mat)
        for r in rows:
            self.lst_matriculas.insert('end', f'ID:{r[0]} - Disciplina:{r[2]} (id:{r[1]})')

    # ---------------- Notas ----------------
    def _build_notas(self, parent):
        frm = ttk.Frame(parent, padding=10)
        frm.pack(fill='x')
        
        ttk.Label(frm, text='Aluno (matrícula):').grid(row=0, column=0, sticky='w')
        self.cb_matriculas_n = ttk.Combobox(frm, values=[m for m, *_ in listar_alunos()], state='readonly', width=25)
        self.cb_matriculas_n.grid(row=0, column=1, sticky='w')
        self.cb_matriculas_n.bind('<<ComboboxSelected>>', lambda e: self.carregar_disciplinas_do_aluno())
        
        self.lbl_nome_n = ttk.Label(frm, text='')
        self.lbl_nome_n.grid(row=0, column=2, sticky='w', padx=8)

        ttk.Label(frm, text='Disciplina (matriculado):').grid(row=1, column=0, sticky='w')
        self.cb_disciplinas_n = ttk.Combobox(frm, values=[], state='readonly', width=60)
        self.cb_disciplinas_n.grid(row=1, column=1, columnspan=2, sticky='w')
        
        ttk.Label(frm, text='Avaliação (ex: Prova 1):').grid(row=2, column=0, sticky='w')
        self.avaliacao_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.avaliacao_var, width=30).grid(row=2, column=1, sticky='w')
        
        ttk.Label(frm, text='Nota (0-10):').grid(row=3, column=0, sticky='w')
        self.nota_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.nota_var, width=10).grid(row=3, column=1, sticky='w')
        
        ttk.Button(frm, text='Salvar nota', command=self.salvar_nota).grid(row=4, column=1, sticky='w', pady=6)

    def carregar_disciplinas_do_aluno(self):
        mat = self.cb_matriculas_n.get().strip()
        if not mat: 
            self.cb_disciplinas_n['values'] = []
            self.lbl_nome_n.config(text='')
            return
        
        aluno = obter_aluno(mat)
        if aluno:
            self.lbl_nome_n.config(text=f'Nome: {aluno[1]} | Série: {aluno[7]}')
        
        rows = listar_matriculas_por_aluno(mat)
        vals = [f"{r[1]} - {r[2]}" for r in rows]
        self.cb_disciplinas_n['values'] = vals
        if vals:
            self.cb_disciplinas_n.set(vals[0])

    def salvar_nota(self):
        mat = self.cb_matriculas_n.get().strip()
        disc = self.cb_disciplinas_n.get().strip()
        ava = self.avaliacao_var.get().strip()
        nota = self.nota_var.get().strip()
        
        if not mat or not disc or not ava or nota == '':
            messagebox.showerror('Erro', 'Preencha todos os campos.')
            return
        
        if not validar_nota(nota):
            messagebox.showerror('Erro', 'Nota inválida.')
            return
        
        try:
            disciplina_id = int(disc.split(' - ')[0])
            adicionar_nota(mat, disciplina_id, ava, float(nota))
            messagebox.showinfo('Sucesso', 'Nota salva.')
            self.avaliacao_var.set('')
            self.nota_var.set('')
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao salvar nota: {e}')

    # ---------------- Visualizar ----------------
    def _build_visualizar(self, parent):
        frm = ttk.Frame(parent, padding=8)
        frm.pack(fill='both', expand=True)
        
        top = ttk.Frame(frm)
        top.pack(fill='x')
        
        ttk.Label(top, text='Filtrar por matrícula (opcional):').pack(side='left', padx=6)
        self.filtro_mat = tk.StringVar()
        ttk.Combobox(top, textvariable=self.filtro_mat, values=[m for m, *_ in listar_alunos()], width=20).pack(side='left')
        
        ttk.Button(top, text='Atualizar', command=self.atualizar_visualizacao).pack(side='left', padx=6)
        ttk.Button(top, text='Exportar CSVs', command=self.exportar_csvs).pack(side='left', padx=6)
        
        self.text_area = tk.Text(frm, wrap='word')
        self.text_area.pack(fill='both', expand=True, padx=6, pady=6)

    def atualizar_visualizacao(self):
        mat = self.filtro_mat.get().strip()
        self.text_area.delete('1.0', 'end')
        
        rows = listar_alunos() if not mat else [obter_aluno(mat)]
        
        for r in rows:
            if not r:
                continue
                
            matricula = r[0]
            endereco = r[6] if r[6] else ''
            
            self.text_area.insert('end', f"Matrícula: {r[0]}\nNome: {r[1]}\nData Nasc: {r[2]}\nCPF: {r[3]}\nE-mail: {r[4]}\nTelefone: {r[5]}\nEndereço / Obs: {endereco}\nSérie: {r[7]}\nIdade: {r[8]}\n")
            
            # Disciplinas matriculadas
            mats = listar_matriculas_por_aluno(matricula)
            self.text_area.insert('end', 'Disciplinas matriculadas:\n')
            
            for m in mats:
                did = m[1]
                nome_disc = m[2]
                media = calcular_media_por_aluno_e_disciplina(matricula, did)
                media_str = f"{media:.2f}" if media is not None else 'N/A'
                
                # Listar notas específicas
                notas = listar_notas_por_aluno(matricula)
                notas_disc = [f"{n[3]}: {n[4]}" for n in notas if n[1] == did]
                
                self.text_area.insert('end', f'  - {nome_disc} (id:{did}) | Média: {media_str}\n')
                if notas_disc:
                    self.text_area.insert('end', '    Notas: ' + ', '.join(notas_disc) + '\n')
            
            self.text_area.insert('end', '\n' + ('-'*80) + '\n\n')

    def exportar_csvs(self):
        a = export_alunos()
        d = export_disciplinas()
        m = export_matriculas()
        n = export_notas()
        messagebox.showinfo('Exportado', f'Arquivos exportados:\n{a}\n{d}\n{m}\n{n}')

    def atualizar_todos(self):
        vals = [m for m, *_ in listar_alunos()]
        
        # Atualizar comboboxes de matrículas
        try:
            self.cb_matriculas_m['values'] = vals
            self.cb_matriculas_n['values'] = vals
            self.filtro_mat['values'] = vals
        except:
            pass
        
        # Atualizar disciplinas
        try:
            self.cb_disciplinas_m['values'] = [f"{d[0]} - {d[1]}" for d in listar_disciplinas()]
        except:
            pass

if __name__ == '__main__':
    app = App()
    app.atualizar_todos()
    app.mainloop()