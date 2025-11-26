# sistema_escolar_boletins.py
import json
import os
import hashlib
import getpass
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# =========== ARQUIVOS JSON ===========
ARQ_PROF = "professores.json"
ARQ_ALUN = "alunos.json"
ARQ_TURM = "turmas.json"
ARQ_ATIV = "atividades.json"

# =========== DADOS EM MEMÓRIA ===========
professores = []
alunos = []
turmas = []
atividades = []
usuario_logado = None

# =========== UTILITÁRIOS ===========
def carregar_arquivo(nome, default=[]):
    if os.path.exists(nome):
        with open(nome, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return default
    return default

def salvar_arquivo(nome, dados):
    with open(nome, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def salvar_tudo():
    salvar_arquivo(ARQ_PROF, professores)
    salvar_arquivo(ARQ_ALUN, alunos)
    salvar_arquivo(ARQ_TURM, turmas)
    salvar_arquivo(ARQ_ATIV, atividades)

def carregar_tudo():
    global professores, alunos, turmas, atividades
    professores = carregar_arquivo(ARQ_PROF, [])
    alunos = carregar_arquivo(ARQ_ALUN, [])
    turmas = carregar_arquivo(ARQ_TURM, [])
    atividades = carregar_arquivo(ARQ_ATIV, [])
    # garante que arquivos existam (cria se faltarem)
    salvar_tudo()

def prox_id(lista):
    return max((x.get("id", 0) for x in lista), default=0) + 1

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def input_int(prompt, min_val=None, max_val=None, allow_empty=False):
    while True:
        v = input(prompt).strip()
        if allow_empty and v == "":
            return None
        if not v.isdigit():
            print("Digite um número válido.")
            continue
        n = int(v)
        if min_val is not None and n < min_val:
            print(f"Valor mínimo: {min_val}")
            continue
        if max_val is not None and n > max_val:
            print(f"Valor máximo: {max_val}")
            continue
        return n

def input_float(prompt, min_val=None, max_val=None, allow_empty=False):
    while True:
        v = input(prompt).strip()
        if allow_empty and v == "":
            return None
        try:
            f = float(v.replace(",", "."))
        except:
            print("Digite um número válido (use . ou ,).")
            continue
        if min_val is not None and f < min_val:
            print(f"Valor mínimo: {min_val}")
            continue
        if max_val is not None and f > max_val:
            print(f"Valor máximo: {max_val}")
            continue
        return f

def confirma(prompt="Confirmar? (s/n): "):
    r = input(prompt).strip().lower()
    return r in ("s", "y")

# =========== BUSCAS ===========
def buscar_professor_por_id(pid):
    return next((p for p in professores if p["id"] == pid), None)

def buscar_aluno_por_id(aid):
    return next((a for a in alunos if a["id"] == aid), None)

def buscar_turma_por_id(tid):
    return next((t for t in turmas if t["id"] == tid), None)

def buscar_atividade_por_id(aid):
    return next((a for a in atividades if a["id"] == aid), None)

# =========== MÓDULO PROFESSORES ===========
def listar_professores():
    print("\n=== PROFESSORES ===")
    if not professores:
        print("Nenhum professor cadastrado.")
        return
    for p in professores:
        print(f"{p['id']} - {p['nome']} (Matrícula: {p['matricula']})")

def cadastrar_professor():
    print("\n=== CADASTRAR PROFESSOR ===")
    nome = input("Nome: ").strip()
    matricula = input("Matrícula: ").strip()
    senha = getpass.getpass("Senha: ")
    if any(p["matricula"].lower() == matricula.lower() for p in professores):
        print("❌ Matrícula já cadastrada.")
        return
    pid = prox_id(professores)
    professores.append({"id": pid, "nome": nome, "matricula": matricula, "senha": hash_senha(senha)})
    salvar_arquivo(ARQ_PROF, professores)
    print("✅ Professor cadastrado.")

def editar_professor():
    listar_professores()
    if not professores: return
    pid = input_int("ID do professor para editar (0 para cancelar): ", min_val=0)
    if pid == 0: return
    p = buscar_professor_por_id(pid)
    if not p:
        print("❌ Professor não encontrado.")
        return
    print("Deixe em branco para manter o valor atual.")
    novo_nome = input(f"Nome ({p['nome']}): ").strip()
    nova_mat = input(f"Matrícula ({p['matricula']}): ").strip()
    trocar_senha = input("Alterar senha? (s/n): ").strip().lower()
    if novo_nome: p["nome"] = novo_nome
    if nova_mat: p["matricula"] = nova_mat
    if trocar_senha in ("s","y"):
        s = getpass.getpass("Nova senha: ")
        p["senha"] = hash_senha(s)
    salvar_arquivo(ARQ_PROF, professores)
    print("✅ Professor atualizado.")

def remover_professor():
    listar_professores()
    if not professores: return
    pid = input_int("ID do professor para remover (0 para cancelar): ", min_val=0)
    if pid == 0: return
    p = buscar_professor_por_id(pid)
    if not p:
        print("❌ Professor não encontrado.")
        return
    if confirma(f"Remover {p['nome']}? (s/n): "):
        professores.remove(p)
        salvar_arquivo(ARQ_PROF, professores)
        print("✅ Professor removido.")

# =========== MÓDULO ALUNOS ===========
def listar_alunos():
    print("\n=== ALUNOS ===")
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    for a in alunos:
        print(f"{a['id']} - {a['matricula']} - {a['nome']}")

def cadastrar_aluno():
    print("\n=== CADASTRAR ALUNO ===")
    nome = input("Nome: ").strip()
    matricula = input("Matrícula: ").strip()
    if any(x["matricula"].lower() == matricula.lower() for x in alunos):
        print("❌ Matrícula já cadastrada.")
        return
    aid = prox_id(alunos)
    alunos.append({"id": aid, "nome": nome, "matricula": matricula})
    salvar_arquivo(ARQ_ALUN, alunos)
    print("✅ Aluno cadastrado.")

def editar_aluno():
    listar_alunos()
    if not alunos: return
    aid = input_int("ID do aluno para editar (0 cancelar): ", min_val=0)
    if aid == 0: return
    a = buscar_aluno_por_id(aid)
    if not a:
        print("❌ Aluno não encontrado.")
        return
    novo_nome = input(f"Nome ({a['nome']}): ").strip()
    nova_mat = input(f"Matrícula ({a['matricula']}): ").strip()
    if novo_nome: a['nome'] = novo_nome
    if nova_mat: a['matricula'] = nova_mat
    salvar_arquivo(ARQ_ALUN, alunos)
    print("✅ Aluno atualizado.")

def remover_aluno():
    listar_alunos()
    if not alunos: return
    aid = input_int("ID do aluno para remover (0 cancelar): ", min_val=0)
    if aid == 0: return
    a = buscar_aluno_por_id(aid)
    if not a:
        print("❌ Aluno não encontrado.")
        return
    if confirma(f"Remover {a['nome']}? (s/n): "):
        # remover de turmas
        for t in turmas:
            if aid in t["alunos"]:
                t["alunos"].remove(aid)
        # remover notas nas atividades (chave como str)
        for atv in atividades:
            if str(aid) in atv.get("notas", {}):
                del atv["notas"][str(aid)]
        alunos.remove(a)
        salvar_tudo()
        print("✅ Aluno removido.")

def buscar_aluno():
    q = input("Digite nome ou matrícula para buscar: ").strip().lower()
    encontrados = [a for a in alunos if q in a["nome"].lower() or q in a["matricula"].lower()]
    if not encontrados:
        print("Nenhum aluno encontrado.")
        return
    for a in encontrados:
        print(f"{a['id']} - {a['matricula']} - {a['nome']}")

def ver_turmas_do_aluno():
    listar_alunos()
    if not alunos: return
    aid = input_int("ID do aluno para ver turmas (0 cancelar): ", min_val=0)
    if aid == 0: return
    a = buscar_aluno_por_id(aid)
    if not a:
        print("Aluno não encontrado.")
        return
    turmas_do_aluno = [t for t in turmas if aid in t["alunos"]]
    if not turmas_do_aluno:
        print("Aluno não está matriculado em nenhuma turma.")
        return
    print(f"Turmas de {a['nome']}:")
    for t in turmas_do_aluno:
        print(f"{t['id']} - {t['nome']}")

# =========== MÓDULO TURMAS ===========
def listar_turmas():
    print("\n=== TURMAS ===")
    if not turmas:
        print("Nenhuma turma cadastrada.")
        return
    for t in turmas:
        print(f"{t['id']} - {t['nome']} (alunos: {len(t['alunos'])}, atividades: {len(t.get('atividades',[]))})")

def cadastrar_turma():
    print("\n=== CADASTRAR TURMA ===")
    nome = input("Nome da turma: ").strip()
    tid = prox_id(turmas)
    turmas.append({"id": tid, "nome": nome, "alunos": [], "atividades": []})
    salvar_arquivo(ARQ_TURM, turmas)
    print("✅ Turma cadastrada.")

def editar_turma():
    listar_turmas()
    if not turmas: return
    tid = input_int("ID da turma para editar (0 cancelar): ", min_val=0)
    if tid == 0: return
    t = buscar_turma_por_id(tid)
    if not t:
        print("Turma não encontrada.")
        return
    novo_nome = input(f"Nome ({t['nome']}): ").strip()
    if novo_nome: t['nome'] = novo_nome
    salvar_arquivo(ARQ_TURM, turmas)
    print("✅ Turma atualizada.")

def remover_turma():
    listar_turmas()
    if not turmas: return
    tid = input_int("ID da turma para remover (0 cancelar): ", min_val=0)
    if tid == 0: return
    t = buscar_turma_por_id(tid)
    if not t:
        print("Turma não encontrada.")
        return
    if confirma(f"Remover turma {t['nome']} e todas as atividades associadas? (s/n): "):
        # remover atividades associadas
        atv_to_remove = [a for a in atividades if a["turma_id"] == tid]
        for a in atv_to_remove:
            atividades.remove(a)
        turmas.remove(t)
        salvar_tudo()
        print("✅ Turma e atividades removidas.")

def ver_alunos_da_turma():
    listar_turmas()
    if not turmas: return
    tid = input_int("ID da turma (0 cancelar): ", min_val=0)
    if tid == 0: return
    t = buscar_turma_por_id(tid)
    if not t:
        print("Turma não encontrada.")
        return
    if not t["alunos"]:
        print("Nenhum aluno matriculado nesta turma.")
        return
    print(f"Alunos da {t['nome']}:")
    for aid in t["alunos"]:
        a = buscar_aluno_por_id(aid)
        if a:
            print(f"{a['id']} - {a['matricula']} - {a['nome']}")

def ver_atividades_da_turma():
    listar_turmas()
    if not turmas: return
    tid = input_int("ID da turma (0 cancelar): ", min_val=0)
    if tid == 0: return
    t = buscar_turma_por_id(tid)
    if not t:
        print("Turma não encontrada.")
        return
    if not t.get("atividades"):
        print("Nenhuma atividade nesta turma.")
        return
    print(f"Atividades da {t['nome']}:")
    for aid in t["atividades"]:
        atv = buscar_atividade_por_id(aid)
        if atv:
            descricao = atv.get("descricao", "")
            print(f"{atv['id']} - {atv['nome']} - {descricao}")

def matricular_aluno_em_turma():
    listar_alunos()
    if not alunos: return
    aid = input_int("ID do aluno (0 cancelar): ", min_val=0)
    if aid == 0: return
    a = buscar_aluno_por_id(aid)
    if not a:
        print("Aluno não encontrado.")
        return
    listar_turmas()
    if not turmas: return
    tid = input_int("ID da turma (0 cancelar): ", min_val=0)
    if tid == 0: return
    t = buscar_turma_por_id(tid)
    if not t:
        print("Turma não encontrada.")
        return
    if aid in t["alunos"]:
        print("Aluno já matriculado.")
        return
    t["alunos"].append(aid)
    salvar_tudo()
    print("✅ Matriculado com sucesso.")

def desmatricular_aluno():
    listar_turmas()
    if not turmas: return
    tid = input_int("ID da turma (0 cancelar): ", min_val=0)
    if tid == 0: return
    t = buscar_turma_por_id(tid)
    if not t:
        print("Turma não encontrada.")
        return
    if not t["alunos"]:
        print("Nenhum aluno na turma.")
        return
    print("Alunos:")
    for aid in t["alunos"]:
        a = buscar_aluno_por_id(aid)
        if a:
            print(f"{a['id']} - {a['matricula']} - {a['nome']}")
    aid = input_int("ID do aluno para desmatricular (0 cancelar): ", min_val=0)
    if aid == 0: return
    if aid not in t["alunos"]:
        print("Aluno não está matriculado nessa turma.")
        return
    t["alunos"].remove(aid)
    # remover notas desse aluno nas atividades da turma
    for atv_id in list(t.get("atividades", [])):
        atv = buscar_atividade_por_id(atv_id)
        if atv and str(aid) in atv.get("notas", {}):
            del atv["notas"][str(aid)]
    salvar_tudo()
    print("✅ Desmatriculado.")

# =========== MÓDULO ATIVIDADES E NOTAS (com descrição) ===========
def listar_atividades():
    print("\n=== ATIVIDADES ===")
    if not atividades:
        print("Nenhuma atividade cadastrada.")
        return
    for a in atividades:
        t = buscar_turma_por_id(a["turma_id"])
        nome_t = t["nome"] if t else "N/D"
        descricao = a.get("descricao", "")
        print(f"{a['id']} - {a['nome']} (Turma: {nome_t}) - {descricao}")

def cadastrar_atividade():
    listar_turmas()
    if not turmas: return
    tid = input_int("ID da turma que receberá a atividade (0 cancelar): ", min_val=0)
    if tid == 0: return
    t = buscar_turma_por_id(tid)
    if not t:
        print("Turma não encontrada.")
        return
    nome = input("Nome da atividade: ").strip()
    descricao = input("Descrição (resumo): ").strip()
    aid = prox_id(atividades)
    atv = {"id": aid, "nome": nome, "descricao": descricao, "turma_id": tid, "notas": {}}
    atividades.append(atv)
    t.setdefault("atividades", []).append(aid)
    salvar_tudo()
    print("✅ Atividade cadastrada.")

def editar_atividade():
    listar_atividades()
    if not atividades: return
    aid = input_int("ID da atividade para editar (0 cancelar): ", min_val=0)
    if aid == 0: return
    atv = buscar_atividade_por_id(aid)
    if not atv:
        print("Atividade não encontrada.")
        return
    novo_nome = input(f"Nome ({atv['nome']}): ").strip()
    nova_descr = input(f"Descrição ({atv.get('descricao','')}): ").strip()
    if novo_nome: atv["nome"] = novo_nome
    if nova_descr: atv["descricao"] = nova_descr
    salvar_arquivo(ARQ_ATIV, atividades)
    print("✅ Atividade atualizada.")

def remover_atividade():
    listar_atividades()
    if not atividades: return
    aid = input_int("ID da atividade para remover (0 cancelar): ", min_val=0)
    if aid == 0: return
    atv = buscar_atividade_por_id(aid)
    if not atv:
        print("Atividade não encontrada.")
        return
    if confirma(f"Remover atividade '{atv['nome']}'? (s/n): "):
        # remover referência da turma
        t = buscar_turma_por_id(atv["turma_id"])
        if t and aid in t.get("atividades", []):
            t["atividades"].remove(aid)
        atividades.remove(atv)
        salvar_tudo()
        print("✅ Atividade removida.")

def ver_notas_atividade():
    listar_atividades()
    if not atividades: return
    aid = input_int("ID da atividade (0 cancelar): ", min_val=0)
    if aid == 0: return
    atv = buscar_atividade_por_id(aid)
    if not atv:
        print("Atividade não encontrada.")
        return
    print(f"Notas da atividade {atv['nome']}:")
    if not atv.get("notas"):
        print("Sem notas registradas.")
        return
    for sid, nota in atv["notas"].items():
        aluno = buscar_aluno_por_id(int(sid))
        nome = aluno["nome"] if aluno else sid
        print(f"{sid} - {nome} : {nota}")

def adicionar_editar_nota():
    listar_atividades()
    if not atividades: return
    aid = input_int("ID da atividade (0 cancelar): ", min_val=0)
    if aid == 0: return
    atv = buscar_atividade_por_id(aid)
    if not atv:
        print("Atividade não encontrada.")
        return
    t = buscar_turma_por_id(atv["turma_id"])
    if not t:
        print("Turma da atividade não encontrada.")
        return
    if not t["alunos"]:
        print("Nenhum aluno matriculado na turma.")
        return
    print("Alunos da turma:")
    for aid_al in t["alunos"]:
        a = buscar_aluno_por_id(aid_al)
        if a:
            atual = atv["notas"].get(str(aid_al), "—")
            print(f"{a['id']} - {a['matricula']} - {a['nome']} (nota atual: {atual})")
    aluno_id = input_int("ID do aluno para lançar/editar nota (0 cancelar): ", min_val=0)
    if aluno_id == 0: return
    if aluno_id not in t["alunos"]:
        print("Aluno não pertence a esta turma.")
        return
    nota = input_float("Nota (0-10): ", min_val=0.0, max_val=10.0)
    atv["notas"][str(aluno_id)] = nota
    salvar_tudo()
    print("✅ Nota registrada/atualizada.")

def remover_nota():
    listar_atividades()
    if not atividades: return
    aid = input_int("ID da atividade (0 cancelar): ", min_val=0)
    if aid == 0: return
    atv = buscar_atividade_por_id(aid)
    if not atv:
        print("Atividade não encontrada.")
        return
    ver_notas_atividade()
    aluno_id = input("Digite o ID do aluno para remover nota (ou vazio para cancelar): ").strip()
    if aluno_id == "": return
    if aluno_id in atv.get("notas", {}):
        if confirma("Remover nota? (s/n): "):
            del atv["notas"][aluno_id]
            salvar_arquivo(ARQ_ATIV, atividades)
            print("✅ Nota removida.")
    else:
        print("Nenhuma nota encontrada para esse aluno nesta atividade.")

# =========== RELATÓRIOS ===========

def gerar_relatorio_texto():
    listar_turmas()
    if not turmas: return
    tid = input_int("ID da turma para relatório (0 cancelar): ", min_val=0)
    if tid == 0: return
    t = buscar_turma_por_id(tid)
    if not t:
        print("Turma não encontrada.")
        return
    print(f"\nRelatório da Turma {t['nome']}")
    if not t["alunos"]:
        print("Sem alunos matriculados.")
        return
    for aid in t["alunos"]:
        a = buscar_aluno_por_id(aid)
        notas = []
        for atv_id in t.get("atividades", []):
            atv = buscar_atividade_por_id(atv_id)
            if atv and str(aid) in atv.get("notas", {}):
                notas.append(f"{atv['nome']}: {atv['notas'][str(aid)]}")
        print(f"{a['matricula']} - {a['nome']} -> {' | '.join(notas) if notas else 'Sem notas'}")

def gerar_relatorios_pdf_turma():
    listar_turmas()
    if not turmas: return
    tid = input_int("ID da turma para gerar PDF (0 cancelar): ", min_val=0)
    if tid == 0: return
    t = buscar_turma_por_id(tid)
    if not t:
        print("Turma não encontrada.")
        return
    filename = f"relatorio_turma_{t['id']}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    width, height = letter
    y = height - 50
    c.drawString(50, y, f"Relatório - Turma {t['nome']}")
    y -= 30
    c.setFont("Helvetica", 12)
    if not t["alunos"]:
        c.drawString(50, y, "Sem alunos matriculados.")
    else:
        for aid in t["alunos"]:
            a = buscar_aluno_por_id(aid)
            c.drawString(50, y, f"{a['matricula']} - {a['nome']}")
            y -= 20
            for atv_id in t.get("atividades", []):
                atv = buscar_atividade_por_id(atv_id)
                if atv and str(aid) in atv.get("notas", {}):
                    c.drawString(70, y, f"{atv['nome']}: {atv['notas'][str(aid)]}")
                    y -= 18
            y -= 8
            if y < 70:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 40
    c.save()
    print(f"✅ PDF de turma gerado: {filename}")

# =========== BOLETINS POR ALUNO (NOVO) ===========
def gerar_boletins_pdf(corte_aprovacao=6.0):
    if not alunos:
        print("Não há alunos cadastrados.")
        return

    # cria pasta para boletins
    pasta = "boletins_alunos"
    os.makedirs(pasta, exist_ok=True)

    for aluno in alunos:
        filename = os.path.join(pasta, f"boletim_{aluno['matricula']}_{aluno['id']}.pdf")
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        margem_x = 2*cm
        y = height - 2*cm

        # cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margem_x, y, "Boletim Escolar")
        c.setFont("Helvetica", 10)
        c.drawString(width - margem_x - 200, y, f"Aluno: {aluno['nome']}")
        y -= 18
        c.drawString(margem_x, y, f"Matrícula: {aluno['matricula']}  |  ID: {aluno['id']}")
        y -= 24
        c.line(margem_x, y, width - margem_x, y)
        y -= 14

        medias_turmas = []
        # percorre turmas do aluno
        turmas_do_aluno = [t for t in turmas if aluno['id'] in t['alunos']]
        if not turmas_do_aluno:
            c.drawString(margem_x, y, "Aluno não está matriculado em nenhuma turma.")
            y -= 18
        else:
            for t in turmas_do_aluno:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margem_x, y, f"Turma: {t['nome']}")
                y -= 16
                c.setFont("Helvetica", 10)

                # cabeçalho da tabela simples
                c.drawString(margem_x, y, "Atividade")
                c.drawString(margem_x + 8*cm, y, "Descrição")
                c.drawString(margem_x + 14*cm, y, "Nota")
                y -= 12
                c.line(margem_x, y, width - margem_x, y)
                y -= 8

                notas_turma = []
                ativs = [buscar_atividade_por_id(aid) for aid in t.get("atividades", [])]
                if not ativs:
                    c.drawString(margem_x, y, "Nenhuma atividade cadastrada nesta turma.")
                    y -= 18
                else:
                    for atv in ativs:
                        nome = atv['nome']
                        descr = atv.get('descricao', '')
                        nota = atv.get("notas", {}).get(str(aluno['id']), "—")
                        nota_text = f"{nota}" if nota != "—" else "—"
                        if nota != "—":
                            try:
                                notas_turma.append(float(nota))
                            except:
                                pass
                        # escreve linha
                        c.drawString(margem_x, y, nome[:30])
                        c.drawString(margem_x + 8*cm, y, (descr[:55] if descr else ""))
                        c.drawString(margem_x + 14*cm, y, nota_text)
                        y -= 14
                        if y < 80:
                            c.showPage()
                            y = height - 2*cm
                    # média da turma para o aluno
                    media_t = sum(notas_turma)/len(notas_turma) if notas_turma else None
                    if media_t is not None:
                        medias_turmas.append(media_t)
                        c.setFont("Helvetica-Bold", 10)
                        c.drawString(margem_x, y, f"Média da turma {t['nome']}: {media_t:.2f}")
                        c.setFont("Helvetica", 10)
                        y -= 16
                    else:
                        c.drawString(margem_x, y, "Média da turma: — (sem notas)")
                        y -= 16

                y -= 6
                if y < 80:
                    c.showPage()
                    y = height - 2*cm

        # média geral do aluno (média das médias por turma)
        if medias_turmas:
            media_geral = sum(medias_turmas)/len(medias_turmas)
            situacao = "APROVADO" if media_geral >= corte_aprovacao else "REPROVADO"
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margem_x, y, f"Média geral: {media_geral:.2f}   |   Situação: {situacao}")
        else:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margem_x, y, "Média geral: —   |   Situação: — (sem notas)")

        c.save()
        print(f"✅ Boletim gerado: {filename}")

