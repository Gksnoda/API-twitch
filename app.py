import streamlit as st
import pandas as pd
import time
from DAO import *
from model import *
import pdfkit as pdf

# Função para gerar o relatório a partir dos critérios selecionados
def generateReport():
    if not report_fields:
        return -1
    
    if st.session_state.filters == "":
        st.session_state.filters = None
    
    session = DAO.getSession()
    session.expire_on_commit = False

    if report_type == 'Videos':
        query = DAORelatorioVideos.select(session, st.session_state.filters, st.session_state.ordernation, report_fields)
    if report_type == 'Streams':
        query = DAORelatorioStreams.select(session, st.session_state.filters, st.session_state.ordernation, report_fields)
    if report_type == 'Canais':
        query = DAORelatorioCanais.select(session, st.session_state.filters, st.session_state.ordernation, report_fields)
    if report_type == 'Usuários':
        query = DAORelatorioUsuarios.select(session, st.session_state.filters, st.session_state.ordernation, report_fields)
    if report_type == 'Categorias':
        query = DAORelatorioCategories.select(session, st.session_state.filters, st.session_state.ordernation, report_fields)

    connection = session.connection()
    df = pd.read_sql_query(query.statement, con = connection)
    session.commit()
    session.close()

    st.session_state.dataframe = df

    # Convertendo o dataframe do relatorio para excel e html
    df.to_excel("DB/relatorio.xlsx", index=False)
    df.to_html('DB/relatorio.html', index=False)

# Função para limpar o campo do input do valor do filtro
def clear_form():        
    st.session_state["bar"] = ""

# ======================================
# Session_states
def set_filters_columns_count():
    st.session_state.filters = ""
    st.session_state.query = False
    st.session_state.countFilters = 0

def set_ordernation():
    st.session_state.ordernation = True
# ======================================

# Converter o relatório para pdf
def df_to_pdf():
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdf.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    pdf.from_file('DB/relatorio.html', 'relatorio.pdf', configuration=config)

#Configurações da página, aqui está sendo mostrado o título da página (na aba do navegador)
st.set_page_config(page_title="Relatório Twitch API")

# Estilização da página
app_style = """
    <style>
        /* Corpo principal da página*/
            [data-testid="stAppViewContainer"] {
                width: 100%;
                /* background: linear-gradient(to bottom left, #6441a5 70%, #ff3e5f); */
                background: linear-gradient(141deg, #ff3e5f 0%, #6441a5 51%, #6441a5 75%);
                color: white;
                font-family: Arial, sans-serif;
            }

            /* Título da página */
            [data-testid="StyledLinkIconContainer"]  {
                text-align: center !important;
                font-size: 40px;
                color: white !important;
                margin-top: -50px;
                margin-bottom: 20px;
            }

            /* Textos da página principal */ 
            [data-testid="stAppViewContainer"] p {
                font-size: 17.2px;
                color: white;
                margin-top: 5px;
            }

            /* Formulário para adicionar filtros */ 
            [data-testid="stForm"]{
                margin-top: -15px;
                margin-bottom: 15px;
                border: 2px solid;
            }

            /* Botão para escolher o campo sobre o qual ordenar*/
            [data-testid="stForm"] .st-aw{
                width: 210px;
            }

            /* Botão para ordenar*/
            .e10yg2by2{
                text-align: center;
                align-content: center;
            }

            /* Botões de select */ 
            .st-av {
                background-color: #9146ff;
                border-color: white;
                color: white;
                font-size: 20px;
            }

            /* Campo de texto */ 
            .st-ci {
                background-color: #9146ff;
                font-size: 20px;
            }

            /* Filtros adicionados */
            [data-testid="stExpander"]{
                margin-top: -15px;
                margin-bottom: 15px;
                border: 2px solid;
            }

            /* Radio button de ordenação */
            .st-ef {
                margin-bottom: 0px;
            }            

            /* Botão para gerar o relatório*/
            .e1f1d6gn3{
                text-align: center;
                align-content: center;
            }

        /* Barra lateral*/
            [data-testid="stSidebar"] {
                background-color: #9146ff;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-decoration: none;
                font-size: 30px;
                text-shadow: 2px 2px 2px black;
                text-align: center;
            }
            [data-testid="stSidebar"] img {
                margin-top: -20px;
                margin-bottom: 30px;
            }
            /* .e115fcil2 */

            [data-testid="stSidebar"] h2 {
                font-size: 30px;
                color: white;
                margin-top: -40px;
            }
            [data-testid="stSidebar"] * {
                align-items: center;
                font-size: 20px;
                font-weight: bold;
                color: white;
            }

            [data-testid="stSidebar"] p {
                margin-bottom: 20px;
            }

            [data-testid="stSidebar"] hr {
                margin-top: 2px;
                margin-bottom: 5px;
            }
    </style>
    """
