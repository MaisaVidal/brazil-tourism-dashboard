from faulthandler import disable
from operator import index
from numpy.core.fromnumeric import size
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import altair as alt
import folium
from folium import plugins
from streamlit_folium import folium_static
from wordcloud import WordCloud
from itertools import chain
import collections
import plotly.express as px

@st.cache(hash_funcs={"MyUnhashableClass6": lambda _: None})
def wordCloudEntidades(dataset):
    sumary = []
    sumary = list(chain(*dataset['lista_entidades']))
    
    if (len(sumary)>0):
        all_summary = " ".join(s for s in sumary)
        wordcloud = WordCloud(
                      background_color="black",
                      width=1600, height=800).generate(all_summary)    

        return wordcloud
    else:    
        return -1
    


@st.cache(hash_funcs={"MyUnhashableClass5": lambda _: None})
def wordCloud(dataset):
    sumary = []
    summary_subs = list(chain(*dataset['lista_substantivos']))
    summary_verbos = list(chain(*dataset['lista_verbos']))
    summary_adjetivos = list(chain(*dataset['lista_adjetivos']))
    
    sumary.extend(summary_subs)
    sumary.extend(summary_verbos)
    sumary.extend(summary_adjetivos)
    all_summary = " ".join(s for s in sumary)
 
    titulo = atracao    
    wordcloud = WordCloud(
                      background_color="black",
                      width=1600, height=800).generate(all_summary)    

    return wordcloud

def media_qtde_caracteres(dataset):   
  return round(dataset['qtde_caracteres_comentario'].mean(), 2)

def media_qtde_token(dataset):
  return round(dataset['qtde_tokens_comentario'].mean(), 2)  

st.set_page_config(layout="wide")

@st.cache(hash_funcs={"MyUnhashableClass": lambda _: None})
def load_dataset():
    return pd.read_json("dataset-versao8.json")

@st.cache(hash_funcs={"MyUnhashableClass2": lambda _: None})
def load_nomes_atracoes():
    return pd.read_csv('nomes_atracoes.csv')

@st.cache(hash_funcs={"MyUnhashableClass4": lambda _: None})
def load_scores_sentencas():
    return pd.read_csv('scores_sentencas_com_tamanho.csv')

    
df_todos = load_dataset()
df_scores_sentencas = load_scores_sentencas()

mes_nome = {1: 'JANEIRO', 2: 'FEVEREIRO', 3: 'MARÇO', 4: 'ABRIL', 5: 'MAIO',
                6: 'JUNHO', 7: 'JULHO', 8: 'AGOSTO', 9: 'SETEMBRO', 10: 'OUTUBRO',
                11: 'NOVEMBRO', 12: 'DEZEMBRO'}

MEDIA_NOTAS_BRASIL = round(df_todos['rating'].mean(), 2)
MEDIA_CARACTERES_BRASIL = media_qtde_caracteres(df_todos)
MEDIA_TOKENS_BRASIL = media_qtde_token(df_todos)
TOTAL_COMENTARIOS_BRASIL = len(df_todos)
TOTAL_USUARIOS_BRASIL = len(pd.DataFrame(df_todos['usuario'].dropna().value_counts()))
TOTAL_ATRACOES_BRASIL = len(pd.DataFrame(df_todos['atracao'].dropna().value_counts()))
TOTAL_CIDADES_BRASIL = len(pd.DataFrame(df_todos['cidade'].dropna().value_counts()))
 
def porcentagem_nota(media_estado):
    return str(round(((media_estado - MEDIA_NOTAS_BRASIL)*100)/MEDIA_NOTAS_BRASIL,2)) + " %" 
def porcentagem_caracter(media_estado):
    return str(round(((media_estado - MEDIA_CARACTERES_BRASIL)*100)/MEDIA_CARACTERES_BRASIL,2)) + " %"
def porcentagem_token(media_estado):
    return str(round(((media_estado - MEDIA_TOKENS_BRASIL)*100)/MEDIA_TOKENS_BRASIL,2)) + " %"

def porcentagem_total_comentarios(total_coments_estado):
    return str(round((total_coments_estado*100)/TOTAL_COMENTARIOS_BRASIL,2)) + " %" 

def porcentagem_total_usuarios(total_usuarios_estado):
    return str(round((total_usuarios_estado*100)/TOTAL_USUARIOS_BRASIL,2)) + " %" 

def porcentagem_total_atracoes(total_atracoes_estado):
    return str(round((total_atracoes_estado*100)/TOTAL_ATRACOES_BRASIL,2)) + " %" 