# =========== RELATÓRIO INTELIGENTE / AUXILIARES ===========
def gerar_relatorio_inteligente():
    print("\n=== Relatório Inteligente ===")
    for t in turmas:
        notas_turma = []
        for atv_id in t.get("atividades", []):
            atv = buscar_atividade_por_id(atv_id)
            if atv:
                for v in atv.get("notas", {}).values():
                    notas_turma.append(v)
        media = sum(notas_turma)/len(notas_turma) if notas_turma else 0
        if media >= 8.5:
            analise = "Excelente desempenho"
        elif media >= 7:
            analise = "Bom desempenho"
        elif media >= 5:
            analise = "Desempenho mediano"
        else:
            analise = "Desempenho abaixo do esperado"
        print(f"Turma {t['nome']} - Média: {media:.2f} -> {analise}")

def melhor_pior_aluno_turma():
    listar_turmas()
    if not turmas: return
    tid = input_int("ID da turma (0 cancelar): ", min_val=0)
    if tid == 0: return
    t = buscar_turma_por_id(tid)
    if not t:
        print("Turma não encontrada.")
        return
    resultados = []
    for aid in t["alunos"]:
        soma = 0
        cnt = 0
        for atv_id in t.get("atividades", []):
            atv = buscar_atividade_por_id(atv_id)
            if atv and str(aid) in atv.get("notas", {}):
                soma += atv["notas"][str(aid)]
                cnt += 1
        media = soma/cnt if cnt>0 else None
        resultados.append({"aluno_id": aid, "media": media})
    # filtrar sem notas
    com_notas = [r for r in resultados if r["media"] is not None]
    if not com_notas:
        print("Nenhum aluno com notas nesta turma.")
        return
    melhor = max(com_notas, key=lambda x: x["media"])
    pior = min(com_notas, key=lambda x: x["media"])
    a_melhor = buscar_aluno_por_id(melhor["aluno_id"])
    a_pior = buscar_aluno_por_id(pior["aluno_id"])
    print(f"Melhor: {a_melhor['nome']} - Média: {melhor['media']:.2f}")
    print(f"Pior: {a_pior['nome']} - Média: {pior['media']:.2f}")

