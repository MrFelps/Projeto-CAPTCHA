# %%
# CÉLULA 1: Captura de tela e criação do DataFrame original
# Execute esta célula primeiro para criar a variável 'df'.

from capt import get_screenshot_tesser
import time
import pandas as pd
import rapidfuzz

print("Iniciando captura de tela em 3 segundos...")
time.sleep(7) # Mais tempo para garantir o foco

# Executa a função de OCR e armazena a tabela na variável 'df'
df = get_screenshot_tesser()
print("Captura concluída! O DataFrame 'df' foi criado.")


# %%
# CÉLULA 2: Cálculo das Notas e Criação da Tabela Final

queries = ["sou", "robô"] 
choices = df.text.to_list()
scores = rapidfuzz.process.cdist(queries, choices)

scores_df = pd.DataFrame(scores).T.rename(columns={0: "sou", 1: "robô"})

final_df = pd.concat([df, scores_df], axis=1)
final_df

# %%
# CÉLULA 3: Filtrando os Resultados para Encontrar a Palavra-Chave
# Execute esta célula DEPOIS da Célula 2 para encontrar a melhor correspondência.

# A nossa supertabela já existe na variável 'final_df'

# O número 80 é o nosso "nível de confiança". Você pode ajustar se precisar.
# Estamos procurando por linhas onde a nota da coluna 'arobot' é maior que 80.
robot_word_info = final_df.loc[final_df['robô'] > 80]

print("Resultado do filtro (palavras com similaridade > 80 com 'arobot'):")

# Mostra a(s) linha(s) que passaram no filtro
robot_word_info

# %%
# CÉLULA 4: Investigando as melhores correspondências
# Este código vai ordenar a tabela para vermos as palavras mais relevantes.

# Ordena o DataFrame final pela coluna 'robô', da maior nota para a menor,
# e nos mostra as 5 primeiras linhas.
final_df.sort_values(by='robô', ascending=False).head(5)
# %%
