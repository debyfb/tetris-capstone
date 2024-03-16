import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

# Config
st.set_page_config(
    page_title="Analysis of Railway Station in West Java",
    layout="wide",
    page_icon=":station:"
)

# Import Dataframe
df = pd.read_csv('daftar.csv')
dfm = pd.read_csv('koordinat_stasiun.csv')
dfs = pd.read_csv('status.csv')
dfk = pd.read_csv('kategori.csv')
dfsk = pd.read_csv('stasiun_aktif_lengkap.csv')



st.title("Analysis of Railway Station in West Java")

with st.sidebar:
    st.header("Data Summary")
    
    col1a, col2a = st.columns(2)
    with col1a:
        st.markdown("**Total of Railway Stations**")
        st.markdown("**:blue[141]**")
    with col2a:
        st.markdown("**Total of Active Railway Stations**")
        st.markdown(":blue[**114**]")

    col1b, col2b = st.columns(2)
    with col1b:
        st.markdown("**Highest Number of Active Stations**")
        st.markdown("**:blue[9]**")
        st.caption("Bogor Regency")
    
    with col2b:
        st.markdown("**Lowest Number of Active Stations**")
        st.markdown(":blue[**0**]")
        st.caption("Kuningan Regency, Sumedang Regency") 

    col1c, col2c = st.columns(2)
    
    with col1c:
        st.markdown("**Highest Population Density**")
        st.markdown("**:blue[15,076]**")
        st.caption("Bandung City")

    with col2c:
        st.markdown("**Lowest Population Density**")
        st.markdown(":blue[**653**]")
        st.caption("Sukabumi Regency")

    col1d, col2d = st.columns(2)

    with col1d:
            st.markdown("**Average of Population Density**")
            st.markdown("**:blue[3,858]**")
    
    with col2d:
        st.markdown("**Total of City/Regency**")
        st.markdown("**:blue[27]**") 

tab1, tab2 = st.tabs(["Introduction", "Data Analysis Report"])

with tab1:
    st.subheader("Why Infrastructure Matters?")
    st.markdown('''
                Infrastructure development in Indonesia plays a crucial role in steering the country towards progress. It is prioritized as it significantly enhances the country’s productivity and competitiveness.
                                
                Good infrastructure is also able to facilitate the distribution and mobility of goods. Shorter and more efficient time makes product prices competitive and not too expensive. 
                Moreover, efficient infrastructure facilitates seamless transportation and distribution of goods, leading to competitive product pricing and increased accessibility.
                
                Improving transportation infrastructure in a region, including railway stations, promotes fairer development of facilities and infrastructure. Smooth distribution eliminates the concept of underdeveloped regions, leading to reduced poverty.
                ''')
    
    st.subheader("Railway Station")
    st.markdown('''
                Railway stations are really important for connecting communities and making travel easier. They serve as hubs for both people and goods, can easily move from one place to another, linking remote locations to big cities. This helps the economy grow by offering dependable and effective transportation for goods and materials, which creates employment opportunities and boosts local businesses, especially in rural places with fewer transport options.
                
                Furthermore, railway stations serve as significant cultural symbols, embodying the history, architecture, and heritage of the regions they serve. In essence, railway stations are essential components of the transportation system, facilitating connections between individuals, communities, and businesses.
                ''')

    st.subheader("Railway Stations in West Java")
    st.map(dfm)
    st.caption("Distribution of railway stations in West Java")
    st.markdown('''
                Understanding the role of railway stations in facilitating transportation and community connectivity provides the foundation for gaining analytical insights into railway stations in West Java.

                The insights gained will provide valuable insights for commuters, policymakers, and stakeholders involved in transportation planning and infrastructure development in West Java.
                ''')