# =========== MENUS (BONITOS) ===========
def linha(tam=60):
    return "-" * tam

def header(title):
    print("\n" + linha(70))
    print(f"📚  {title}")
    print(linha(70))

def menu_acesso():
    header("ACESSO AO SISTEMA - Política de Privacidade (LGPD)")
    print("A escola respeita a Lei Geral de Proteção de Dados (13.709/2018).")
    print("Os dados são usados apenas para fins educacionais e administrativos.\n")
    print("1. Cadastrar professor")
    print("2. Login")
    print("0. Sair")
    return input("Escolha: ").strip()

def menu_principal():
    nome = usuario_logado['nome'] if usuario_logado else "Nenhum"
    header(f"SISTEMA ESCOLAR - Professor: {nome}")
    print("1. Gerenciar Alunos")
    print("2. Turmas")
    print("3. Atividades e Notas")
    print("4. Relatórios e PDFs")
    print("5. Logout")
    print("0. Sair")
    return input("Escolha: ").strip()

def menu_professores_ui():
    header("PROFESSORES")
    print("1. Listar professores")
    print("2. Cadastrar professor")
    print("3. Editar professor")
    print("4. Remover professor")
    print("0. Voltar")
    return input("Escolha: ").strip()

def menu_alunos_ui():
    header("ALUNOS")
    print("1. Listar alunos")
    print("2. Cadastrar aluno")
    print("3. Editar aluno")
    print("4. Remover aluno")
    print("5. Buscar aluno")
    print("6. Ver turmas do aluno")
    print("0. Voltar")
    return input("Escolha: ").strip()

