import tkinter as tk
from tkinter import filedialog, messagebox

def metodo_basico(sequencia, padrao):
    """Realiza a busca pelo método básico de comparação."""
    ocorrencias = 0
    comparacoes = 0

    for i in range(len(sequencia) - len(padrao) + 1):
        match = True
        for j in range(len(padrao)):
            comparacoes += 1
            if sequencia[i + j] != padrao[j]:
                match = False
                break
        if match:
            ocorrencias += 1

    return ocorrencias, comparacoes


def calcular_lps(padrao):
    """Calcula o array de prefixo para o algoritmo KMP."""
    lps = [0] * len(padrao)
    comprimento = 0
    i = 1

    while i < len(padrao):
        if padrao[i] == padrao[comprimento]:
            comprimento += 1
            lps[i] = comprimento
            i += 1
        else:
            if comprimento != 0:
                comprimento = lps[comprimento - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def metodo_kmp(sequencia, padrao):
    """Realiza a busca pelo algoritmo KMP."""
    ocorrencias = 0
    comparacoes = 0

    lps = calcular_lps(padrao)
    i = 0  # Índice na sequência
    j = 0  # Índice no padrão

    while i < len(sequencia):
        comparacoes += 1
        if padrao[j] == sequencia[i]:
            i += 1
            j += 1

        if j == len(padrao):
            ocorrencias += 1
            j = lps[j - 1]
        elif i < len(sequencia) and padrao[j] != sequencia[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return ocorrencias, comparacoes


def realizar_busca():
    """Executa a busca pelos dois métodos e exibe os resultados."""
    sequencia = text_sequencia.get("1.0", tk.END).strip()
    padrao = entry_padrao.get().strip()

    if not sequencia or not padrao:
        messagebox.showwarning("Entrada inválida", "Insira a sequência de DNA e a subsequência a ser buscada.")
        return

    # Busca pelo método básico
    ocorrencias_basico, comparacoes_basico = metodo_basico(sequencia, padrao)

    # Busca pelo método KMP
    ocorrencias_kmp, comparacoes_kmp = metodo_kmp(sequencia, padrao)

    # Exibe os resultados
    messagebox.showinfo(
        "Resultados da Busca",
        f"Método Básico:\n"
        f"Ocorrências: {ocorrencias_basico}\n"
        f"Comparações: {comparacoes_basico}\n\n"
        f"Método KMP:\n"
        f"Ocorrências: {ocorrencias_kmp}\n"
        f"Comparações: {comparacoes_kmp}"
    )


def carregar_arquivo():
    """Carrega uma sequência de DNA de um arquivo."""
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo de DNA",
        filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
    )
    if file_path:
        with open(file_path, "r") as file:
            sequencia = file.read().replace("\n", "").strip()
            text_sequencia.delete("1.0", tk.END)
            text_sequencia.insert(tk.END, sequencia)


# Configuração da interface gráfica
root = tk.Tk()
root.title("Busca de Subsequências em DNA")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

lbl_sequencia = tk.Label(frame, text="Sequência de DNA:")
lbl_sequencia.grid(row=0, column=0, sticky="w")

text_sequencia = tk.Text(frame, height=10, width=50)
text_sequencia.grid(row=1, column=0, columnspan=2, pady=5)

btn_carregar = tk.Button(frame, text="Carregar Arquivo", command=carregar_arquivo)
btn_carregar.grid(row=2, column=0, columnspan=2, pady=5)

lbl_padrao = tk.Label(frame, text="Subsequência a buscar:")
lbl_padrao.grid(row=3, column=0, sticky="w")

entry_padrao = tk.Entry(frame, width=30)
entry_padrao.grid(row=4, column=0, pady=5)

btn_buscar = tk.Button(frame, text="Buscar", command=realizar_busca)
btn_buscar.grid(row=4, column=1, pady=5)

root.mainloop()