with tab2:

    # Status
    st.header("Analysis of the Number of Railway Stations in West Java Based on Status")
    
    st.markdown('''
                Status of the railway station is categorized into 3 groups.
                1. **Operasi**: The station is still operational.
                2. **Reaktivasi**: The station is currently being reactivated.
                3. **Tidak operasi**: The station is no longer operational.
                ''')

    tab1a, tab2a = st.tabs(["All Data", "Filtered by City/Regency"])

    # All data
    with tab1a:
        dropped_dfs = dfs[(dfs.groupby('nama_kabupaten_kota')['jumlah_stasiun'].transform('sum') != 0)]
        status_groupby_kota = dropped_dfs.groupby(['nama_kabupaten_kota','status'])['jumlah_stasiun'].sum().reset_index()
        chart1 = alt.Chart(status_groupby_kota).mark_bar().encode(
        x = alt.X('sum(jumlah_stasiun):Q', stack='zero', title='Total'),
        y = alt.Y('nama_kabupaten_kota:N', title='City/Regency').sort('-x'),
        color = alt.Color('status:N', title='Status')
            ).configure_view(
                stroke='transparent'
            ).configure_range(
            category={'scheme': 'darkmulti'}
            ).configure_axis(labelLimit=1000
            ).properties(width=800)
        st.altair_chart(chart1)
        st.caption("Note: Kuningan Regency and Sumedang Regency do not have any stations.")
    
    # Filtered by city/regency
    with tab2a:
        # Data selection
        kota1 = dfs['nama_kabupaten_kota'].unique().tolist()
        status_option = st.selectbox('Select a city or a regency:', kota1, key='kota1_selectbox')
        st.caption("Note: Kuningan Regency and Sumedang Regency do not have any stations.")
        # 2 column layout
        col1e, col2e = st.columns(2)

        with col1e:
            st.write(f"**Number of Railway Stations in West Java Based on Status**")
            
            status_all = dfs.groupby('status')['jumlah_stasiun'].sum().reset_index()
            
            piechart1 = alt.Chart(status_all).mark_arc().encode(
                theta = alt.Theta('jumlah_stasiun:Q', title='Total'),
                color = alt.Color('status:N', title='Status'),
                tooltip = [alt.Tooltip('status:N', title='Status'),
                           alt.Tooltip('jumlah_stasiun:Q', title='Total')]
                ).configure_range(
                    category={'scheme': 'darkmulti'}
                ).properties(
                    width=350,
                    height=350
                )
            st.altair_chart(piechart1)
        
        with col2e:
            st.write(f"**Number of Railway Stations in {status_option}, West Java Based on Status**")
        
            # Filter the data based on selected city/regency
            filtered_dfs = dfs.copy()
            filtered_dfs = filtered_dfs[filtered_dfs['nama_kabupaten_kota'] == status_option]

            # Calculate status
            status_per_kota = filtered_dfs.groupby('status')['jumlah_stasiun'].sum().reset_index()

            # Pie Chart
            piechart2 = alt.Chart(status_per_kota).mark_arc().encode(
                theta = alt.Theta('jumlah_stasiun:Q', title='Total'),
                color = alt.Color('status:N', title='Status'),
                tooltip = [alt.Tooltip('status:N', title='Status'),
                           alt.Tooltip('jumlah_stasiun:Q', title='Total')]
                ).configure_range(
                    category={'scheme': 'darkmulti'}
                ).properties(
                    width=350,
                    height=350
                )
            st.altair_chart(piechart2)

    st.markdown("The majority of railway stations in West Java are currently **:blue[operational]**, while a smaller proportion are either inactive or in the process of reactivation. This shows that railway infrastructure varies across regions, with some areas not having any train access.")    
    
    # Class Category
    st.header("Analysis of the Number of Railway Stations in West Java Based on Class")

    st.markdown('''
                Class of railway station is categorized into 8 groups.
                1. **I**: The station provides long and medium distance trains.
                2. **II**: The station provides medium distance and local trains.
                3. **III**: The station provides local trains and commuter line.
                4. **Halte**: The station only have platforms and ticket sales counters.
                5. **Besar**: The station has larger area and more complete facilities than class I, II, or III stations.
                6. **Besar Tipe A**: The station is large and provides long and medium distance trains.
                7. **Besar Tipe B**: The station is large and provides medium distance and local trains.
                8. **Besar Tipe C**: The station is large and provides long and medium distance trains.
                
                Below, the class of railway station is divided into two main groups: **:blue[Regular Stations]** and **:blue[Large Stations]**. Regular stations consist of Class I, II, III, and Halte, while large stations consist of Besar, Besar Tipe A, Besar Tipe B, and Besar Tipe C.
                ''')

    dropped_dfk = dfk[(dfk.groupby('nama_kabupaten_kota')['jumlah_stasiun'].transform('sum') != 0)]
    class_groupby_kota = dropped_dfk.groupby(['nama_kabupaten_kota','kategori_kelas'])['jumlah_stasiun'].sum().reset_index()
    
    tab1b, tab2b = st.tabs(["Regular Stations", "Large Stations"])
    
    with tab1b:
    # Kelas Biasa
        kelas_biasa = class_groupby_kota[class_groupby_kota['kategori_kelas'].isin(['I', 'II', 'III', 'HALTE'])]
        dropped_kelas_biasa = kelas_biasa[(kelas_biasa.groupby('nama_kabupaten_kota')['jumlah_stasiun'].transform('sum') != 0)]
        chart1a = alt.Chart(dropped_kelas_biasa).mark_bar().encode(
        x = alt.X('sum(jumlah_stasiun):Q', stack='zero', title='Total'),
        y = alt.Y('nama_kabupaten_kota:N', title='City/Regency').sort('-x'),
        color = alt.Color('kategori_kelas:N', title='Class').sort('-x')
            ).configure_view(
                stroke='transparent'
            ).configure_range(
                category={'scheme': 'darkmulti'}
            ).configure_axis(labelLimit=1000
            ).properties(width=750)
        st.altair_chart(chart1a)
    
    with tab2b:
        # Kelas Besar
        kelas_besar = class_groupby_kota[class_groupby_kota['kategori_kelas'].isin(['BESAR', 'BESAR TIPE A', 'BESAR TIPE B', 'BESAR TIPE C'])]
        dropped_kelas_besar = kelas_besar[(kelas_besar.groupby('nama_kabupaten_kota')['jumlah_stasiun'].transform('sum') != 0)]
        chart1b = alt.Chart(dropped_kelas_besar).mark_bar().encode(
        x = alt.X('sum(jumlah_stasiun):Q', stack='zero', title='Total'),
        y = alt.Y('nama_kabupaten_kota:N', title='City/Regency').sort('-x'),
        color = alt.Color('kategori_kelas:N', title='Class').sort('-x')
            ).configure_view(
                stroke='transparent'
            ).configure_range(
                category={'scheme': 'darkmulti'}
            ).configure_axis(labelLimit=1000
            ).properties(width=750)
        st.altair_chart(chart1b)

    st.markdown("Most railway stations in West Java are categorized as **:blue[class III]**, which provides local trains and commuter line, followed by class II and I. This distribution emphasizes a **:blue[focus on serving local commuting needs]**.")
    
    st.header("Analysis of Population Density, Nominal GRDP Per Capita, and Tourism Aspects with the Number of Active Stations")    
    
    st.write("This analysis focuses on finding the impact of population density, Nominal GRDP per capita, and tourism on the number of active railway stations.")

    tab1c, tab2c, tab3c = st.tabs(["Population Density", "Nominal GRDP Per Capita", "Tourism"])
    
    with tab1c:
        st.markdown('''
                    Population density is the number of people per square kilometer of the area.

                    Transportation infrastructure tends to be more concentrated in areas with higher population densities due to increased demand for transportation services. However, it's important to note that this correlation may not always hold true in every case.
                    ''')
        chart2 = alt.Chart(dfsk).mark_circle(size=60).encode(
                x = alt.X('kepadatan_penduduk:Q', title='Population Density'),
                y = alt.Y('stasiun_aktif:Q', title='Number of Active Stations'),
                color = alt.Color('nama_kabupaten_kota:N', title='City/Regency'),
                tooltip = [alt.Tooltip('nama_kabupaten_kota:N', title='City/Regency'),
                           alt.Tooltip('stasiun_aktif:Q', title='Active Stations'),
                           alt.Tooltip('kepadatan_penduduk:Q', title='Population Density')]
            ).interactive(
            ).configure_range(
                category={'scheme': 'spectral'}
            ).configure_axis(labelLimit=1000
            ).properties(width=800)
        st.altair_chart(chart2)
        
    with tab2c:
        st.markdown('''
                    Nominal GRDP per capita measures how well the economy of the region is doing without factoring in price changes due to inflation or deflation. Nominal GRDP (gross regional domestic product) per capita is calculated by dividing the GRDP of a region by its population.
                    
                    The unit used for nominal GDP per capita is thousand rupiah.
                    ''')
        chart3 = alt.Chart(dfsk).mark_circle(size=60).encode(
                x = alt.X('pdrb_adhk_per_kapita:Q', title='Nominal GRDP Per Capita'),
                y = alt.Y('stasiun_aktif:Q', title='Number of Active Stations'),
                color = alt.Color('nama_kabupaten_kota:N', title='City/Regency'),
                tooltip = [alt.Tooltip('nama_kabupaten_kota:N', title='City/Regency'),
                           alt.Tooltip('stasiun_aktif:Q', title='Active Stations'),
                           alt.Tooltip('pdrb_adhk_per_kapita:Q', title='Nominal GRDP Per Capita')]                
            ).interactive(
            ).configure_range(
                category={'scheme': 'spectral'}
            ).configure_axis(labelLimit=1000
            ).properties(width=800)
        st.altair_chart(chart3)
    
    with tab3c:
        st.markdown('''
                    Tourism aspect in West Java is evaluated based on the total number of visitors, including both foreign and domestic visitors, who visit recreational destinations in West Java during the year 2021.
                    ''')
        chart4 = alt.Chart(dfsk).mark_circle(size=60).encode(
                x = alt.X('pengunjung:Q', title='Visitors'),
                y = alt.Y('stasiun_aktif:Q', title='Number of Active Stations'),
                color = alt.Color('nama_kabupaten_kota:N', title='City/Regency'),
                tooltip = [alt.Tooltip('nama_kabupaten_kota:N', title='City/Regency'),
                           alt.Tooltip('stasiun_aktif:Q', title='Active Stations'),
                           alt.Tooltip('pengunjung:Q', title='Visitors')]
            ).interactive(
            ).configure_range(
                category={'scheme': 'spectral'}
            ).configure_axis(labelLimit=1000
            ).properties(width=800)
        st.altair_chart(chart4)
    
    st.header("Correlation")
    st.markdown("The heatmap below visualizes correlations between the number of active stations, population density, nominal GRDP per capita, and tourism.")
    with st.expander("See guidelines"):
        st.write('''
                 - **:blue[1.0 to 0.8]**: Very strong positive correlation
                 - **:blue[0.8 to 0.6]**: Strong positive correlation
                 - **:blue[0.6 to 0.4]**: Moderate positive correlation
                 - **:blue[0.4 to 0.2]**: Weak positive correlation
                 - **:blue[0.2 to 0.0]**: Very weak positive correlation
                 - **:blue[0.0]**: No correlation
                 - **:blue[0.0 to -0.2]**: Very weak negative correlation
                 - **:blue[-0.2 to -0.4]**: Weak negative correlation
                 - **:blue[-0.4 to -0.6]**: Moderate negative correlation
                 - **:blue[-0.6 to -0.8]**: Strong negative correlation
                 - **:blue[-0.8 to -1.0]**: Very strong negative correlation
                 ''')


    column_labels = {
        'stasiun_aktif': 'Active Stations',
        'pengunjung': 'Tourism',
        'pdrb_adhk_per_kapita': 'GRDP Per Capita',
        'kepadatan_penduduk': 'Population Density'
    }
    cor_data = (dfsk.drop(columns=['nama_kabupaten_kota'])
                .corr().stack()
                .reset_index()
                .rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'}))
    cor_data['variable'] = cor_data['variable'].map(column_labels)
    cor_data['variable2'] = cor_data['variable2'].map(column_labels)
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)

    base = alt.Chart(cor_data).encode(
    x='variable2:O',
    y='variable:O'    
    )

    # Text layer with correlation labels
    # Colors are for easier readability
    text = base.mark_text().encode(
        text='correlation_label',
        color=alt.condition(
            alt.datum.correlation > 0.5, 
            alt.value('black'),
            alt.value('white')
        )
    )

    # The correlation heatmap
    cor_plot = base.mark_rect().encode(
        color='correlation:Q',
    ).properties(
        width=500,
        height=400)
    cor_plot + text

    st.markdown('''
                - The correlations between the number of active stations and the number of visitors indicates a moderate positive correlation It means regions with higher visitor numbers tend to have more active stations. This suggests that transportation infrastructure development may be responsive to demand from visitors.
                - The correlations between the number of active stations and population density indicates a moderate negative correlation. It means regions with lower population density tend to have more active stations. This suggests that transportation infrastructure development may be responsive to the need to serve dispersed populations.
                - The correlations between the number of active stations and nominal GRDP per capita indicates a very weak negative correlation. It means economic factors may not be the primary driver behind transportation infrastructure.
                - Tourism demand have the most significant impact on the number of active stations among other factors.
                ''')
