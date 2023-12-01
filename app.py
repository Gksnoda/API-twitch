import streamlit as st
import pandas as pd
import time
from DAO import *
from model import *
import pdfkit as pdf

#funcao que ira gerar o relatorio, com base nos campos, filtros e ordenação selecionado pelo usuario
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

    ##print(query.statement)

    df = pd.read_sql_query(query.statement, con = DAO.getSession())
    session.commit()
    session.close()

    st.session_state.dataframe = df

    #convertendo o dataframe do relatorio para excel e html
    df.to_excel("E:/relatorio.xlsx", index=False)
    df.to_html('E:/relatorio.html', index=False)


#funcao para limpar o campo do input do valor do filtro
def clear_form():        
    st.session_state["bar"] = ""

#funcoes para setar alguns session_states que precisamos utilizar 
def set_filters_columns_count():
    st.session_state.filters = ""
    st.session_state.query = False
    st.session_state.countFilters = 0

def set_ordernation():
    st.session_state.ordernation = True

#converte o arquivo html gerado pelo pandas para pdf
def df_to_pdf():
    path_to_wkhtmltopdf = r'E:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdf.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    pdf.from_file('E:/relatorio.html', 'relatorio.pdf', configuration=config)


#configuração da página
st.set_page_config(page_title="Relatório TwitchAPI")


#remove 'Made with Streamlit' da página
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


#sidebar
st.sidebar.header("Twitch API")
##st.sidebar.image('./img/logo.jpg', width=200)
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.header("Desenvolvido por:")
st.sidebar.write("Guilherme Ribeiro")
st.sidebar.write("Tales Oliveira")


#titulo
st.title('Relatórios TwitchAPI')
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

#página para gerar o relatório
if st.session_state.controller == 0:
    f1, f2 = st.columns([1, 1])

    with f1:
        report_type = st.selectbox(
        'Selecione o relatório:',
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
        report_fields = st.multiselect(f'Selecione os campos do relatório de {report_type}:', options = st.session_state.df.columns)

    st.write('\n')
    st.write("Selecione os filtros do relatório:")

    with st.form("myform"):
        f1, f2, f3 = st.columns([1, 1, 1])
        with f1:
            field = st.selectbox("Campo:", options = st.session_state.df.columns)
        with f2:
            comparison = st.selectbox("Comparação:", options = ('igual', 'maior', 'menor', 'maior ou igual', 'menor ou igual', 'diferente de', 'que possua a string'))
        with f3:
            comparison_value = st.text_input("Valor")

        f1, f2, f3 = st.columns([1, 1, 1])
        
        with f2:
            st.write('\n')
            submit = st.form_submit_button(label="Adicionar filtro", on_click=clear_form)

            
    if submit and comparison_value:
        map_operation = {
        'igual':f'= ',
        'maior':f'> ',
        'menor':f'< ',
        'maior ou igual':f'>= ',
        'menor ou igual':f'<= ',
        'diferente de':f'!= ',
        'que possua a string': 'LIKE \'%'
        }

        operation = map_operation[comparison]
        
        if st.session_state.df[f'{field}'].dtypes == 'object' and not comparison == 'que possua a string':
            value = f"'{comparison_value}'"
        elif comparison == 'que possua a string':
            value = f"{comparison_value}"
        else:
            value = f'{comparison_value}'

        #adiciona os filtros
        if st.session_state.countFilters == 0:
            st.session_state.filters += f"{field} {operation}{value}"
        else:
            st.session_state.filters += f" AND {field} {operation}{value}"

        #se a comparação for "que possua a string", precisamos adicionar o % no final para realizar a consulta
        if comparison == 'que possua a string':
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

    st.write('\n\n\n')

    with st.expander("Filtros adicionados"):
        st.write(st.session_state.filters)

    f1, f2, f3 = st.columns([1.5, 1.5, 1])

    with f1:
        ordernation_field = st.selectbox('Selecione o campo que o relatório será ordenado:', options = st.session_state.df.columns)
        
    with f2:
        ordernation_type = st.radio(f'Campo {ordernation_field} ordenado de modo:', options = ('Crescente', 'Decrescente'), horizontal = True)

    with f3:
        st.write('\n\n\n\n\n')

        ordernation_report = st.button('Ordenar relatório!', on_click=set_ordernation)

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


#página com o relatório gerado
else:
    if st.session_state.report == False:

        #gera o relatório para pdf
        df_to_pdf()

        with open("relatorio.pdf", "rb") as pdf_file:
            st.session_state.pdfData  = pdf_file.read()

        with open("E:/relatorio.xlsx", "rb") as xlsx_file:
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

