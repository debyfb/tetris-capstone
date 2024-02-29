import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

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
dfsk = pd.read_csv('daftar_status_kepadatan.csv')
dfk = pd.read_csv('kategori.csv')


st.title("Analysis of Railway Station in West Java")

with st.sidebar:
    st.header("Data Summary")
    
    col1a, col2a = st.columns(2)
    with col1a:
        st.markdown("**Total of Railway Stations**")
        st.markdown("**:blue[141]**")
    with col2a:
        st.markdown("**Total of Active Railway Stations**")
        st.markdown(":blue[**27**]")

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
    
    
    # link = '[LinkedIn](http://linkedin.com/in/deby-febriani/)'
    # st.markdown(link, unsafe_allow_html=True)

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
    
    tab1a, tab2a = st.tabs(["All Data", "Filtered by City/Regency"])

    with tab1a:
        status_groupby_kota = dfs.groupby(['nama_kabupaten_kota','status'])['jumlah_stasiun'].sum().reset_index()
        
        chart1 = alt.Chart(status_groupby_kota).mark_bar().encode(
        x = alt.X('sum(jumlah_stasiun):Q', stack='zero', title='Total'),
        y = alt.Y('nama_kabupaten_kota:N', title='City/Regency'),
        color = alt.Color('status:N', title='Status'),
        order = alt.Order('status', sort='ascending')
            ).configure_view(
                stroke='transparent'
            ).configure_axis(labelLimit=1000
            ).properties(width=800)
        st.altair_chart(chart1)
    
    with tab2a:
        # Data selection
        kota1 = dfs['nama_kabupaten_kota'].unique().tolist()
        status_option = st.selectbox('Select a city or a regency:', kota1, key='kota1_selectbox')

        # 2 column layout
        col1e, col2e = st.columns(2)

        with col1e:
            st.write(f"**Number of Railway Stations in West Java Based on Status**")
            
            status_all = dfs.groupby('status')['jumlah_stasiun'].sum().reset_index()
            
            piechart1 = alt.Chart(status_all).mark_arc().encode(
                theta = alt.Theta('jumlah_stasiun:Q', title='Total'),
                color = alt.Color('status:N', title='Status'),
                tooltip = ['status', 'jumlah_stasiun']
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
                tooltip = ['status', 'jumlah_stasiun']
                ).properties(
                    width=350,
                    height=350
                )
            st.altair_chart(piechart2)

    st.markdown('''
                Status of the railway station is categorized into 3 groups.
                1. **Operasi**: The station is still operational.
                2. **Reaktivasi**: The station is currently being reactivated.
                3. **Tidak operasi**: The station is no longer operational.
                ''')
    st.subheader("Insight")
    st.markdown("The majority of railway stations in West Java are currently **:blue[operational]**, while a smaller proportion are either inactive or in the process of reactivation. We can see that Kuningan Regency and Sumedang Regency do not have any stations. This shows that railway infrastructure varies across regions, with some areas not having any train access. To improve this situation, the government need to expand railway networks and connect more areas, ensuring everyone has access to transportation in West Java.")
    
    # Category
    st.header("Analysis of the Number of Railway Stations in West Java Based on Class")

    class_groupby_kota = dfk.groupby(['nama_kabupaten_kota','kategori_kelas'])['jumlah_stasiun'].sum().reset_index()

    chart1a = alt.Chart(class_groupby_kota).mark_bar().encode(
       x = alt.X('sum(jumlah_stasiun):Q', stack='zero', title='Total'),
       y = alt.Y('nama_kabupaten_kota:N', title='City/Regency'),
       color = alt.Color('kategori_kelas:N', title='Class')
        ).configure_view(
            stroke='transparent'
        ).configure_range(
            category={'scheme': 'spectral'}
        ).configure_axis(labelLimit=1000
        ).properties(width=800)
    st.altair_chart(chart1a)
    st.markdown('''
                Class of railway station is categorized into 8 groups.
                1. **I**: The station provides long and medium distance trains.
                2. **II**: The station provides medium distance and local trains.
                3. **III**: The station provides local trains and commuter line.
                4. **Besar**: The station has larger area and more complete facilities than class I, II, or III stations.
                5. **Besar Tipe A**: The station is large and provides long and medium distance trains.
                6. **Besar Tipe B**: The station is large and provides medium distance and local trains.
                7. **Besar Tipe C**: The station is large and provides long and medium distance trains.
                8. **Halte**: The station only have platforms and ticket sales counters.
                ''')
    st.subheader("Insight")
    st.markdown("Most railway stations in West Java are categorized as **:blue[class III]**, which provides local trains and commuter line, followed by class II and I. This distribution emphasizes a focus on serving local commuting needs. However, there's a potential for further development of medium and long-distance rail services to enhance intercity connectivity.")
    
    st.header("Analysis of the Number of Active Railway Stations with Population Density in West Java")    

    chart2 = alt.Chart(dfsk).mark_circle(size=60).encode(
            x = alt.X('kepadatan_penduduk:Q', title='Population Density'),
            y = alt.Y('stasiun_aktif_per_kab_kota:Q', title='Number of Active Stations'),
            color = alt.Color('nama_kabupaten_kota:N', title='City/Regency'),
            tooltip = ['stasiun_aktif_per_kab_kota:Q', 'kepadatan_penduduk:Q', 'nama_kabupaten_kota:N']
        ).interactive(
        ).configure_range(
            category={'scheme': 'spectral'}
        ).configure_axis(labelLimit=1000
        ).properties(width=800)
    st.altair_chart(chart2)
    st.markdown(f"Note that only 23 out of 27 regencies/cities are displayed because there are 4 regencies/cities in West Java that do not have active stations, namely **Kuningan Regency**, **Majalengka Regency**, **Pangandaran Regency**, and **Sumedang Regency**")
    st.subheader("Insight")
    st.markdown('''
                Transportation infrastructure tends to be more concentrated in areas with higher population densities due to increased demand for transportation services. However, it's important to note that this correlation may not always hold true in every case.
                
                For instance, :blue[Cimahi Regency], with the 2nd highest population density, has only one active station, while :blue[Sukabumi Regency], with the lowest population density in the area, surprisingly has 7 active stations. This highlights the need for a proactive approach by provincial governments in developing transportation infrastructure in less densely populated areas. Such uneven distribution emphasizes the need for targeted investment and strategic planning to ensure fair access to railway services across different regions of West Java.

                This suggests that factors other than population density, such as historical development, economic considerations, and strategic planning, play a significant role in determining the distribution of railway infrastructure. Understanding these small differences is essential for optimizing transportation accessibility and fostering balanced regional development across West Java.
                ''')