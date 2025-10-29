import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- OS SEUS DADOS RECOLHIDOS ---
data = {
    ('Python', 'Sim', 10):   {'RPS': 5.1,   'Mediano': 4,   'Falhas': 0},
    ('Python', 'Sim', 100):  {'RPS': 50.4,  'Mediano': 6,   'Falhas': 0},
    ('Python', 'Sim', 1000): {'RPS': 82.5,  'Mediano': 4,   'Falhas': 676},
    ('Python', 'Não', 10):   {'RPS': 5.2,   'Mediano': 3,   'Falhas': 0},
    ('Python', 'Não', 100):  {'RPS': 50.6,  'Mediano': 3,   'Falhas': 0},
    ('Python', 'Não', 1000): {'RPS': 74.2,  'Mediano': 4,   'Falhas': 1540},
    ('Ruby',   'Sim', 10):   {'RPS': 5.2,   'Mediano': 8,   'Falhas': 0},
    ('Ruby',   'Sim', 100):  {'RPS': 51.0,  'Mediano': 5,   'Falhas': 0},
    ('Ruby',   'Sim', 1000): {'RPS': 107.3, 'Mediano': 4,   'Falhas': 988},
    ('Ruby',   'Não', 10):   {'RPS': 5.3,   'Mediano': 7,   'Falhas': 0},
    ('Ruby',   'Não', 100):  {'RPS': 50.8,  'Mediano': 5,   'Falhas': 0},
    ('Ruby',   'Não', 1000): {'RPS': 91.6,  'Mediano': 4,   'Falhas': 666},
}

# Organiza os dados numa tabela (DataFrame)
df = pd.DataFrame.from_dict(data, orient='index')
df.index = pd.MultiIndex.from_tuples(df.index, names=['Versão API', 'Cache Ligado?', 'Usuários'])
df.reset_index(inplace=True)

# Garante a ordem correta dos usuários para os gráficos
df['Usuários'] = pd.Categorical(df['Usuários'], categories=[10, 100, 1000], ordered=True)

# --- FUNÇÃO PARA GERAR OS GRÁFICOS ---
def gerar_graficos_por_versao(versao_api):
    df_versao = df[df['Versão API'] == versao_api]

    # Gráfico 1: Tempo de Resposta vs. Número de Usuários (Com vs Sem Cache)
    df_pivot_tempo = df_versao.pivot(index='Usuários', columns='Cache Ligado?', values='Mediano')
    ax1 = df_pivot_tempo.plot(
        kind='bar',
        figsize=(10, 6),
        title=f'Desempenho ({versao_api}): Tempo Mediano vs. Carga (Com vs. Sem Cache)',
        width=0.8
    )
    ax1.set_ylabel('Tempo de Resposta Mediano (ms)')
    ax1.set_xlabel('Número de Usuários Simulados')
    ax1.legend(title='Cache Ativo?')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
    plt.tight_layout()
    plt.savefig(f'grafico_tempo_{versao_api.lower()}.png')
    print(f"Gráfico 'grafico_tempo_{versao_api.lower()}.png' gerado com sucesso.")
    plt.close() # Fecha a figura para não interferir com a próxima

    # Gráfico 2: RPS vs. Número de Usuários (Com vs Sem Cache)
    df_pivot_rps = df_versao.pivot(index='Usuários', columns='Cache Ligado?', values='RPS')
    ax2 = df_pivot_rps.plot(
        kind='bar',
        figsize=(10, 6),
        title=f'Capacidade ({versao_api}): RPS vs. Carga (Com vs. Sem Cache)',
        width=0.8
    )
    ax2.set_ylabel('Requisições por Segundo (RPS)')
    ax2.set_xlabel('Número de Usuários Simulados')
    ax2.legend(title='Cache Ativo?')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
    plt.tight_layout()
    plt.savefig(f'grafico_rps_{versao_api.lower()}.png')
    print(f"Gráfico 'grafico_rps_{versao_api.lower()}.png' gerado com sucesso.")
    plt.close() # Fecha a figura

# --- GERAR OS GRÁFICOS PARA PYTHON E RUBY ---
gerar_graficos_por_versao('Python')
gerar_graficos_por_versao('Ruby')

print("\n--- Concluído ---")
print("Foram gerados 4 gráficos comparando o desempenho com e sem cache para Python e Ruby.")