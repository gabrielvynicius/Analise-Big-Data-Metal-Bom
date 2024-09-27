import pandas as pd
import plotly.graph_objects as go

df = pd.read_excel(
    'C:/Users/gabriel/Documents/TRABALHOS DE FACULDADE/Dados dos Clientes Metal Bom/Controle_de_Clientes_Metal_Bom.xlsx'
)

# Tratameto de dados.
df['Data do Serviço'] = pd.to_datetime(
    df['Data do Serviço'], dayfirst=True, errors='coerce'
)

df['Ano'] = df['Data do Serviço'].dt.year
df['Mês'] = df['Data do Serviço'].dt.month_name(locale='pt_PT')

df = df.dropna(subset=['Data do Serviço'])

contagem_mensal = df.groupby(
    ['Ano', 'Mês']).size().reset_index(name='Atendimentos')

meses_ordem = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
               "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

anos = df['Ano'].unique()
meses_completos = pd.MultiIndex.from_product(
    [anos, meses_ordem], names=['Ano', 'Mês']
)

contagem_mensal = contagem_mensal.set_index(['Ano', 'Mês']).reindex(
    meses_completos, fill_value=0).reset_index()

# Configurando a anlise de dados.
fig = go.Figure()

for ano in contagem_mensal['Ano'].unique():
    dados_ano = contagem_mensal[contagem_mensal['Ano'] == ano]
    fig.add_trace(go.Scatter(
        x=dados_ano['Mês'], y=dados_ano['Atendimentos'], mode='lines+markers', name=str(ano)
    ))

fig.update_layout(
    title='Atendimentos por Mês',
    xaxis_title='Mês',
    yaxis_title='Número de Atendimentos',
    xaxis=dict(tickmode='array', tickvals=meses_ordem, ticktext=meses_ordem),
    yaxis=dict(range=[0, max(contagem_mensal['Atendimentos']) + 5]),
    template='plotly_white'
)

fig.show()

print("Dados originais do DataFrame:")
print(df.head())

print("Contagem mensal de atendimentos:")
print(contagem_mensal)

print(anos)