st.markdown(app_style, unsafe_allow_html=True) 

# Barra lateral
st.sidebar.header("Twitch API")
st.sidebar.image('./img/twitch.png')
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.header("Desenvolvido por:")
st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
st.sidebar.write("Guilherme Ribeiro")
st.sidebar.write("Tales Oliveira")
st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
#st.sidebar.image('./img/streamlit.png', width=35);

#titulo
st.title('Relatórios Twitch API')
st.write('\n')

#sessions states
if 'controller' not in st.session_state:
    st.session_state.controller = 0

if 'dataframe' not in st.session_state:
    st.session_state.dataframe = False

if 'df' not in st.session_state:
    st.session_state.df = False

if 'filters' not in st.session_state:
    st.session_state.filters = ""

if 'countFilters' not in st.session_state:
    st.session_state.countFilters = 0

if 'ordernation' not in st.session_state:
    st.session_state.ordernation = None

if 'query' not in st.session_state:
    st.session_state.query = False

if 'report' not in st.session_state:
    st.session_state.report = False

if 'dataPdf' not in st.session_state:
    st.session_state.dataPdf = None

if 'dataXlsx' not in st.session_state:
    st.session_state.dataXlsx = None

# Para gerar o relatório
if st.session_state.controller == 0:
    f1, f2 = st.columns([1, 1])

    with f1:
        report_type = st.selectbox(
        'Selecione a tabela para gerar o relatório:',
        ('Videos', 'Streams', 'Canais', 'Usuários', 'Categorias'), on_change=set_filters_columns_count)

    session = DAO.getSession()
    session.expire_on_commit = False

    if st.session_state.query is False:
        if report_type == 'Videos':
            query = DAORelatorioVideos.select(session, None, None, None)    
        elif report_type == 'Streams':
            query = DAORelatorioStreams.select(session, None, None, None)
        elif report_type == 'Canais':
            query = DAORelatorioCanais.select(session, None, None, None)
        elif report_type == 'Usuários':
            query = DAORelatorioUsuarios.select(session, None, None, None)
        elif report_type == 'Categorias':
            query = DAORelatorioCategories.select(session, None, None, None)

        st.session_state.df = pd.read_sql_query(query.statement, con=session.bind)
        session.commit()
        session.close()
    st.session_state.query = True

    with f2:
        report_fields = st.multiselect(f'Selecione os campos do relatório de {report_type}:', options = st.session_state.df.columns, placeholder = 'Selecionar campo')
    
    # Formulário dos filtros
    st.write('\n')
    st.write("Filtrar por campos:")
    with st.form("myform"):
        f1, f2, f3 = st.columns([1, 1, 1])
        with f1:
            field = st.selectbox("Campo:", options = st.session_state.df.columns)
        with f2:
            comparison = st.selectbox("Comparação:", options = ('igual', 'maior', 'menor', 'maior ou igual', 'menor ou igual', 'diferente de', 'contendo a string'))
        with f3:
            comparison_value = st.text_input("Valor")

        f1, f2, f3 = st.columns([1, 1, 1])
        
        with f2:
            st.write('\n')
            submit = st.form_submit_button(label="Adicionar filtro", on_click=clear_form)

    # Tipo de comparação a ser feita
    if submit and comparison_value:
        map_operation = {
            'igual': f'= ',
            'maior': f'> ',
            'menor': f'< ',
            'maior ou igual': f'>= ',
            'menor ou igual': f'<= ',
            'diferente de': f'!= ',
            'contendo a string': 'LIKE \'%'
        }

        operation = map_operation[comparison]
            
        if st.session_state.df[f'{field}'].dtypes == 'object' and not comparison == 'contendo a string':
            value = f"'{comparison_value}'"
        elif comparison == 'contendo a string':
            value = f"{comparison_value}"
        else:
            value = f'{comparison_value}'

        # Adiciona os filtros
        if st.session_state.countFilters == 0:
            st.session_state.filters += f"{field} {operation}{value}"
        else:
            st.session_state.filters += f" AND {field} {operation}{value}"

        # Caso a opçãp "contendo a string" seja utilizada, precisamos adicionar o % no final para realizar a consulta
        if comparison == 'contendo a string':
            st.session_state.filters += '%\''

        st.session_state.countFilters = 1
        container = st.empty()
        container.success('Filtro adicionado com sucesso!') 
        time.sleep(3) 
        container.empty() 

    if submit and not comparison_value: 
        container = st.empty()
        container.error('Preencha o valor da comparação!') 
        time.sleep(3) 
        container.empty() 

    st.write('\n\n\n\n\n\n')
    st.write('Filtros adicionados:')
    with st.expander(" "):
        st.write(st.session_state.filters)


    # Formulário de ordenação do relatório
    st.write('\n')
    st.write("Ordenar relatório:")
    with st.form("myform2"):
        o1, o2 = st.columns([1.5, 1.5])
        with o1:
            ordernation_field = st.selectbox('Ordenar por:', options = st.session_state.df.columns)
        with o2:
            ordernation_type = st.radio(f'Campo {ordernation_field} ordenado de modo:', options = ('Crescente', 'Decrescente'), horizontal = True)
        
        st.write('\n\n\n\n\n')
        o1, o2 = st.columns([1, 1])
        
        st.write('\n')
        ordernation_report = st.form_submit_button(label='Ordenar relatório', on_click=set_ordernation)

    if ordernation_report == 'Crescente':
        ordernation = 'ASC'
    else:
        ordernation = 'DESC'
        
    if ordernation_report:
        st.session_state.ordernation = f'{ordernation_field} {ordernation}'
        container = st.empty()
        container.success(f'Relatório será ordenado pelo campo {ordernation_field} de forma {ordernation_type}!') 
        time.sleep(3) 
        container.empty() 

    st.write('\n\n\n')
    f1, f2, f3 = st.columns([1, 1, 1])

    with f2:
        st.write('\n\n\n\n\n')
        report = st.button('Gerar relatório')

    st.write('\n\n\n\n\n')

    if report:
        status = generateReport()
        if status == -1:
            st.error("Selecione os campos do relatório!")
        else:
            st.session_state.controller = 1
            st.experimental_rerun()

# Página do relatório
else:
    if st.session_state.report == False:

        #gera o relatório para pdf
        df_to_pdf()

        with open("relatorio.pdf", "rb") as pdf_file:
            st.session_state.pdfData  = pdf_file.read()

        with open("DB/relatorio.xlsx", "rb") as xlsx_file:
            st.session_state.xlsxData = xlsx_file.read()

    st.session_state.report = st.dataframe(st.session_state.dataframe, width=1000, height=500)

    f1, f2, f3 = st.columns([1, 1, 1])

    st.write('\n')
    st.write('\n')

    with f1:
        report_pdf = st.download_button('Exportar relátorio para PDF!', data = st.session_state.pdfData,
        file_name="relatorio.pdf")

    with f2:
        report_xlsx= st.download_button('Exportar relátorio para XLSX!', data = st.session_state.xlsxData,
        file_name="relatorio.xlsx")

    with f3:
        new_reports = st.button("Criar mais relatórios!")
    
    if new_reports:
        st.session_state.controller = 0
        st.session_state.countFilters = 0
        st.session_state.filters = ""
        st.session_state.ordernation = None
        st.session_state.report = False
        report_fields = []
        st.experimental_rerun()

