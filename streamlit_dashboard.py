import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Adicionar execution ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'execution'))
from trends_tool_batch import TrendsBatchAnalyzer

# Configuração da página
st.set_page_config(
    page_title="📊 Trends Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 12px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 12px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("📊 Trends Dashboard")
st.markdown("Análise de palavras-chave com raspagem de dados no Google Trends e Wikipedia.")
st.markdown("Baixe o exemplo da tabela e preencha com suas keywords para começar!")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    upload_mode = st.radio(
        "Modo de entrada:",
        ["Upload de Arquivo", "Exemplo da tabela"]
    )

# Gerenciamento de estado
if 'results' not in st.session_state:
    st.session_state.results = None
    st.session_state.df_summary = None
    st.session_state.analyzer = None
    st.session_state.errors = []
    st.session_state.example_loaded = False

# Modo 1: Upload de arquivo
if upload_mode == "Upload de Arquivo":
    uploaded_file = st.file_uploader(
        "📤 Selecione seu arquivo CSV ou Excel",
        type=['csv', 'xlsx', 'xls'],
        help="Colunas: keyword (obrigatória), geo, timeframe, language (opcionais)"
    )
    
    if uploaded_file is not None:
        # Salvar arquivo temporário
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ Arquivo '{uploaded_file.name}' carregado")
        
        # Preview dos dados
        if uploaded_file.name.endswith('.csv'):
            df_preview = pd.read_csv(temp_path)
        else:
            df_preview = pd.read_excel(temp_path)
        
        st.subheader("📋 Preview dos dados")
        st.dataframe(df_preview, use_container_width=True)
        
        # Validar duplicatas
        if 'keyword' in df_preview.columns:
            duplicates = df_preview[df_preview.duplicated(subset=['keyword'], keep=False)]['keyword'].unique()
            if len(duplicates) > 0:
                st.warning(f"⚠️ Aviso: {len(duplicates)} keyword(s) duplicada(s) detectada(s):")
                for dup in duplicates:
                    count = len(df_preview[df_preview['keyword'] == dup])
                    st.text(f"   • '{dup}' aparece {count} vezes")
                st.info("✓ Será removida apenas a primeira ocorrência durante o processamento")
        
        if st.button("🚀 Processar Arquivo", key="process_file_btn"):
            st.info("⏳ Processando keywords... Aguarde!")
            
            try:
                analyzer = TrendsBatchAnalyzer()
                results = analyzer.process_batch(temp_path)
                
                st.session_state.results = results
                st.session_state.analyzer = analyzer
                st.session_state.errors = analyzer.errors
                
                summary_df = analyzer.get_results_dataframe(results)
                st.session_state.df_summary = summary_df
                
                successful = sum(1 for r in results if r['success'])
                st.success(f"✅ {successful}/{len(results)} keywords processadas com sucesso")
                
                os.remove(temp_path)
                
            except Exception as e:
                st.error(f"❌ Erro ao processar: {str(e)}")

# Modo 2: Usar exemplo
else:
    col1, col2 = st.columns(2)

    example_path = "input_example.csv"
    with col1:
        if os.path.exists(example_path):
            with open(example_path, 'rb') as f:
                st.download_button(
                    label="⬇️ Baixar Exemplo CSV",
                    data=f.read(),
                    file_name="input_example.csv",
                    mime="text/csv",
                    key="download_example_btn"
                )
            st.session_state.example_loaded = True
        else:
            st.warning("Arquivo de exemplo não encontrado para download")
    
    if st.session_state.example_loaded:
        example_path = "input_example.csv"
        
        if os.path.exists(example_path):
            st.success("✅ Exemplo carregado")
            
            df_preview = pd.read_csv(example_path)
            st.subheader("📋 Preview do exemplo")
            st.dataframe(df_preview, use_container_width=True)
            
            # Validar duplicatas
            if 'keyword' in df_preview.columns:
                duplicates = df_preview[df_preview.duplicated(subset=['keyword'], keep=False)]['keyword'].unique()
                if len(duplicates) > 0:
                    st.warning(f"⚠️ Aviso: {len(duplicates)} keyword(s) duplicada(s) detectada(s):")
                    for dup in duplicates:
                        count = len(df_preview[df_preview['keyword'] == dup])
                        st.text(f"   • '{dup}' aparece {count} vezes")
                    st.info("✓ Será removida apenas a primeira ocorrência durante o processamento")
            
            if st.button("🚀 Processar Exemplo", key="process_example_btn"):
                st.info("⏳ Processando exemplo... Aguarde!")
                
                try:
                    analyzer = TrendsBatchAnalyzer()
                    results = analyzer.process_batch(example_path)
                    
                    st.session_state.results = results
                    st.session_state.analyzer = analyzer
                    st.session_state.errors = analyzer.errors
                    
                    summary_df = analyzer.get_results_dataframe(results)
                    st.session_state.df_summary = summary_df
                    
                    successful = sum(1 for r in results if r['success'])
                    st.success(f"✅ {successful}/{len(results)} keywords processadas")
                    
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
        else:
            st.error("Arquivo de exemplo não encontrado!")

# Mostrar resultados se disponível
if st.session_state.df_summary is not None and not st.session_state.df_summary.empty:
    st.markdown("---")
    st.header("📊 Análise de Resultados")
    
    # Abas de resultados
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Resumo", "📋 Tabela Completa", "🎯 Comparativos", "⚠️ Erros"])
    
    df_summary = st.session_state.df_summary
    
    with tab1:
        st.subheader("📊 Estatísticas Gerais")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Keywords", len(df_summary))
        
        with col2:
            com_dados = df_summary['has_data'].sum()
            st.metric("Com Dados", com_dados)
        
        with col3:
            google_medio = df_summary['google_mean'].mean()
            st.metric("Google Trends (Média)", f"{google_medio:.1f}")
        
        with col4:
            total_erros = len(st.session_state.errors)
            st.metric("Erros", total_erros)
        
        # Seletor de métrica
        st.subheader("📈 Gráficos Comparativos")
        
        col_metric1, col_metric2 = st.columns([2, 1])
        with col_metric1:
            st.markdown("**Selecione a métrica:**")
        with col_metric2:
            metric_type = st.selectbox(
                "Métrica",
                ["Máximo", "Média", "Mínimo"],
                key="metric_selector",
                label_visibility="collapsed"
            )
        
        # Determinar colunas
        if metric_type == "Máximo":
            google_col = 'google_max'
            wiki_col = 'wiki_max'
            title_suffix = "Máximo"
        elif metric_type == "Média":
            google_col = 'google_mean'
            wiki_col = 'wiki_mean'
            title_suffix = "Média"
        else:
            google_col = 'google_min'
            wiki_col = 'wiki_min'
            title_suffix = "Mínimo"
        
        # Gráficos lado a lado
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown(f"**Google Trends - {title_suffix} (Top 15)**")
            top_google = df_summary.nlargest(15, google_col)[['keyword', google_col]].sort_values(google_col)
            fig_google = go.Figure(data=[
                go.Bar(y=top_google['keyword'], x=top_google[google_col], orientation='h', marker_color='#1f77b4')
            ])
            fig_google.update_layout(height=400, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
            fig_google.update_xaxes(title_text="Valor")
            fig_google.update_yaxes(title_text="")
            st.plotly_chart(fig_google, use_container_width=True)
        
        with col_g2:
            st.markdown(f"**Wikipedia - {title_suffix} (Top 15)**")
            top_wiki = df_summary.nlargest(15, wiki_col)[['keyword', wiki_col]].sort_values(wiki_col)
            fig_wiki = go.Figure(data=[
                go.Bar(y=top_wiki['keyword'], x=top_wiki[wiki_col], orientation='h', marker_color='#ff7f0e')
            ])
            fig_wiki.update_layout(height=400, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
            fig_wiki.update_xaxes(title_text="Valor")
            fig_wiki.update_yaxes(title_text="")
            st.plotly_chart(fig_wiki, use_container_width=True)
    
    with tab2:
        st.subheader("📋 Dados Completos com Filtros")
        
        # Filtros
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            search_keyword = st.text_input("🔍 Buscar keyword", value="")
        
        with col_f2:
            google_min = st.number_input("Google Trends (mínimo)", min_value=0, max_value=100, value=0)
        
        with col_f3:
            regions = df_summary['top_region'].unique()
            selected_region = st.selectbox("Região", ["Todas"] + sorted(list(regions)))
        
        # Aplicar filtros
        df_filtered = df_summary.copy()
        
        if search_keyword:
            df_filtered = df_filtered[df_filtered['keyword'].str.contains(search_keyword, case=False, na=False)]
        
        if google_min > 0:
            df_filtered = df_filtered[df_filtered['google_max'] >= google_min]
        
        if selected_region != "Todas":
            df_filtered = df_filtered[df_filtered['top_region'] == selected_region]
        
        # Exibir tabela
        st.dataframe(
            df_filtered,
            use_container_width=True,
            hide_index=True,
            column_config={
                "keyword": st.column_config.TextColumn("Keyword", width="medium"),
                "google_max": st.column_config.NumberColumn("Google Max", format="%.0f"),
                "google_mean": st.column_config.NumberColumn("Google Média", format="%.2f"),
                "google_min": st.column_config.NumberColumn("Google Min", format="%.0f"),
                "wiki_max": st.column_config.NumberColumn("Wiki Max", format="%.0f"),
                "wiki_mean": st.column_config.NumberColumn("Wiki Média", format="%.2f"),
                "wiki_min": st.column_config.NumberColumn("Wiki Min", format="%.0f"),
            }
        )
        
        # Download CSV
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download (CSV)",
            data=csv,
            file_name="trends_results.csv",
            mime="text/csv"
        )
    
    with tab3:
        st.subheader("🎯 Comparativos Avançados")
        
        # Seleção de keywords para comparação
        keywords_list = df_summary['keyword'].tolist()
        selected_keywords = st.multiselect(
            "Selecione keywords para comparar",
            keywords_list,
            default=keywords_list[:5] if len(keywords_list) >= 5 else keywords_list
        )
        
        if selected_keywords:
            df_compare = df_summary[df_summary['keyword'].isin(selected_keywords)]
            
            # Gráfico de comparação - 3 métricas lado a lado
            col_c1, col_c2, col_c3 = st.columns(3)
            
            with col_c1:
                st.markdown("**Máximo**")
                fig_max = go.Figure(data=[
                    go.Bar(name='Google', x=df_compare['keyword'], y=df_compare['google_max'], marker_color='#1f77b4'),
                    go.Bar(name='Wiki', x=df_compare['keyword'], y=df_compare['wiki_max'], marker_color='#ff7f0e')
                ])
                fig_max.update_layout(height=400, barmode='group', showlegend=True, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig_max, use_container_width=True)
            
            with col_c2:
                st.markdown("**Média**")
                fig_mean = go.Figure(data=[
                    go.Bar(name='Google', x=df_compare['keyword'], y=df_compare['google_mean'], marker_color='#2ca02c'),
                    go.Bar(name='Wiki', x=df_compare['keyword'], y=df_compare['wiki_mean'], marker_color='#d62728')
                ])
                fig_mean.update_layout(height=400, barmode='group', showlegend=True, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig_mean, use_container_width=True)
            
            with col_c3:
                st.markdown("**Mínimo**")
                fig_min = go.Figure(data=[
                    go.Bar(name='Google', x=df_compare['keyword'], y=df_compare['google_min'], marker_color='#9467bd'),
                    go.Bar(name='Wiki', x=df_compare['keyword'], y=df_compare['wiki_min'], marker_color='#8c564b')
                ])
                fig_min.update_layout(height=400, barmode='group', showlegend=True, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig_min, use_container_width=True)
            
            # Tabela de comparação
            st.markdown("**Tabela de Comparação**")
            st.dataframe(
                df_compare[['keyword', 'google_max', 'google_mean', 'google_min', 'wiki_max', 'wiki_mean', 'wiki_min']],
                use_container_width=True,
                hide_index=True
            )
    
    with tab4:
        st.subheader("⚠️ Erros e Avisos")
        
        if st.session_state.errors:
            st.warning(f"Total de erros: {len(st.session_state.errors)}")
            
            for i, error in enumerate(st.session_state.errors[:20], 1):
                st.text(f"{i}. {error}")
            
            if len(st.session_state.errors) > 20:
                st.info(f"... e mais {len(st.session_state.errors) - 20} erros")
        else:
            st.success("✅ Nenhum erro encontrado!")
