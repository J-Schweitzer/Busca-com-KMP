import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import networkx as nx
from pyvis.network import Network

def identificar_alfabeto(arquivo):
    """Identifica automaticamente o alfabeto presente no arquivo."""
    alfabeto = set()
    with open(arquivo, "r") as file:
        for linha in file:
            for letra in linha:
                if letra != '\n' and letra.isprintable():  # Ignora quebras de linha e caracteres não imprimíveis
                    alfabeto.add(letra)
    return sorted(alfabeto)  # Ordena para facilitar a visualização

def realizar_busca():
    # Obtém o arquivo e a cadeia a partir da interface
    arquivo = file_path.get()
    cadeia = entry_cadeia.get()

    if not arquivo or not cadeia:
        messagebox.showwarning("Entrada inválida", "Selecione um arquivo e insira uma cadeia de busca.")
        return

    # Identifica automaticamente o alfabeto a partir do arquivo
    alfabeto = identificar_alfabeto(arquivo)
    
    if not alfabeto:
        messagebox.showwarning("Alfabeto vazio", "Não foram encontrados caracteres no arquivo.")
        return

    # Processa o arquivo para busca
    with open(arquivo, "r") as file:
        cmaior = [letra for linha in file for letra in linha if letra != '\n']
    cmenor = [char for char in cadeia]

    # Código de busca SEM autômato
    qtd_ocorrencias_sem, qtd_comparacoes_sem = 0, 0
    for i in range(len(cmaior)):
        achou = True
        for j in range(len(cmenor)):
            if (i + j) == len(cmaior):
                achou = False
                break
            qtd_comparacoes_sem += 1
            if cmenor[j] != cmaior[i + j]:
                achou = False
        if achou:
            qtd_ocorrencias_sem += 1

    # Código de busca COM autômato
    def maiorPrefSufProprio(cadeia):
        maior = 0
        for i in reversed(range(len(cadeia) - 1)):
            prefixo, sufixo = cadeia[:(i + 1)], cadeia[-(i + 1):]
            if prefixo == sufixo and len(prefixo) > maior:
                maior = len(prefixo)
                break
        return maior

    def criaTransicoes(cadeia, alfabeto):
        sub, transicoes = "", []
        for estado in range(len(cadeia) + 1):
            letra_correta = cadeia[estado] if estado < len(cadeia) else 'FIM'
            for letra_alternativa in alfabeto:
                proximo = estado + 1 if letra_alternativa == letra_correta else maiorPrefSufProprio(sub + letra_alternativa)
                transicao = ['s' + str(estado), letra_alternativa, 's' + str(proximo)]
                transicoes.append(transicao)
            sub += letra_correta
        return transicoes

    estados = ['s' + str(n) for n in range(len(cadeia) + 1)]
    inicial, finais = estados[:1], estados[-1:]
    transicoes = criaTransicoes(cadeia, alfabeto)
    dtransicoes = dict(((e1, e2), s) for e1, e2, s in transicoes)

    qtd_ocorrencias_com, qtd_comparacoes_com, estado = 0, 0, inicial[0]
    for i in range(len(cmaior)):
        if estado in finais:
            qtd_ocorrencias_com += 1
        simbolo = cmaior[i]
        estado = dtransicoes.get((estado, simbolo), None)
        if estado is None:
            break
        qtd_comparacoes_com += 1

    if estado in finais:
        qtd_ocorrencias_com += 1

    # Exibe os resultados
    messagebox.showinfo("Resultado", f"Ocorrências SEM autômato: {qtd_ocorrencias_sem}\nComparações SEM autômato: {qtd_comparacoes_sem}\nOcorrências COM autômato: {qtd_ocorrencias_com}\nComparações COM autômato: {qtd_comparacoes_com}")
    
    # Visualização do autômato
    G = nx.DiGraph()
    for estado in estados:
        G.add_node(estado, color="red" if estado in finais else "blue")
    for v in transicoes:
        G.add_edge(v[0], v[2], label=v[1])

    nt = Network('500px', '800px', directed=True)
    nt.from_nx(G)
    nt.write_html("G.html")
    webbrowser.open("G.html")

def selecionar_arquivo():
    file_selected = filedialog.askopenfilename()
    file_path.set(file_selected)

# Configuração da interface
root = tk.Tk()
root.title("Busca em Arquivo")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

file_path = tk.StringVar()

btn_arquivo = tk.Button(frame, text="Selecionar Arquivo", command=selecionar_arquivo)
btn_arquivo.grid(row=0, column=0, padx=5, pady=5)

entry_file = tk.Entry(frame, textvariable=file_path, width=40)
entry_file.grid(row=0, column=1, padx=5, pady=5)

lbl_cadeia = tk.Label(frame, text="Cadeia a ser buscada:")
lbl_cadeia.grid(row=1, column=0, padx=5, pady=5)

entry_cadeia = tk.Entry(frame)
entry_cadeia.grid(row=1, column=1, padx=5, pady=5)

btn_buscar = tk.Button(frame, text="Buscar", command=realizar_busca)
btn_buscar.grid(row=2, columnspan=2, pady=10)

root.mainloop()