def menu_turmas_ui():
    header("TURMAS")
    print("1. Listar turmas")
    print("2. Cadastrar turma")
    print("3. Editar turma")
    print("4. Remover turma")
    print("5. Ver alunos da turma")
    print("6. Ver atividades da turma")
    print("7. Matricular aluno")
    print("8. Desmatricular aluno")
    print("0. Voltar")
    return input("Escolha: ").strip()

def menu_atividades_ui():
    header("ATIVIDADES E NOTAS")
    print("1. Listar atividades")
    print("2. Cadastrar atividade (com descrição)")
    print("3. Editar atividade")
    print("4. Remover atividade")
    print("5. Ver notas de uma atividade")
    print("6. Adicionar/editar nota")
    print("7. Remover nota")
    print("0. Voltar")
    return input("Escolha: ").strip()

def menu_relatorios_ui():
    header("RELATÓRIOS E PDFS")
    print("1. Gerar relatório (texto) por turma")
    print("2. Gerar relatório (PDF) por turma")
    print("3. Gerar boletins em PDF (um por aluno)")
    print("4. Relatório inteligente (médias por turma)")
    print("5. Melhor/pior aluno por turma")
    print("0. Voltar")
    return input("Escolha: ").strip()

# =========== LOGIN / EXECUÇÃO ===========
def login_professor_interface():
    global usuario_logado
    header("LOGIN")
    matricula = input("Matrícula: ").strip()
    senha = getpass.getpass("Senha: ")
    for p in professores:
        if p["matricula"] == matricula and p["senha"] == hash_senha(senha):
            usuario_logado = p
            print(f"✅ Bem-vindo, {p['nome']}!")
            return True
    print("❌ Matrícula ou senha inválida.")
    return False

