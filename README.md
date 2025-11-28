Funcionamento do Código:
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Ele permite gerenciar:

👨‍🏫 Professores

👦 Alunos

🏫 Turmas

📝 Atividades

⭐ Notas

📄 Relatórios e boletins em PDF

Tudo é salvo em arquivos JSON, então nada se perde quando você fecha o programa.

O sistema tem menus organizados e exige login de professor para acessar as funções.

🧠 Como o código funciona (bem simples)
✔️ Armazena dados em JSON

São usados 4 arquivos:

professores.json

alunos.json

turmas.json

atividades.json

O sistema cria os arquivos automaticamente na primeira execução.

✔️ Tem menus para cada parte do sistema

Os menus são assim:

Menu de acesso → cadastrar professor ou login

Menu principal → alunos, turmas, atividades, PDFs

Submenus → editar, cadastrar, remover, etc.

✔️ Gera PDF

Com:

Boletim individual do aluno

Relatório completo da turma

Relatório inteligente

Usa a biblioteca reportlab.

------------------------------------------------------------------------------------------------------------------------------------------------------------------

▶️ Como rodar o sistema (bem simples)
1️⃣ Instale o Python

Python 3.10 ou mais novo.

2️⃣ Instale a biblioteca usada para gerar PDFs

No terminal:

pip install reportlab

3️⃣ Coloque o arquivo pim.py dentro de uma pasta vazia

O programa vai criar os JSONs automaticamente.

4️⃣ Rode o sistema

No terminal:

python pim.py


Pronto! O sistema abre o menu inicial.

▶️ Primeiro uso

Escolha Cadastrar Professor

Faça login com a matrícula e senha cadastradas

Acesse todas as funções do sistema
