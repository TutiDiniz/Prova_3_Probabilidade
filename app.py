import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import math
from scipy.stats import norm


st.set_option('deprecation.showPyplotGlobalUse', False)
rng = np.random.default_rng()

def soma_amostras(amostras):
    Sn_amostras = []
    for amostra in amostras:
      soma = 0
      for resultado in amostra:
        soma += resultado
      Sn_amostras.append(soma)
    return Sn_amostras

def padroniza_amostras(amostras, u, dp):
    Zn = []
    Sn_amostras = soma_amostras(amostras)
    for Sn in Sn_amostras:
        z = (Sn - (n*u)) / (dp * np.sqrt(n))
        Zn.append(z)
    return Zn    

def binomial(p, m, n):
    gerar_amostras = rng.binomial(n, p, size=(m, n))
    u = n * p
    dp = (np.sqrt(p * (1 - p) * n))
    Zn = padroniza_amostras(gerar_amostras, u, dp)
    amostras = np.hstack(gerar_amostras)
    return amostras, Zn

def exponencial(l, m, n):
    gerar_amostras = rng.exponential(scale=1/l, size=(m,n))
    u = 1/l
    dp = 1/l
    Zn = padroniza_amostras(gerar_amostras, u, dp)
    amostras = np.hstack(gerar_amostras)
    return amostras, Zn

def uniforme(a, b, m, n):
    gerar_amostras = rng.uniform(a, b, size=(m,n))
    u = (a+b)/2
    dp = np.sqrt(pow(a-b, 2) / 12)
    Zn = padroniza_amostras(gerar_amostras, u, dp)
    amostras = np.hstack(gerar_amostras)
    return amostras, Zn  

def plotar_graficos(amostras, media_amostral):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6))

    ax1.hist(amostras, bins = 20, density = True, color='lightblue')
    ax1.set_title('Histograma das Amostras')

    ax2.hist(media_amostral, bins=bins, density=True, color='pink')

    x = np.linspace(-4, 4, 1000)
    ax2.plot(x, norm.pdf(x, loc=0, scale=1), color='red')
    ax2.set_title('Histograma das Médias Amostrais Normalizadas e Normal (0, 1)')
    return fig

def comentarios_normal():
    st.write("**Aproximação pela Normal (0, 1):** Em todos os casos, o Teorema Central do Limite oferece uma perspectiva \
    fundamental sobre o comportamento das médias amostrais. Podemos ver que, mesmo quando a distribuição original não é normal,\
     as médias amostrais normalizadas tendem a seguir uma distribuição normal com média igual a 0 e desvio padrão igual a 1, \
     principalmente a medida que o tamanho da amostra aumenta.")


st.header('Simulação Teorema Central do Limite')
st.write('Nesse projeto vamos simular experimentalmente o teorema central do limite, analisando os resultados por meios de gráficos \
para as distruibuições binomial, exponencial e uniforme.')
st.markdown("#### Selecione os valores desejados para as variáveis:")
m = st.number_input('Número de Amostras (m)', min_value = 100, max_value = 2000, step = 100, value = 1000)
n = st.number_input('Tamanho das Amostras (n)', min_value = 5, max_value = 200, step = 10, value = 100)
bins = st.number_input('Quantidade de bins (ajuste conforme necessário, menos bins são mais interessantes para dados mais concentrados)', min_value = 5, max_value = 55, step = 2, value = 35)

st.sidebar.markdown('## Distribuições de Probabilidade')

categorias = list({'Binomial', 'Exponencial', 'Uniforme'})

categoria = st.sidebar.selectbox('Selecione a distribuição que deseja simular', options = categorias)

if categoria == 'Binomial':
    p = st.sidebar.slider('Probabilidade de Succeso (p)', min_value = 0.05, max_value = 0.95, step = 0.05, value = 0.5)
    amostras, media_amostral = binomial(p, m, n)
    if st.button('Gerar e Plotar'):
        st.markdown("## Distribuição Binomial")
        fig = plotar_graficos(amostras, media_amostral)
        st.pyplot(fig)

        st.write("**1 - Distribuição Binomial com p = 0.1:** Ao analisar a distribuição binomial com uma baixa probabilidade de \
        sucesso p = 0,1, notamos que a maioria dos eventos resulta em falhas. \
        A forma da distribuição é assimétrica, com uma concentração significativa de valores próximos a zero. Isso ocorre devido \
        à probabilidade relativamente baixa de sucesso em cada tentativa independente.")


        st.write("**2 - Distribuição Binomial com p = 0.5:** Ao contrário da distribuição com baixa probabilidade de sucesso,\
        a distribuição binomial com p = 0,5 exibe uma simetria mais pronunciada em torno da média. Isso ocorre porque,\
        com uma probabilidade de sucesso de 0,5 em cada tentativa independente, os resultados positivos e negativos têm uma \
        probabilidade semelhante de ocorrência.")

        comentarios_normal()

if categoria == 'Exponencial':
    l = st.sidebar.number_input('Parâmetro λ', min_value = 1, max_value = 22, step = 3, value = 7)
    amostras, media_amostral = exponencial(l, m, n)
    if st.button('Gerar e Plotar'):
        st.markdown("## Distribuição Exponencial")
        fig = plotar_graficos(amostras, media_amostral)
        st.pyplot(fig)

        st.write(f"**1 - Distribuição Exponencial:** Ao examinarmos o histograma das amostras para a distribuição exponencial com λ = {l},\
        percebemos que os dados seguem uma decaída exponencial. A forma de decaída dos dados indica que a probabilidade de eventos \
        raros diminui exponencialmente à medida que avançamos ao longo da distribuição. Valores iniciais têm maior probabilidade de \
        ocorrência, enquanto valores mais distantes do início têm probabilidade progressivamente menor. Essa propriedade faz da \
        distribuição exponencial uma escolha adequada para modelar fenômenos como o tempo entre eventos sucessivos e o decaimento \
        radioativo.")

        comentarios_normal()

if categoria == 'Uniforme':
    a = st.sidebar.number_input('Parâmetro a', min_value = 5, max_value = 20, step = 5, value = 15)
    b = st.sidebar.number_input('Parâmetro b', min_value = 25, max_value = 50, step = 5, value = 35)
    amostras, media_amostral = uniforme(a, b, m, n)
    if st.button('Gerar e Plotar'):
        st.markdown("## Distribuição Uniforme")
        fig = plotar_graficos(amostras, media_amostral)
        st.pyplot(fig)
        
        st.subheader('Comentários:')
        st.write(f"**1 - Distribuição Uniforme:** A observação da distribuição uniforme revela que os dados estão igualmente distribuídos\
        em todo o intervalo definido [{a}, {b}]. Isso significa que a probabilidade de um valor ocorrer em qualquer subintervalo é constante,\
        sem qualquer preferência por determinadas faixas. Não há evidências de viés em direção a valores específicos, e a uniformidade dos\
        dados é evidente visualmente no histograma das amostras.")

        comentarios_normal()