def logout_professor():
    global usuario_logado
    usuario_logado = None
    print("🔒 Logout realizado.")

def main():
    carregar_tudo()
    while True:
        op = menu_acesso()
        if op == "1":
            cadastrar_professor()
        elif op == "2":
            if login_professor_interface():
                break
        elif op == "0":
            print("Saindo...")
            return
        else:
            print("Opção inválida.")

    # menu principal
    while True:
        op = menu_principal()
        if op == "1":
            while True:
                sub = menu_professores_ui()
                if sub == "1": listar_professores()
                elif sub == "2": cadastrar_professor()
                elif sub == "3": editar_professor()
                elif sub == "4": remover_professor()
                elif sub == "0": break
                else: print("Inválido.")
        elif op == "2":
            while True:
                sub = menu_alunos_ui()
                if sub == "1": listar_alunos()
                elif sub == "2": cadastrar_aluno()
                elif sub == "3": editar_aluno()
                elif sub == "4": remover_aluno()
                elif sub == "5": buscar_aluno()
                elif sub == "6": ver_turmas_do_aluno()
                elif sub == "0": break
                else: print("Inválido.")
        elif op == "3":
            while True:
                sub = menu_turmas_ui()
                if sub == "1": listar_turmas()
                elif sub == "2": cadastrar_turma()
                elif sub == "3": editar_turma()
                elif sub == "4": remover_turma()
                elif sub == "5": ver_alunos_da_turma()
                elif sub == "6": ver_atividades_da_turma()
                elif sub == "7": matricular_aluno_em_turma()
                elif sub == "8": desmatricular_aluno()
                elif sub == "0": break
                else: print("Inválido.")
        elif op == "4":
            while True:
                sub = menu_atividades_ui()
                if sub == "1": listar_atividades()
                elif sub == "2": cadastrar_atividade()
                elif sub == "3": editar_atividade()
                elif sub == "4": remover_atividade()
                elif sub == "5": ver_notas_atividade()
                elif sub == "6": adicionar_editar_nota()
                elif sub == "7": remover_nota()
                elif sub == "0": break
                else: print("Inválido.")
        elif op == "5":
            while True:
                sub = menu_relatorios_ui()
                if sub == "1": gerar_relatorio_texto()
                elif sub == "2": gerar_relatorios_pdf_turma()
                elif sub == "3": gerar_boletins_pdf()
                elif sub == "4": gerar_relatorio_inteligente()
                elif sub == "5": melhor_pior_aluno_turma()
                elif sub == "0": break
                else: print("Inválido.")
        elif op == "6":
            logout_professor()
            salvar_tudo()
            main()  # reinicia fluxo de login
            return
        elif op == "0":
            salvar_tudo()
            print("Saindo...")
            return
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