def porcentagem_total_cidades(total_cidades_estado):
    return str(round((total_cidades_estado*100)/TOTAL_CIDADES_BRASIL,2)) + " %" 

def mes_mais_visitado():
    mes_df_qtde = pd.DataFrame(df['mes_data'].dropna().value_counts()).reset_index()
    mes_df_qtde.columns = ['mes_data', 'qtde_comentarios']
    mes_df_qtde = mes_df_qtde.sort_values(by='qtde_comentarios', ascending=False)
    return mes_nome[mes_df_qtde['mes_data'][0]]

def ano_mais_visitado():
    ano_df_qtde = pd.DataFrame(df['ano_data'].dropna().value_counts()).reset_index()
    ano_df_qtde.columns = ['ano_data', 'qtde_comentarios']
    ano_df_qtde = ano_df_qtde.sort_values(by='qtde_comentarios', ascending=False)
    return ano_df_qtde['ano_data'][0]

def sentencas_mais_positivas(n_top):
    df_filtrado = df_scores_sentencas[(df_scores_sentencas.indice_comentario.isin(df.index.tolist())) & (df_scores_sentencas.tam_sentenca > 4)]
    
    df_ordenado_por_score = df_filtrado.sort_values(by='score_positivo',ascending=False).head(n_top)
    html = ""
    for sentenca in df_ordenado_por_score['sentenca']:
        html = html + "* *"+sentenca+"*\n"
    st.markdown(html)

def sentencas_mais_positivas_localidade(n_top):
    df_filtrado = df_scores_sentencas[(df_scores_sentencas.indice_comentario.isin(df.index.tolist())) & (df_scores_sentencas.tam_sentenca > 4)]
    
    df_ordenado_por_score = df_filtrado.sort_values(by='score_positivo',ascending=False).head(n_top)
    html = ""
    for i in df_ordenado_por_score.index:
        indice = df_ordenado_por_score['indice_comentario'][i]
        sentenca = df_ordenado_por_score['sentenca'][i]
        atracao = df['atracao'][indice]
        cidade = df['cidade'][indice]
        estado = df['estado'][indice]

        html = html +"* *"+sentenca+"* "+" - **" +atracao+" em "+cidade+"/"+estado +"**\n"
    st.markdown(html)

def sentencas_mais_negativas_localidade(n_top):
    df_filtrado = df_scores_sentencas[(df_scores_sentencas.indice_comentario.isin(df.index.tolist())) & (df_scores_sentencas.tam_sentenca > 4)]
    
    df_ordenado_por_score = df_filtrado.sort_values(by='score_negativo',ascending=False).head(n_top)
    html = ""
    for i in df_ordenado_por_score.index:
        indice = df_ordenado_por_score['indice_comentario'][i]
        sentenca = df_ordenado_por_score['sentenca'][i]
        atracao = df['atracao'][indice]
        cidade = df['cidade'][indice]
        estado = df['estado'][indice]

        html = html + "* *"+sentenca+"* "+" - **" +atracao+" em "+cidade+"/"+estado +"**\n"
    st.markdown(html)

def sentencas_mais_negativas(n_top):
    df_filtrado = df_scores_sentencas[(df_scores_sentencas.indice_comentario.isin(df.index.tolist())) & (df_scores_sentencas.tam_sentenca > 4)]
    df_ordenado_por_score = df_filtrado.sort_values(by='score_negativo',ascending=False).head(n_top)
    html = ""
    for sentenca in df_ordenado_por_score['sentenca']:
        html = html + "* *"+sentenca+"*\n"
    st.markdown(html)

lista_estados = [
'Todos',    
'Acre',
'Alagoas',
'Amapa',
'Amazonas',
'Bahia',
'Ceara',
'Distrito Federal',
'Espirito Santo',
'Goias',
'Maranhao',
'Mato Grosso',
'Mato Grosso do Sul',
'Minas Gerais',
'Para',
'Paraiba',
'Parana',
'Pernambuco',
'Piaui',
'Rio de Janeiro',
'Rio Grande do Norte',
'Rio Grande do Sul',
'Rondonia',
'Roraima',
'Santa Catarina',
'Sao Paulo',
'Sergipe',
'Tocantins']

st.sidebar.info("Bem-vindos a *Brazil Turism Dashboard (BTD)* - Uma *dashboard* interativa sobre comentários de atrações turísticas do Brasil")
page = st.sidebar.selectbox(
    "Selecione o tipo de visualização",
    ("Por Localidade", "Por atração turística")
)
st.sidebar.image('images/logo-app.jpg')




if page == 'Por Localidade':
    option = st.selectbox('Selecione o Estado', lista_estados)

    LATITUDE_INICIAL = -15.788497
    LONGITUDE_INICIAL = -47.879873

    if option == 'Todos':
        df = df_todos
    else:
        df = df_todos[df_todos['estado'] == option]
       
    if (len(df)>0):
            
        st.write('')
        row1_space1, row1_1, row1_space2, row1_2, row1_space3,row1_3, row1_space4 = st.columns((.1, 1, .1, 1, .1, 1, .1))
        with row1_1:
            TOTAL_COMENTS = len(df)
            row1_1.metric(label ='Total de comentários',value = TOTAL_COMENTS,
                        delta=porcentagem_total_comentarios(TOTAL_COMENTS), delta_color="off")
        with row1_2:
            TOTAL_USUARIOS = len(pd.DataFrame(df['usuario'].dropna().value_counts()))
            row1_2.metric(label ='Total de usuários',value = TOTAL_USUARIOS,
                        delta=porcentagem_total_usuarios(TOTAL_USUARIOS), delta_color="off")
        with row1_3:
            TOTAL_ATRACOES = len(pd.DataFrame(df['atracao'].dropna().value_counts()))
            row1_3.metric(label ='Total de atrações',value = TOTAL_ATRACOES,
                        delta=porcentagem_total_atracoes(TOTAL_ATRACOES), delta_color="off")
        
        st.write('')
        row0_space1, row0_1, row0_space2, row0_2, row0_space3,row0_3, row0_space4 = st.columns((.1, 1, .1, 1, .1, 1, .1))
        with row0_1:
            TOTAL_CIDADES = len(pd.DataFrame(df['cidade'].dropna().value_counts())) 
            row0_1.metric(label ='Total de cidades comentadas',value = TOTAL_CIDADES,
                        delta=porcentagem_total_cidades(TOTAL_CIDADES), delta_color="off")    
        with row0_2:
            MES_MAIS_VISITADO = mes_mais_visitado()
            row0_2.metric(label ='Mês mais visitado',value = MES_MAIS_VISITADO)
        with row0_3:
            ANO_MAIS_VISITADO = ano_mais_visitado()
            row0_3.metric(label ='Ano mais visitado',value = ANO_MAIS_VISITADO)
            
        st.write('')
        row2_space1,row2_1, row2_space2, row2_2, row2_space3, row2_3, row2_space4 = st.columns((.1, 1, .1, 1, .1, 1, .1))    
            
        with row2_1:
            media_caracteres = media_qtde_caracteres(df)
            row2_1.metric(label ='Média de caracteres por comentário',value = media_caracteres, delta=porcentagem_caracter(media_caracteres) )
        with row2_2:
            media_token = media_qtde_token(df)
            row2_2.metric(label ='Média de tokens por comentário',value = media_token, delta=porcentagem_token(media_token))    
        with row2_3:
            media_nota = round(df['rating'].mean(),2)
            row2_3.metric(label ='Média das Notas',value = media_nota, delta=porcentagem_nota(media_nota))          
        if option != 'Todos':           
            st.write('*Observação: As porcentagens apresentadas são em comparação ao Brasil*')
        
        st.write('')    
        row000_1, espaco = st.columns(( 1, .1))
        with row000_1:
            local = option
            if (option == 'Todos'):
                local = 'Brasil'                    
            st.write('#### Veja o que falam de mais positivo sobre as atrações do ',local)
            top_number = st.number_input('Digite a quantidade de frases desejada', min_value=1, max_value=30, value=5, key=5)
            sentencas_mais_positivas_localidade(top_number)
        
        st.write('')    
        row000_2, espaco = st.columns(( 1, .1))
        with row000_2:
            local = option
            if (option == 'Todos'):
                local = 'Brasil'                    
            st.write('#### Veja o que falam de mais negativo sobre as atrações do ',local)
            top_number = st.number_input('Digite a quantidade de frases desejada', min_value=1, max_value=30, value=5, key=6)
            sentencas_mais_negativas_localidade(top_number)    
        
        st.write('')    
        row00_1, espaco = st.columns(( 1, .1))
        with row00_1:
            st.write('#### O gráfico a seguir mostra a distribuição dos comentários entre os gêneros dos usuários.')
            genero_user = df.groupby(['genero_usuario']).count().reset_index()
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            ax.pie(genero_user['usuario'],labels=genero_user['genero_usuario'], autopct='%1.2f%%',startangle=90)
            ax.legend(genero_user['genero_usuario'],bbox_to_anchor=(0.8,1))
            ax.axis('equal')
            st.pyplot(fig)
            
        st.write('')    
        row3_1, espaco = st.columns(( 1, .1))

        with row3_1:
            if option == 'Todos':
                st.write('#### O gráfico a seguir mostra a distribuição dos comentários entre as unidades federativas do Brasil. ')
                notas_df = pd.DataFrame(df['estado'].dropna().value_counts()).reset_index()
                notas_df.columns = ['estado', 'qtde_comentarios']
                notas_df = notas_df.sort_values(by='qtde_comentarios')
                chart = alt.Chart(notas_df, width=700, title="Estado x Total de Comentários").mark_bar().encode(
                    x=alt.X(shorthand="qtde_comentarios", title="Total de comentários"),
                    y=alt.Y(shorthand="estado", title="Estado", sort='-x'),
                    opacity=alt.value(1),
                color=alt.condition(
                    alt.datum.estado == notas_df['estado'][0],  # If it's the top ranked prediction
                        alt.value('#f63366'),     #  sets the bar to the streamlit pink.
                        alt.value('grey')  ) # else this colour
                )
                text = chart.mark_text(
                    align='left',
                    baseline='middle',
                    dx=3  # Nudges text to right so it doesn't appear on top of the bar
                ).encode(
                    text=alt.Text('qtde_comentarios')
                )
                st.altair_chart(chart+text)
            else:
                st.write(f'#### O gráfico a seguir mostra a distribuição dos comentários entre as cidades do ',option,'.')
                notas_df = pd.DataFrame(df['cidade'].dropna().value_counts()).reset_index()
                notas_df.columns = ['cidade', 'qtde_comentarios']
                notas_df = notas_df.sort_values(by='qtde_comentarios')
                chart = alt.Chart(data=notas_df, width=700, title="Cidade x Total de Comentários").mark_bar().encode(
                    x=alt.X(shorthand="qtde_comentarios", title="Total de comentários"),
                    y=alt.Y(shorthand="cidade", title="Cidade", sort='-x'),
                    opacity=alt.value(1),
                color=alt.condition(
                    alt.datum.cidade == notas_df['cidade'][0],  # If it's the top ranked prediction
                        alt.value('#f63366'),     #  sets the bar to the streamlit pink.
                        alt.value('grey')  ) # else this colour
                )
                
                text = chart.mark_text(
                    align='left',
                    baseline='middle',
                    dx=3  # Nudges text to right so it doesn't appear on top of the bar
                ).encode(
                    text=alt.Text('qtde_comentarios')
                )
                
                st.altair_chart(chart+text)  
        st.write('')    
        row2_1, row2_space1 = st.columns((1, .1))
        with row2_1:
            if option == 'Todos':
                df_temp2 = df[['estado','rating']]
                #df_temp2['atracao_cidade'] =  df_temp2['atracao'] + '(' + df_temp2['cidade'] + ')'
                grouped = df_temp2[['rating']].groupby(by=[df_temp2['estado']])
                grouped_medio = grouped.mean().sort_values(by='rating',ascending=False).reset_index()
                grouped_medio.columns = ['estado', 'rating_medio']
                st.write('#### O gráfico a seguir mostra a média das notas dos usuários entre os estados comentados.')        
                chart = alt.Chart(grouped_medio, width=700, title="Estado x Média das Notas").mark_bar().encode(
                    x=alt.X(shorthand="rating_medio", title="Média das Notas"),
                    y=alt.Y(shorthand='estado',title='Estado', sort='-x'),
                    opacity=alt.value(1),
                color=alt.condition(
                    alt.datum.estado == grouped_medio['estado'][0],  # If it's the top ranked prediction
                        alt.value('#f63366'),     #  sets the bar to the streamlit pink.
                        alt.value('grey')  ) # else this colour
                )
                
                text = chart.mark_text(
                    align='left',
                    baseline='middle',
                    dx=3  # Nudges text to right so it doesn't appear on top of the bar
                ).encode(
                    text=alt.Text('rating_medio', format=',.2r')
                )
                        
                st.altair_chart(chart+text)
            else:
                df_temp2 = df[['cidade','rating']]
                #df_temp2['atracao_cidade'] =  df_temp2['atracao'] + '(' + df_temp2['cidade'] + ')'
                grouped = df_temp2[['rating']].groupby(by=[df_temp2['cidade']])
                grouped_medio = grouped.mean().sort_values(by='rating',ascending=False).reset_index()
                grouped_medio.columns = ['cidade', 'rating_medio']
                st.write(f'#### O gráfico a seguir mostra a média das notas dos usuários entre as cidades comentadas do ',option,'.')    
                chart = alt.Chart(grouped_medio, width=700, title="Cidade x Média das Notas").mark_bar().encode(
                    x=alt.X(shorthand="rating_medio", title="Média das Notas"),
                    y=alt.Y(shorthand='cidade',title='Cidade', sort='-x'),
                    opacity=alt.value(1),
                color=alt.condition(
                    alt.datum.cidade == grouped_medio['cidade'][0],  # If it's the top ranked prediction
                        alt.value('#f63366'),     #  sets the bar to the streamlit pink.
                        alt.value('grey')  ) # else this colour
                )
                
                text = chart.mark_text(
                    align='left',
                    baseline='middle',
                    dx=3  # Nudges text to right so it doesn't appear on top of the bar
                ).encode(
                    text=alt.Text('rating_medio', format=',.2r')
                )
                        
                st.altair_chart(chart+text)
            
        
        st.write('')
        rowx_1, rowx_space2 = st.columns((1, .1))

        with rowx_1:
            df_temp = df[['atracao','cidade']]
            atracao_df = df_temp.groupby(['atracao', 'cidade']).agg({'atracao':['count']}).sort_index().reset_index()
            atracao_df.columns = ['atracao', 'cidade' ,'qtde_comentarios']
            atracao_df['atracao_cidade'] =  atracao_df['atracao'] + '(' + atracao_df['cidade'] + ')'
            atracao_df = atracao_df.sort_values('qtde_comentarios', ascending=False).reset_index()
            
            if (len(atracao_df) > 10):
                top_number = 10
            else:
                top_number = len(atracao_df)
                
            st.write(f'#### O gráfico a seguir mostra o Top {top_number} das atrações mais comentadas.')    
            msg_top = 'Top '+ str(top_number)+ ' das atrações mais comentadas'
            chart = alt.Chart(atracao_df[:top_number], width=700, title=msg_top).mark_bar().encode(
                x=alt.X(shorthand="qtde_comentarios", title="Total de comentários"),
                y=alt.Y(shorthand='atracao_cidade',title='Atração', sort='-x'),
                opacity=alt.value(1),
            color=alt.condition(
                alt.datum.atracao_cidade == atracao_df['atracao_cidade'][0],  # If it's the top ranked prediction
                    alt.value('#f63366'),     #  sets the bar to the streamlit pink.
                    alt.value('grey')  ) # else this colour
            )
            
            text = chart.mark_text(
                align='left',
                baseline='middle',
                dx=3  # Nudges text to right so it doesn't appear on top of the bar
            ).encode(
                text=alt.Text('qtde_comentarios')
            )
            
            st.altair_chart(chart+text)  
            
        rowx_2, rowx_space3 = st.columns((1, .1))         
        with rowx_2:
            df_temp2 = df[['atracao','cidade','rating']]
            #df_temp2['atracao_cidade'] =  df_temp2['atracao'] + '(' + df_temp2['cidade'] + ')'
            grouped = df_temp2[['rating']].groupby(by=[df_temp2['atracao'],df_temp2['cidade']])
            grouped_medio = grouped.mean().sort_values(by='rating',ascending=False).reset_index()
            grouped_medio.columns = ['atracao', 'cidade', 'rating_medio']
            grouped_medio['atracao_cidade'] = grouped_medio['atracao']+' (' +grouped_medio['cidade']+ ')'
            #st.write(grouped_medio)
            if (len(grouped_medio) > 10):
                top_number = 10
            else:
                top_number = len(grouped_medio)
            st.write(f'#### O gráfico a seguir mostra o Top {top_number} das atrações mais bem avaliadas.')     
            msg_top = 'Top '+ str(top_number)+ ' das atrações mais bem avaliadas'
            chart = alt.Chart(grouped_medio[:top_number], width=700, title=msg_top).mark_bar().encode(
                x=alt.X(shorthand="rating_medio", title="Média das Notas"),
                y=alt.Y(shorthand='atracao_cidade',title='Atração', sort='-x'),
                opacity=alt.value(1),
            color=alt.condition(
                alt.datum.atracao_cidade == grouped_medio['atracao_cidade'][0],  # If it's the top ranked prediction
                    alt.value('#f63366'),     #  sets the bar to the streamlit pink.
                    alt.value('grey')  ) # else this colour
            )
            
            text = chart.mark_text(
                align='left',
                baseline='middle',
                dx=3  # Nudges text to right so it doesn't appear on top of the bar
            ).encode(
                text=alt.Text('rating_medio', format=',.2r')
            )
                    
            st.altair_chart(chart+text)
            
        st.write('')
        row4_1, row4_space2  = st.columns((1, .1))
        with row4_1:        
            st.write('#### O gráfico a seguir mostra a distribuição dos comentários entre os anos.') 
            ano_df = pd.DataFrame(df['ano_data'].dropna().value_counts()).reset_index()
            ano_df = ano_df.sort_values(by='index')
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=ano_df['index'],y=ano_df['ano_data'], color='blue', ax=ax)
            ax.set_xlabel('Ano')
            ax.set_ylabel('Total de Comentários')
            ax.set_title('Distribuição dos comentários através dos anos')
            st.pyplot(fig)
        
        st.write('')
        row4_2, row4_space3  = st.columns((1, .1))    
        with row4_2:
            st.write('#### O gráfico a seguir mostra a distribuição dos comentários entre os meses de janeiro a dezembro.')
            mes_df = pd.DataFrame(df['mes_data'].dropna().value_counts()).reset_index()
            mes_df = mes_df.sort_values(by='index')
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=mes_df['index'],y=mes_df['mes_data'], color='blue', ax=ax)
            ax.set_xlabel('Mês')
            ax.set_ylabel('Total de Comentários')
            ax.set_title('Distribuição dos comentários através dos meses')
            st.pyplot(fig)
            
        st.write('')
        row4_3, row3_space3  = st.columns((1, .1))     
        with row4_3:
            st.write('#### O gráfico a seguir mostra a distribuição dos comentários através das notas')
            notas_df = pd.DataFrame(df['rating'].dropna().value_counts()).reset_index()
            notas_df = notas_df.sort_values(by='index')
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=notas_df['index'],y=notas_df['rating'], color='goldenrod', ax=ax)
            ax.set_xlabel('Nota')
            ax.set_ylabel('Total de Comentários')
            ax.set_title('Distribuição dos comentários através das notas')
            st.pyplot(fig)    
        
        st.write('')
        rowwces_2, rowwces_space2 = st.columns((1, .1))
        
        with rowwces_2:
            st.subheader('Nuvem de Entidades')
            wc = wordCloudEntidades(df)
            if (wc == -1):
                st.markdown('*Não há entidades!*')
            else:        
                fig = plt.figure(figsize=(8,8))
                plt.imshow(wc,interpolation="bilinear")
                plt.axis('off')
                plt.tight_layout()
                st.pyplot(fig)         
        
        
        st.write('')
        row5_2, row5_space2 = st.columns((1, .1))
        
        with row5_2:
            st.subheader('Nuvem de palavras')
            nome_arquivo = option
            nome_arquivo = nome_arquivo.replace(" ", "_")
            nome_arquivo = nome_arquivo.lower()
            caminho_arquivo = "images/nuvem_palavras_" + nome_arquivo + ".png"
            st.image(caminho_arquivo)         
             
        
        st.write('')
        row6_2, row6_space2 = st.columns((1, .1))   
        
        with row6_2:
            st.subheader('Substantivos mais comuns')
            top_number = st.number_input('Digite a quantidade de substantivos desejada', min_value=1, max_value=30, value=10)
            lista_verbos = list(chain(*df['lista_substantivos'])) 
            counter=collections.Counter(lista_verbos)
            top_verbos = pd.DataFrame(counter.most_common(top_number))
            top_verbos.columns = ['substantivo', 'frequencia']
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=top_verbos['frequencia'],y=top_verbos['substantivo'], color='pink', ax=ax)
            ax.set_xlabel('Frequência')
            ax.set_ylabel('Substantivo')
            st.pyplot(fig)  
            
        st.write('')
        row7_2, row7_space2 = st.columns((1, .1))   
        
        with row7_2:
            st.subheader('Adjetivos mais comuns')
            top_number = st.number_input('Digite a quantidade de adjetivos desejada', min_value=1, max_value=30, value=10)
            lista_verbos = list(chain(*df['lista_adjetivos'])) 
            counter=collections.Counter(lista_verbos)
            top_verbos = pd.DataFrame(counter.most_common(top_number))
            top_verbos.columns = ['adjetivo', 'frequencia']
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=top_verbos['frequencia'],y=top_verbos['adjetivo'], color='green', ax=ax)
            ax.set_xlabel('Frequência')
            ax.set_ylabel('Adjetivo')
            st.pyplot(fig)       
        
        st.write('')
        row8_2, row8_space2 = st.columns((1, .1))
            
        with row8_2:
            st.subheader('Verbos mais comuns')
            top_number = st.number_input('Digite a quantidade de verbos desejada',  min_value=1, max_value=30, value=10)
            lista_verbos = list(chain(*df['lista_verbos'])) 
            counter=collections.Counter(lista_verbos)
            top_verbos = pd.DataFrame(counter.most_common(top_number))
            top_verbos.columns = ['verbo', 'frequencia']
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=top_verbos['frequencia'],y=top_verbos['verbo'], color='goldenrod', ax=ax)
            ax.set_xlabel('Frequência')
            ax.set_ylabel('Verbo')
            st.pyplot(fig)  
            
        st.write('')
        row5_1, row5_space1 = st.columns((1, .1))
        with row5_1:
            st.subheader('Mapa de calor dos comentários entre as cidades')
            coordenadas=[]
            for lat,lng in zip(df.latitude_cidade.values,df.longitude_cidade.values):
                coordenadas.append([lat,lng])
               
            mapa_calor = folium.Map(location=[LATITUDE_INICIAL, LONGITUDE_INICIAL],zoom_start=4,tiles='Stamen Toner')
               
            # Adicionando os registros no mapa de calor:
            mapa_calor.add_child(plugins.HeatMap(coordenadas))        
            folium_static(mapa_calor)

    else:
        st.markdown('Infelizmente, não há comentários de atrações turíscas para o estado selecionado.')        
else:
        atracoes_df = load_nomes_atracoes()
        atracao = st.selectbox('Selecione atração',list(atracoes_df['atracao'])) 
        df = df_todos[df_todos['atracao'] == atracao]
        st.write('')
        rowatracao1_1, rowatracao1_space1 = st.columns((1, .1))
        with rowatracao1_1:
            localizacao = df['cidade'].iloc[0] + " - " + df['estado'].iloc[0]
            rowatracao1_1.metric(label ='Localização',value = localizacao)
            
        st.write('')
        row1_1, row1_space1, row1_2, row1_space2, row1_3, row1_space3 = st.columns((1, .1, 1, .1, 1, .1))
        with row1_1:
            TOTAL_COMENTS = len(df)
            row1_1.metric(label ='Total de comentários',value = TOTAL_COMENTS)
        with row1_2:
            TOTAL_USUARIOS = len(pd.DataFrame(df['usuario'].dropna().value_counts()))
            row1_2.metric(label ='Total de usuários',value = TOTAL_USUARIOS)
        with row1_3:
            MES_MAIS_VISITADO = mes_mais_visitado()
            row1_3.metric(label ='Mês mais visitado',value = MES_MAIS_VISITADO)
                
        st.write('')
        row2_1, row2_space1, row2_2, row2_space2, row2_3, row2_space3 = st.columns((1, .1, 1, .1, 1, .1))
        with row2_1:
            ANO_MAIS_VISITADO = ano_mais_visitado()
            row2_1.metric(label ='Ano mais visitado',value = ANO_MAIS_VISITADO)
        with row2_2:
            media_caracteres = media_qtde_caracteres(df)
            row2_2.metric(label ='Média de caracteres por comentário',value = media_caracteres)
        with row2_3:
            media_token = media_qtde_token(df)
            row2_3.metric(label ='Média de tokens por comentário',value = media_token)    
                
        st.write('')
        row4x_1, row4_space1  = st.columns((1, .1))    
        with row4x_1:
            row4x_1.metric(label ='Média das Notas',value = round(df['rating'].mean(),2))
        
        st.write('')    
        rowcp_1, espaco = st.columns(( 1, .1))
        with rowcp_1:
            st.write('#### Veja o que falam de mais positivo sobre essa atração.')
            top_number = st.number_input('Digite a quantidade de frases desejada', min_value=1, max_value=30, value=5, key=3)
            sentencas_mais_positivas(top_number)
        
        st.write('')    
        rowcn_2, espaco = st.columns(( 1, .1))
        with rowcn_2:
            st.write('#### Veja o que falam de mais negativo sobre essa atração.')
            top_number = st.number_input('Digite a quantidade de frases desejada', min_value=1, max_value=30, value=5, key=4)
            sentencas_mais_negativas(top_number)
         
              
        st.write('')    
        row00x_1, espaco = st.columns(( 1, .1))
        with row00x_1:
            st.write('#### O gráfico a seguir mostra a distribuição dos comentários entre os gêneros dos usuários.')
            genero_user = df.groupby(['genero_usuario']).count().reset_index()
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            ax.pie(genero_user['usuario'],labels=genero_user['genero_usuario'], autopct='%1.2f%%',startangle=90)
            ax.legend(genero_user['genero_usuario'],bbox_to_anchor=(0.8,1))
            ax.axis('equal')
            st.pyplot(fig)    
                
        st.write('')
        row4_1, row4_space2  = st.columns((1, .1))
        with row4_1:        
            st.write('#### O gráfico a seguir mostra a distribuição dos comentários sobre a atração através dos anos.') 
            ano_df = pd.DataFrame(df['ano_data'].dropna().value_counts()).reset_index()
            ano_df = ano_df.sort_values(by='index')
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=ano_df['index'],y=ano_df['ano_data'], color='blue', ax=ax)
            ax.set_xlabel('Ano')
            ax.set_ylabel('Total de Comentários')
            ax.set_title('Distribuição dos comentários através dos anos')
            st.pyplot(fig)
                
        st.write('')
        row4_2, row4_space3  = st.columns((1, .1))    
        with row4_2:
            st.write('#### O gráfico a seguir mostra a distribuição dos comentários entre os meses de janeiro a dezembro.')
            mes_df = pd.DataFrame(df['mes_data'].dropna().value_counts()).reset_index()
            mes_df = mes_df.sort_values(by='index')
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=mes_df['index'],y=mes_df['mes_data'], color='blue', ax=ax)
            ax.set_xlabel('Mês')
            ax.set_ylabel('Total de Comentários')
            ax.set_title('Distribuição dos comentários através dos meses')
            st.pyplot(fig)
                    
        st.write('')
        row4_3, row3_space3  = st.columns((1, .1))     
        with row4_3:
            st.write('#### O gráfico a seguir mostra a distribuição dos comentários através das notas')
            notas_df = pd.DataFrame(df['rating'].dropna().value_counts()).reset_index()
            notas_df = notas_df.sort_values(by='index')
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=notas_df['index'],y=notas_df['rating'], color='goldenrod', ax=ax)
            ax.set_xlabel('Nota')
            ax.set_ylabel('Total de Comentários')
            ax.set_title('Distribuição dos comentários através das notas')
            st.pyplot(fig)    
        
        st.write('')
        rowwce, rowwce_space = st.columns((1, .1))
        with rowwce:
            st.subheader('Nuvem de Entidades')
            wc = wordCloudEntidades(df)
            fig = plt.figure(figsize=(8,8))
            plt.imshow(wc,interpolation="bilinear")
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig)
        
        
        st.write('')
        rowwc, rowwc_space = st.columns((1, .1))
        with rowwc:
            st.subheader('Nuvem de Palavras')
            wc = wordCloud(df)
            fig = plt.figure(figsize=(8,8))
            plt.imshow(wc,interpolation="bilinear")
            plt.axis('off')
            plt.title(atracao,fontsize=18)
            plt.tight_layout()
            st.pyplot(fig)
        
        st.write('')
        row6_2, row6_space2 = st.columns((1, .1))   
        
        with row6_2:
            st.subheader('Substantivos mais comuns')
            top_number = st.number_input('Digite a quantidade de substantivos desejada', min_value=1, max_value=30, value=10)
            lista_verbos = list(chain(*df['lista_substantivos'])) 
            counter=collections.Counter(lista_verbos)
            top_verbos = pd.DataFrame(counter.most_common(top_number))
            top_verbos.columns = ['substantivo', 'frequencia']
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=top_verbos['frequencia'],y=top_verbos['substantivo'], color='pink', ax=ax)
            ax.set_xlabel('Frequência')
            ax.set_ylabel('Substantivo')
            st.pyplot(fig)        
                
        st.write('')
        row7_2, row7_space2 = st.columns((1, .1))   
            
        with row7_2:
            st.subheader('Adjetivos mais comuns')
            top_number = st.number_input('Digite a quantidade de adjetivos desejada',  min_value=1, max_value=30, value=10)
            lista_verbos = list(chain(*df['lista_adjetivos'])) 
            counter=collections.Counter(lista_verbos)
            top_verbos = pd.DataFrame(counter.most_common(top_number))
            top_verbos.columns = ['adjetivo', 'frequencia']
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=top_verbos['frequencia'],y=top_verbos['adjetivo'], color='green', ax=ax)
            ax.set_xlabel('Frequência')
            ax.set_ylabel('Adjetivo')
            st.pyplot(fig)       
            
        st.write('')
        row8_2, row8_space2 = st.columns((1, .1))
                
        with row8_2:
            st.subheader('Verbos mais comuns')
            top_number = st.number_input('Digite a quantidade de verbos desejada',  min_value=1, max_value=30, value=10)
            lista_verbos = list(chain(*df['lista_verbos'])) 
            counter=collections.Counter(lista_verbos)
            top_verbos = pd.DataFrame(counter.most_common(top_number))
            top_verbos.columns = ['verbo', 'frequencia']
            fig = Figure(figsize=(8,4))
            ax = fig.subplots()
            sns.barplot(x=top_verbos['frequencia'],y=top_verbos['verbo'], color='goldenrod', ax=ax)
            ax.set_xlabel('Frequência')
            ax.set_ylabel('Verbo')
            st.pyplot(fig)    
            