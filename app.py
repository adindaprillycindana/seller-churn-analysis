
import streamlit as st
import pandas as pd
import pickle

# CONFIG & MODEL
st.set_page_config(
    page_title="Seller Churn Monitoring - Admin",
    layout="wide",
)

@st.cache_resource
def load_model():
    with open("best_model.sav", "rb") as f:
        return pickle.load(f)

model = load_model()

# SIDEBAR - INFO ADMIN
st.sidebar.title("Panel Admin")
st.sidebar.markdown(
    """
    Gunakan halaman ini untuk mengecek **risiko churn seller**  
    berdasarkan perilaku historis dan karakteristik tokonya.

    **Tips penggunaan:**
    - Isi fitur sesuai rentang nilai di dokumentasi.
    - Pastikan nilai kategorikal cocok dengan data training.
    - Perhatikan interpretasi probabilitas di bagian hasil.
    """
)

st.sidebar.markdown("---")
st.sidebar.subheader("Status Model")
st.sidebar.markdown(
    """
    - Nama model: `best_model.sav`  
    - Target: Probabilitas seller churn  
    - Output:  
      - Probabilitas churn  
      - Label: Berisiko churn / Tidak berisiko
    """
)

# HEADER HALAMAN
st.markdown(
    """
    <div style="padding: 10px 0 5px 0;">
        <h1 style="margin-bottom:0;">Seller Churn Monitoring</h1>
        <p style="color:gray; margin-top:4px;">
            Admin panel untuk memonitor dan mengevaluasi risiko churn seller berdasarkan fitur historis.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Placeholder untuk hasil prediksi (agar berasa dashboard)
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    churn_prob_placeholder = st.empty()
with metric_col2:
    churn_label_placeholder = st.empty()
with metric_col3:
    note_placeholder = st.empty()

# TABS: FORM INPUT & DOKUMENTASI
tab_form, tab_doc = st.tabs(["🔍 Cek Risiko Seller", "📄 Dokumentasi Fitur"])

with tab_form:
    st.subheader("Input Profil dan Perilaku Seller")

    st.markdown(
        """
        Lengkapi data di bawah ini untuk satu seller.  
        Sistem akan menghitung probabilitas churn dan memberikan status risiko.
        """
    )

    # Gunakan form supaya terasa lebih rapi seperti halaman admin
    with st.form("seller_form"):
        st.markdown("### Fitur Numerik")

        col1, col2, col3 = st.columns(3)

        with col1:
            product_id_nunique = st.number_input("product_id_nunique (1 - 129.6)", 1.0, 129.6, 10.0)
            price_min = st.number_input("price_min (0.85 - 1299)", 0.85, 1299.0, 50.0)
            freight_value_min = st.number_input("freight_value_min (0 - 71.04)", 0.0, 71.04, 5.0)
            freight_value_max = st.number_input("freight_value_max (0.75 - 218.7)", 0.75, 218.7, 20.0)
            payment_installments_min = st.number_input("payment_installments_min (0 - 10)", 0, 10, 0)
            payment_installments_max = st.number_input("payment_installments_max (1 - 20)", 1, 20, 5)
            payment_installments_median = st.number_input("payment_installments_median (1 - 10)", 1.0, 10.0, 3.0)
            payment_value_min = st.number_input("payment_value_min (0 - 1336.98)", 0.0, 1336.98, 50.0)
            payment_value_sum = st.number_input("payment_value_sum (18.56 - 78346.48)", 18.56, 78346.48, 1000.0)
            review_score_min = st.number_input("review_score_min (1 - 5)", 1, 5, 3)
            product_description_lenght_min = st.number_input("product_description_lenght_min (4 - 3992)", 4, 3992, 50)
            product_description_lenght_max = st.number_input("product_description_lenght_max (4 - 3992)", 4, 3992, 500)
            product_photos_qty_min = st.number_input("product_photos_qty_min (1 - 14)", 1, 14, 1)
            product_photos_qty_max = st.number_input("product_photos_qty_max (1 - 20)", 1, 20, 5)

        with col2:
            product_weight_g_min = st.number_input("product_weight_g_min (2 - 21490)", 2.0, 21490.0, 200.0)
            product_weight_g_max = st.number_input("product_weight_g_max (50 - 30000)", 50.0, 30000.0, 1000.0)
            product_weight_g_median = st.number_input("product_weight_g_median (2 - 24615)", 2.0, 24615.0, 500.0)
            product_length_cm_min = st.number_input("product_length_cm_min (7 - 89)", 7.0, 89.0, 20.0)
            product_height_cm_min = st.number_input("product_height_cm_min (2 - 62)", 2.0, 62.0, 5.0)
            product_height_cm_max = st.number_input("product_height_cm_max (2 - 96.3)", 2.0, 96.3, 20.0)
            product_width_cm_max = st.number_input("product_width_cm_max (8 - 90)", 8.0, 90.0, 20.0)
            seller_customer_distance_km_min = st.number_input("seller_customer_distance_km_min (0 - 2073)", 0.0, 2073.33, 10.0)
            seller_customer_distance_km_max = st.number_input("seller_customer_distance_km_max (1.14 - 3289)", 1.14, 3289.06, 100.0)
            seller_customer_distance_km_median = st.number_input("seller_customer_distance_km_median (1.14 - 2221)", 1.14, 2221.45, 50.0)
            seller_review_response_hours_min = st.number_input("seller_review_response_hours_min (2.42 - 148)", 2.42, 148.42, 10.0)
            seller_review_response_hours_max = st.number_input("seller_review_response_hours_max (4 - 5711)", 4.07, 5711.14, 100.0)
            seller_review_response_hours_mean = st.number_input("seller_review_response_hours_mean (4 - 363)", 4.07, 363.85, 20.0)

        with col3:
            seller_lead_time_approval_hours_min = st.number_input("seller_lead_time_approval_hours_min (0 - 43)", 0.0, 43.22, 1.0)
            seller_lead_time_approval_hours_max = st.number_input("seller_lead_time_approval_hours_max (0 - 258)", 0.0, 258.09, 24.0)
            seller_lead_time_approval_hours_median = st.number_input("seller_lead_time_approval_hours_median (0 - 64)", 0.0, 64.30, 5.0)
            seller_buffer_time_days_min = st.number_input("seller_buffer_time_days_min (-117 - 19)", -117.0, 19.0, 0.0)
            seller_buffer_time_days_max = st.number_input("seller_buffer_time_days_max (-46 - 1046)", -46.0, 1046.0, 5.0)
            seller_buffer_time_days_mean = st.number_input("seller_buffer_time_days_mean (-46 - 32)", -46.0, 32.17, 1.0)
            freight_gmv_ratio = st.number_input("freight_gmv_ratio (0.0015 - 0.5127)", 0.0015, 0.5127, 0.05)
            price_range = st.number_input("price_range (0 - 2198)", 0.0, 2198.72, 100.0)
            price_range_normalized = st.number_input("price_range_normalized (0 - 9.44)", 0.0, 9.44, 1.0)
            account_age = st.number_input("account_age (31 - 703)", 31, 703, 100)
            Activity_Rate = st.number_input("Activity_Rate (0.0014 - 0.9536)", 0.0014, 0.9536, 0.3)

        st.markdown("### Fitur Kategorikal")

        col_cat1, col_cat2 = st.columns(2)

        with col_cat1:
            seller_city_mode = st.select_box("seller_city_mode",
                                             ['timbo', 'porto alegre', 'ibitinga', 'sao paulo', 'imigrante',
       'formiga', 'atibaia', 'rio de janeiro', 'blumenau', 'paulinia',
       'belo horizonte', 'serra negra', 'cachoeirinha',
       'sao jose do rio preto', 'ribeirao preto', 'santo andre',
       'porto ferreira', 'curitiba', 'volta redonda', 'toledo',
       'campinas', 'guarulhos', 'guaratingueta', 'maua',
       'itaquaquecetuba', 'amparo', 'tupa', 'ribeirao pires',
       'campo limpo paulista', 'presidente prudente',
       'ferraz de  vasconcelos', 'jundiai', 'juiz de fora',
       'ribeirao das neves', 'barueri', 'maringa', 'rio claro',
       'joinville', 'sao paulop', 'taboao da serra', 'tiete', 'sorocaba',
       'goiania', 'nova trento', 'criciuma', 'marilia', 'recife',
       'sarandi', 'nova iguacu', 'venancio aires', 'vila velha',
       'sertanopolis', 'tres de maio', 'araucaria',
       'sao bernardo do capo', 'araguari', 'cotia', 'sao caetano do sul',
       'franca', 'guaira', 'santos', 'salto', 'jaragua do sul',
       'braganca paulista', 'vendas@creditparts.com.br', 'limeira',
       'garulhos', 'alambari', 'claudio', 'teresopolis', 'guariba',
       'sao jose dos pinhais', 'campos dos goytacazes', 'brasilia',
       'pouso alegre', 'rio negrinho', 'uba', 'carapicuiba',
       'ribeirao pretp', 'bertioga', 'borda da mata', 'araraquara',
       'campos novos', 'brasilia df', 'birigui', 'vicosa', 'bahia',
       'sao jose do rio pardo', 'itu', 'osasco', 'divinopolis', 'sinop',
       'jaci', 'florianopolis', 'barretos', 'são paulo',
       'sao bernardo do campo', 'cornelio procopio', 'santa cruz do sul',
       'poa', 'clementina', 'valinhos', 'sao carlos', 'cascavel',
       'petropolis', 'palhoca', 'mogi das cruzes', 'timoteo', 'mirassol',
       'pedreira', 'praia grande', 'rio do sul', 'ouro fino',
       'indaiatuba', 'jales', 'diadema', 'marechal candido rondon',
       'uberlandia', 'chapeco', 'igaracu do tiete', 'sao jose dos campos',
       'aracatuba', 'pinhalao', 'manaus', 'ribeirao preto / sao paulo',
       'nova friburgo', 'caucaia', 'macatuba', 'loanda', 'fortaleza',
       'rio bonito', 'ferraz de vasconcelos', 'taio', 'sombrio',
       'mesquita', 'campo grande', 'indaial', 'umuarama', 'londrina',
       'niteroi', 'itajobi', 'ipatinga', 'vitoria',
       'carapicuiba / sao paulo', 'sao paulo - sp', 'congonhal',
       'lencois paulista', 'bady bassitt', 'apucarana', 'botucatu',
       'anapolis', 'parnamirim', 'mirandopolis', 'caxias do sul',
       'foz do iguacu', 'santa rita do sapucai', 'fazenda rio grande',
       'arapongas', 'boituva', 'taruma', 'santana de parnaiba', 'lorena',
       'presidente getulio', 'itaipulandia', 'americana', 'avare',
       'japira', 'carazinho', 'guaratuba', 'suzano', 'itapevi', 'bauru',
       'cachoeira do sul', 'coxim', 'viamao', 'gaspar', 'rio do oeste',
       'california', 'pinhais', 'votuporanga', 'varzea paulista', 'bage',
       'francisco beltrao', 'jacutinga', 'caruaru',
       'santa terezinha de itaipu', 'novo horizonte', 'itaborai', 'jau',
       "santa barbara d'oeste", 'rolandia', 'congonhas', 'laurentino',
       "sao miguel d'oeste", 'descalvado', 'curitibanos', 'canoas',
       'guanhaes', 'assis', 'fernandopolis', 'brusque',
       'sao bento do sul', 'mandaguacu', 'irati', 'cianorte', 'tabatinga',
       'vespasiano', 'barra mansa', 'sao pedro', 'itapema',
       'entre rios do oeste', 'mairinque', 'aruja', 'balneario camboriu',
       'ampere', 'piracicaba', 'sao goncalo', 'santo antonio de posse',
       'novo hamburgo', 'sapiranga', 'pilar do sul', 'jaguariuna',
       'andradas', 'itajai', 'tres coroas', 'registro', 'triunfo',
       'novo hamburgo, rio grande do sul, brasil', 'itaporanga',
       'nova odessa', 'santo angelo', 'araras', 'imbituva', 'santa maria',
       'pato bragado', 'tres coracoes', 'catanduva',
       'sao sebastiao da grama/sp', 'jaguaruna', 'buritama', 'navegantes',
       'colombo', 'sumare', 'jaboticabal', 'mogi guacu', 'piracanjuba',
       'barra velha', 'rodeio', 'pinhalzinho', 'varginha', 'mandirituba',
       'natal', 'sao jose', 'lagoa santa', 'parana', 'uniao da vitoria',
       'campo largo', 'jaragua', 'imbe', 'canoinhas', 'imbituba',
       'sabara', 'estancia velha', 'ilicinea', 'colatina', 'ponta grossa',
       'serra', 'pocos de caldas', 'sao leopoldo', 'andira-pr',
       'igrejinha', 'garopaba', 'mateus leme', 'patos de minas',
       'cananeia', 'contagem', 'uruacu', 'erechim',
       'governador valadares', 'pelotas', 'echapora', 'aguas claras df',
       'laranjeiras do sul', 'morrinhos', 'sao sebastiao', 'batatais',
       "arraial d'ajuda (porto seguro)", 'sao roque', 'ibirite', 'itauna',
       'gama', 'varzea alegre', 'jaciara', 'garca', 'cosmopolis',
       'bariri', 'afonso claudio', 'guaruja', 'robeirao preto', 'marica',
       'duque de caxias', 'macae', 'formosa', 'massaranduba', 'soledade',
       'bebedouro', 'francisco morato', 'votorantim',
       'scao jose do rio pardo', 'concordia', 'pedrinhas paulista',
       'baependi', 'santa barbara d´oeste', 'porto velho', 'jacarei',
       'joao pessoa', 'lagoa da prata', 'serrana', 'conchal',
       'mineiros do tiete', 'cerqueira cesar', 'sao joao de meriti',
       'rio das pedras', 'cuiaba', 'braco do norte', 'montes claros',
       'sao francisco do sul', 'capivari', 'teresina', 'tabao da serra',
       'icara', 'leme', 'penapolis', 'porto seguro', 'horizontina',
       'santa rosa', 'olimpia', 'tatui', 'jacarei / sao paulo',
       'juzeiro do norte', 'campo bom', 'bofete', 'alvares machado',
       'itabira', 'nilopolis', 'rio grande', 'cafelandia',
       'cariacica / es', 'betim', 'terra boa', 'rolante',
       'vargem grande do sul', 'porto belo', 'laranjal paulista', 'sp',
       'cajamar', 'irece', 'muqui', 'orlandia', 'vitoria de santo antao',
       'formosa do oeste', 'dores de campos', 'brotas', 'artur nogueira',
       'santo andre/sao paulo', 'itatiba', 'lajeado', 'rio verde',
       'condor', 'embu das artes', 'dracena', 'pradopolis', 'castro',
       'aracaju', 'pacatuba', 'itapeva', 'taubate', 'tubarao', 'uberaba',
       'itapetininga', 'queimados', 'caratinga', 'cordeiropolis',
       'alvorada', 'angra dos reis rj', 'rio de janeiro / rio de janeiro',
       'osvaldo cruz', 's jose do rio preto', 'ourinhos', 'farroupilha',
       'montenegro', 'salvador', 'angra dos reis', 'bento goncalves',
       'cachoeiro de itapemirim', 'fernando prestes',
       'campina das missoes', 'tambau', 'conselheiro lafaiete', 'lages',
       'engenheiro coelho', 'aperibe', 'pato branco', 'itau de minas',
       'jussara', 'socorro', 'paraiso do sul', 'holambra', 'tanabi',
       'fronteira', 'ipira', 'mogi mirim', 'itapecerica da serra',
       'bocaiuva do sul', 'hortolandia', 'bombinhas', 'sao ludgero',
       'belo horizont', 'cambe', 'cacador', 'passos', 'ararangua',
       'vargem grande paulista', 'camanducaia', 'torres', 'sbc/sp',
       'sao joaquim da barra', 'palotina', 'pedregulho', 'cariacica',
       'monte alegre do sul', 'feira de santana', 'pitangueiras',
       'nhandeara', 'marialva', 'sao luis',
       'rio de janeiro \\rio de janeiro', 'sao jose dos pinhas',
       'pompeia', 'guanambi', 'santa barbara d oeste', 'xanxere',
       'muriae', 'maua/sao paulo', 'pinhais/pr', 'cravinhos',
       'lages - sc', 'presidente epitacio', 'ibia', 'embu guacu',
       'guiricema', 'mucambo', 'araxa', 'colorado', 'campina grande',
       'resende', 'luziania', 'ubatuba', 'neopolis', 'monte alto',
       'sete lagoas', 'campo magro', 'sao miguel do oeste', 'orleans',
       'armacao dos buzios', 'mombuca', 'mage', 'sando andre',
       'joao pinheiro', 'ji parana', 'sao jose do rio pret', 'uruguaiana',
       'centro', 'brejao', 'pitanga', 'santo antonio de padua',
       'flores da cunha', 'araquari', 'guarapuava', 'jambeiro',
       'ponte nova', 'campo do meio', 'eunapolis', 'ao bernardo do campo',
       'riberao preto', 'floranopolis', 'abadia de goias', 'louveira',
       'cascavael', 'pedro leopoldo', 'sao joao del rei', 'carmo da mata',
       'aparecida', 'saquarema', 'santa maria da serra',
       'coronel fabriciano', 'santa rosa de viterbo', 'mococa',
       'floresta', 'pirituba', 'mairipora', 'laguna', 'paracambi',
       'arinos', 'paraiba do sul', 'dois corregos', 'campanha'])
            customer_city_mode = st.select_box("customer_city_mode", 
                                               ['sao paulo', 'eldorado', 'fortaleza', 'rio de janeiro', 'marau',
       'ituiutaba', 'niteroi', 'ribeirao preto', 'brasilia', 'recife',
       'sao jose dos campos', 'olimpia', 'itapeva',
       'ferraz de vasconcelos', 'goiania', 'cachoeirinha', 'londrina',
       'contagem', 'barauna', 'suzano', 'osasco', 'tatui', 'assis',
       'itabira', 'jacarei', 'mogi das cruzes', 'arinos', 'guarulhos',
       'pedreira', 'hortolandia', 'vitoria da conquista', 'amparo',
       'camacari', 'itajobi', 'barra mansa', 'caxias do sul',
       'belo horizonte', 'corumba', 'campinas', 'florianopolis',
       'porto alegre', 'sao bernardo do campo', 'embu das artes',
       'bertioga', 'goioere', 'nova iguacu', 'petropolis', 'cataguases',
       'ijui', 'guararema', 'joinville', 'diadema', 'jaragua do sul',
       'joao pessoa', 'varzea grande', 'venancio aires',
       'santa cruz do rio pardo', 'chopinzinho', 'viradouro',
       'capao da canoa', 'campos dos goytacazes', 'caete', 'areal',
       'timoteo', 'salvador', 'palmitos', 'cacu', 'chapeco', 'caratinga',
       'ouroeste', 'viamao', 'lagoa da confusao', 'garca',
       'cachoeiro de itapemirim', 'maringa', 'bombinhas', 'santo andre',
       'denise', 'blumenau', 'muriae', 'campo grande', 'teresopolis',
       'vitoria', 'santos', 'governador valadares', 'canoas', 'itajuba',
       'penapolis', 'rio grande', 'jundiai', 'divinopolis',
       'santana de parnaiba', 'cachoeira do sul', 'barueri', 'limeira',
       'alto do rodrigues', 'paracatu', 'ibiuna', 'curitiba', 'alvorada',
       'sao vicente', 'agua doce', 'morrinhos', 'picarra', 'cotia',
       'vinhedo', 'poa', 'itumbiara', 'araraquara', 'sorocaba', 'brotas',
       'maceio', 'itaberaba', 'castro', 'mato leitao', 'pitangueiras',
       'guaruja', 'redencao', 'patos de minas', 'campo mourao', 'buriti',
       'sao luis', 'sao jose', 'ji-parana', 'praia grande', 'avelar',
       'gravatal', 'feira de santana', 'itaquaquecetuba', 'paulinia',
       'aparecida de goiania', 'itanhaem', 'rio negrinho',
       'alta floresta', 'sananduva', 'campo verde', 'presidente prudente',
       'sao leopoldo', 'piracicaba', 'campo limpo paulista', 'cascavel',
       'marilia', 'itaperuna', 'candeias do jamari', 'rio verde',
       'colombo', 'abrantes', 'teresina', 'campina grande', 'itamira',
       'atibaia', 'aracatuba', 'agua boa', 'camboriu',
       'almirante tamandare', 'cerro largo', 'anapolis',
       'entre rios de minas', 'nova prata', 'belem', 'guaratingueta',
       'espirito santo do pinhal', 'brazopolis', 'saquarema',
       'pires do rio', 'conceicao do coite', 'franca', 'farroupilha',
       'santa ines', 'luziania', 'olinda', 'bauru', 'juatuba', 'aracaju',
       'itatiba', 'americana', 'americo brasiliense', 'cafelandia',
       'rio do sul', 'pirapozinho', 'cordeiropolis', 'canela',
       'sao jose do rio pardo', 'apucarana', 'boa esperanca', 'birigui',
       'palmeira', 'rolandia', 'batatais', 'ataleia', 'angulo',
       'lauro de freitas', 'sao caetano do sul', 'inhumas', 'valinhos',
       'jesuania', 'dois irmaos', 'sete lagoas', 'cruzeiro do oeste',
       'alegrete', 'arraial do cabo', 'guacui', 'francisco morato',
       'currais novos', 'juiz de fora', 'gravatai', 'carapicuiba',
       'garuva', 'formiga', 'caraguatatuba', 'vila velha', 'arcos',
       'palmas', 'itirucu', 'mongagua', 'bento goncalves',
       'balneario camboriu', 'andradas', 'bom repouso', 'arandu',
       'sao manuel', 'pelotas', 'itamonte', 'nova prata do iguacu',
       'santa maria', 'santana do mundau', 'ico', 'garopaba', 'cacapava',
       'aruja', 'cabo frio', 'belford roxo', 'sao joao del rei',
       'bebedouro', 'ilheus', 'salto', 'balsas', 'bage',
       'cerqueira cesar', 'canelinha', 'joao monlevade', 'jaguarao',
       'criciuma', 'araruama', 'novo hamburgo', 'camaragibe', 'ampere',
       'pinheiral', 'pouso alegre', 'rio das ostras', 'pinhais',
       'rio novo', 'macae', 'floresta', 'icara', 'itaqui', 'tubarao',
       'manhuacu', 'itapirapua', 'aracariguama', 'duque de caxias',
       'lavras da mangabeira', 'sao joao nepomuceno', 'tapiratiba',
       'arapongas', 'garanhuns', 'serra', 'pindamonhangaba', 'bom jesus',
       'carai', 'cidade gaucha', 'cuiaba', 'barra do garcas', 'caruaru',
       'araxa', 'sao jose dos pinhais', 'uniao da vitoria', 'panambi',
       'cubatao', 'itapetininga', 'piedade', 'capela do alto',
       'campo novo do parecis', 'clevelandia', 'sao carlos',
       'santa branca', 'rio branco', 'itabuna', 'cocal',
       'engenheiro beltrao', 'mogi mirim', 'barra velha',
       'conselheiro lafaiete', 'areia', 'itariri', 'ipiau',
       'montes claros', 'formosa', 'matao', 'quatro bocas', 'ibipora',
       'cachoeiras de macacu', 'bacabal', 'casimiro de abreu',
       'natividade', 'barretos', 'brumado', 'aracati', 'barreiras',
       'xangri-la', 'francisco beltrao', 'angatuba', 'nilopolis',
       'santana do livramento', 'canto do buriti', 'gouveia',
       'brumadinho', 'estancia', 'taubate', 'ponta grossa',
       'angra dos reis', 'catanduva', 'pirapora', 'cidelandia',
       'araucaria', 'sao joao da boa vista', 'alcinopolis', 'brusque',
       'planaltino', 'engenheiro balduino', 'vilhena', 'balbinos',
       'pontalina', 'passira', 'carlos barbosa', 'erechim', 'medianeira',
       'jequie', 'sao jose do vale do rio preto', 'pereira barreto',
       'itapira', 'santiago', 'conceicao', 'itambacuri', 'rio claro',
       'uibai', 'crixas', 'caldas novas', 'teofilo otoni', 'tijucas',
       'pompeia', 'itu', 'caieiras', 'pederneiras', 'espera feliz',
       'guaxupe', 'itapolis', 'manaus', 'candeias', 'parelhas',
       'barbacena', 'aparecida do taboado', 'lins', 'porto velho',
       'sao jose do rio preto', 'mairipora', 'barra de sao francisco',
       'itacare', 'nipoa', 'siqueira campos', 'baixo guandu', 'timbo',
       'icem', 'belo oriente', 'cornelio procopio', 'cicero dantas',
       'votuporanga', 'castelo', 'paraguacu paulista', 'cianorte',
       'botucatu', 'extrema', 'bocaiuva', 'caconde', 'paraiba do sul',
       'bambui', 'uberlandia', 'santana', 'alvaro de carvalho', 'araras',
       'arapiraca', 'sao goncalo', 'nova serrana', 'sao joao de meriti',
       'sao mateus', 'camanducaia', 'ouro preto', 'ariranha',
       'nova friburgo', 'capinzal', 'caicara do norte', 'barra bonita',
       'aragarcas', 'nova odessa', 'agrestina', 'sao jose do hortencio',
       'queimados', 'marica', 'buritizeiro', 'apuiares',
       'riachao das neves', 'campo largo', 'araguaina', 'capitolio',
       'natal', 'maua', 'alem paraiba', 'itupeva', 'louveira',
       'imigrante', 'dourados', 'indaiatuba', 'ipatinga', 'bacaxa',
       'alto parana', 'picos', 'bom sucesso', 'iati', 'teutonia',
       'varginha', 'pesqueira', 'ibia', 'uruguaiana', 'jordania',
       'sabino', 'porto ferreira', 'lavras', 'itamarandiba',
       'sao jose de uba', 'jandaia do sul', 'curvelo', 'corupa', 'penha',
       'vazante', 'sao lourenco do piaui', 'esmeraldas', 'eunapolis',
       'cha grande', 'cajamar', 'imbe', 'planaltina', 'barra do pirai',
       'andira', 'mage', 'careacu', 'uirauna', 'navegantes',
       'aracoiaba da serra', 'campanha', 'alexandria', 'acreuna',
       "herval d'oeste", 'castanhal', 'mata de sao joao', 'xanxere',
       'peixoto de azevedo', 'itaborai', 'lagoa grande',
       "arraial d'ajuda", 'volta redonda', 'agua doce do norte',
       'santa monica', 'nova lima', 'novo cruzeiro', 'ilhabela',
       'boituva', 'canapolis', 'peruibe', 'registro', 'itajai',
       'nova europa', 'raposo', 'adamantina', 'benedito novo',
       'afonso claudio', 'ajuricaba', 'jacobina', 'sao domingos do prata',
       'abreu e lima', 'para de minas', 'campos novos', 'novo horizonte',
       'irece', 'lagoa santa', 'mandaguari', 'sobral', 'votorantim',
       'miranda', 'piranga', 'canoinhas', 'porteirinha', 'artur nogueira',
       'guapimirim', 'boa vista', 'cruzeiro', 'itaguai', 'japeri', 'leme',
       'jandira', 'flores da cunha', 'lajeado', "santa barbara d'oeste",
       'fazenda rio grande', 'santo antonio de padua', 'ituverava',
       'caetanopolis', 'foz do iguacu', 'sao mamede', 'bom jesus da lapa',
       'holambra', 'braganca paulista', 'dracena', 'pocos de caldas',
       'betim'])
            customer_state_mode = st.select_box("customer_state_mode", 
                                                ['SP', 'CE', 'RS', 'RJ', 'MG', 'PR', 'GO', 'BA', 'DF', 'MS', 'SC',
       'PB', 'MT', 'TO', 'ES', 'PA', 'AL', 'PE', 'MA', 'RO', 'AC', 'PI',
       'SE', 'AM', 'AP', 'RN'])

        with col_cat2:
            seller_state_mode = st.select_box("seller_state_mode", 
                                              ['SC', 'RS', 'SP', 'MG', 'RJ', 'PR', 'GO', 'PE', 'ES', 'DF', 'BA',
       'MT', 'AM', 'CE', 'MS', 'RN', 'RO', 'PB', 'PI', 'SE', 'MA'])
            payment_type_mode = st.select_box("payment_type_mode", 
                                              ['credit_card', 'boleto', 'voucher', 'debit_card'])
            order_status_mode = st.select_box("order_status_mode", 
                                              ['delivered', 'canceled', 'shipped'])
            product_category_name_english_mode = st.select_box(
                "product_category_name_english_mode",
                ['sports_leisure', 'fashion_bags_accessories', 'furniture_decor',
       'housewares', 'health_beauty', 'auto', 'air_conditioning', 'toys',
       'baby', 'furniture_living_room', 'cool_stuff',
       'construction_tools_lights', 'computers_accessories',
       'small_appliances', 'construction_tools_construction',
       'books_general_interest', 'bed_bath_table', 'perfumery',
       'stationery', 'garden_tools', 'watches_gifts', 'home_appliances',
       'construction_tools_safety', 'food', 'telephony', 'pet_shop',
       'musical_instruments', 'electronics', 'consoles_games',
       'costruction_tools_garden', 'home_confort', 'drinks', 'art',
       'audio', 'furniture_bedroom', 'books_technical',
       'kitchen_dining_laundry_garden_furniture',
       'fashio_female_clothing', 'fixed_telephony', 'home_appliances_2',
       'cine_photo', 'market_place', 'luggage_accessories',
       'home_construction', 'furniture_mattress_and_upholstery',
       'office_furniture', 'food_drink', 'industry_commerce_and_business',
       'costruction_tools_tools', 'party_supplies',
       'fashion_underwear_beach', 'computers', 'arts_and_craftmanship',
       'dvds_blu_ray', 'fashion_sport', 'agro_industry_and_commerce',
       'diapers_and_hygiene', 'signaling_and_security', 'music',
       'la_cuisine', 'christmas_supplies', 'books_imported',
       'small_appliances_home_oven_and_coffee', 'fashion_shoes',
       'fashion_male_clothing', 'tablets_printing_image']
            )

        submitted = st.form_submit_button("Prediksi Risiko Churn")

    # Setelah form disubmit
    if submitted:
        data_dict = {
            "product_id_nunique": [product_id_nunique],
            "price_min": [price_min],
            "freight_value_min": [freight_value_min],
            "freight_value_max": [freight_value_max],
            "payment_installments_min": [payment_installments_min],
            "payment_installments_max": [payment_installments_max],
            "payment_installments_median": [payment_installments_median],
            "payment_value_min": [payment_value_min],
            "payment_value_sum": [payment_value_sum],
            "review_score_min": [review_score_min],
            "product_description_lenght_min": [product_description_lenght_min],
            "product_description_lenght_max": [product_description_lenght_max],
            "product_photos_qty_min": [product_photos_qty_min],
            "product_photos_qty_max": [product_photos_qty_max],
            "product_weight_g_min": [product_weight_g_min],
            "product_weight_g_max": [product_weight_g_max],
            "product_weight_g_median": [product_weight_g_median],
            "product_length_cm_min": [product_length_cm_min],
            "product_height_cm_min": [product_height_cm_min],
            "product_height_cm_max": [product_height_cm_max],
            "product_width_cm_max": [product_width_cm_max],
            "seller_customer_distance_km_min": [seller_customer_distance_km_min],
            "seller_customer_distance_km_max": [seller_customer_distance_km_max],
            "seller_customer_distance_km_median": [seller_customer_distance_km_median],
            "seller_review_response_hours_min": [seller_review_response_hours_min],
            "seller_review_response_hours_max": [seller_review_response_hours_max],
            "seller_review_response_hours_mean": [seller_review_response_hours_mean],
            "seller_lead_time_approval_hours_min": [seller_lead_time_approval_hours_min],
            "seller_lead_time_approval_hours_max": [seller_lead_time_approval_hours_max],
            "seller_lead_time_approval_hours_median": [seller_lead_time_approval_hours_median],
            "seller_buffer_time_days_min": [seller_buffer_time_days_min],
            "seller_buffer_time_days_max": [seller_buffer_time_days_max],
            "seller_buffer_time_days_mean": [seller_buffer_time_days_mean],
            "freight_gmv_ratio": [freight_gmv_ratio],
            "price_range": [price_range],
            "price_range_normalized": [price_range_normalized],
            "account_age": [account_age],
            "Activity_Rate": [Activity_Rate],
            "seller_city_mode": [seller_city_mode],
            "customer_city_mode": [customer_city_mode],
            "customer_state_mode": [customer_state_mode],
            "seller_state_mode": [seller_state_mode],
            "payment_type_mode": [payment_type_mode],
            "order_status_mode": [order_status_mode],
            "product_category_name_english_mode": [product_category_name_english_mode],
        }

        df_input = pd.DataFrame(data_dict)

        st.markdown("### Ringkasan Data Seller")
        st.dataframe(df_input, use_container_width=True)

        try:
            # probabilitas churn
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(df_input)[0][1]
            else:
                proba = float(model.predict(df_input)[0])

            pred = model.predict(df_input)[0]

            # Card di bagian atas
            churn_prob_placeholder.metric(
                "Probabilitas Churn",
                f"{proba:.2%}",
            )

            if pred == 1:
                churn_label_placeholder.markdown(
                    "<div style='padding:10px;border-radius:8px;background-color:#ffe5e5;color:#b00020;'>"
                    "<b>Status:</b> Seller berisiko churn"
                    "</div>",
                    unsafe_allow_html=True,
                )
                note_placeholder.markdown(
                    """
                    **Rekomendasi awal:**
                    - Evaluasi kualitas layanan dan waktu pengiriman.
                    - Buat program retensi, misalnya insentif atau promo khusus.
                    - Pantau kembali dalam periode waktu pendek.
                    """
                )
                st.error("SELLER BERISIKO CHURN")
            else:
                churn_label_placeholder.markdown(
                    "<div style='padding:10px;border-radius:8px;background-color:#e6f4ea;color:#1e4620;'>"
                    "<b>Status:</b> Seller tidak berisiko churn"
                    "</div>",
                    unsafe_allow_html=True,
                )
                note_placeholder.markdown(
                    """
                    **Catatan:**
                    - Pertahankan kualitas layanan dan performa seller.
                    - Seller tetap perlu dimonitor jika terjadi penurunan aktivitas.
                    """
                )
                st.success("SELLER TIDAK BERISIKO CHURN")

            st.markdown("#### Interpretasi Probabilitas")
            st.markdown(
                """
                - Di bawah 0.30: Risiko churn rendah.  
                - 0.30 sampai 0.60: Risiko churn sedang.  
                - Di atas 0.60: Risiko churn tinggi, perlu tindakan retensi.
                """
            )

        except Exception as e:
            st.error("Error saat prediksi.")
            st.exception(e)

with tab_doc:
    st.subheader("Panduan Singkat Penggunaan Data")

    st.markdown(
        """
        Halaman ini berisi ringkasan batas nilai data yang digunakan model.  
        Tujuannya agar admin tahu apakah data seller yang dicek masih berada di kisaran yang wajar.
        """
    )

    st.markdown("### 1. Batas Nilai Fitur Angka (Numerik)")

    st.markdown(
        """
        Nilai di bawah ini adalah kisaran data yang dipakai saat model dibuat.  
        Jika nilai yang dimasukkan jauh di luar kisaran ini, hasil prediksi bisa kurang akurat.
        """
    )

    with st.expander("Lihat tabel batas nilai fitur numerik"):
        st.markdown(
            """
            | Kriteria (Fitur)                   | Rentang Nilai (min - max) | Keterangan Singkat                                 |
            | ---------------------------------- | ------------------------- | -------------------------------------------------- |
            | product_id_nunique                 | 1.00 - 129.60             | Jumlah produk unik yang pernah dijual seller       |
            | price_min                          | 0.85 - 1299.00            | Harga terendah produk seller                       |
            | freight_value_min                  | 0.00 - 71.04              | Ongkir minimum per item                            |
            | freight_value_max                  | 0.75 - 218.70             | Ongkir maksimum per item                           |
            | payment_installments_min           | 0 - 10                    | Cicilan minimum                                    |
            | payment_installments_max           | 1 - 20                    | Cicilan maksimum                                   |
            | payment_installments_median        | 1 - 10                    | Cicilan yang paling sering terjadi                 |
            | payment_value_min                  | 0.00 - 1336.98            | Nilai pembayaran terkecil per pesanan              |
            | payment_value_sum                  | 18.56 - 78,346.48         | Total nilai pembayaran per seller                   |
            | review_score_min                   | 1 - 5                     | Nilai review terendah                              |
            | product_description_lenght_min     | 4 - 3992                  | Panjang deskripsi produk terpendek                 |
            | product_description_lenght_max     | 4 - 3992                  | Panjang deskripsi produk terpanjang                |
            | product_photos_qty_min             | 1 - 14                    | Jumlah foto minimum                                |
            | product_photos_qty_max             | 1 - 20                    | Jumlah foto maksimum                               |
            | product_weight_g_min               | 2 - 21,490                | Berat produk paling ringan                         |
            | product_weight_g_max               | 50 - 30,000               | Berat produk paling berat                          |
            | product_weight_g_median            | 2 - 24,615                | Berat produk yang paling umum                      |
            | product_length_cm_min              | 7 - 89                    | Panjang produk minimum                             |
            | product_height_cm_min              | 2 - 62                    | Tinggi produk minimum                              |
            | product_height_cm_max              | 2 - 96.30                 | Tinggi produk maksimum                             |
            | product_width_cm_max               | 8 - 90                    | Lebar produk maksimum                              |
            | seller_customer_distance_km_min    | 0.00 - 2073.33            | Jarak pelanggan terdekat                           |
            | seller_customer_distance_km_max    | 1.14 - 3289.06            | Jarak pelanggan terjauh                            |
            | seller_customer_distance_km_median | 1.14 - 2221.45            | Jarak pelanggan yang paling umum                   |
            | seller_review_response_hours_min   | 2.42 - 148.42             | Respon tercepat ke review atau komplain            |
            | seller_review_response_hours_max   | 4.07 - 5711.14            | Respon terlambat ke review atau komplain           |
            | seller_review_response_hours_mean  | 4.07 - 363.85             | Rata-rata waktu respon review atau komplain        |
            | seller_lead_time_approval_hours_min| 0.00 - 43.22              | Persetujuan order tercepat                         |
            | seller_lead_time_approval_hours_max| 0.00 - 258.09             | Persetujuan order terlambat                        |
            | seller_lead_time_approval_hours_median | 0.00 - 64.30          | Waktu persetujuan yang paling umum                 |
            | seller_buffer_time_days_min        | -117.00 - 19.00           | Selisih tercepat antara janji kirim dan realisasi  |
            | seller_buffer_time_days_max        | -46.00 - 1046.00          | Selisih terlambat antara janji kirim dan realisasi |
            | seller_buffer_time_days_mean       | -46.00 - 32.17            | Rata-rata selisih janji kirim dan realisasi        |
            | freight_gmv_ratio                  | 0.0015 - 0.5127           | Porsi ongkir terhadap nilai pesanan                |
            | price_range                        | 0.00 - 2198.72            | Rentang harga produk di seller                     |
            | price_range_normalized             | 0.00 - 9.44               | Versi berskala dari rentang harga                  |
            | account_age                        | 31 - 703                  | Umur akun seller (hari)                            |
            | Activity_Rate                      | 0.0014 - 0.9536           | Seberapa aktif seller selama periode data          |
            """,
            unsafe_allow_html=False,
        )

    st.markdown(
        """
        **Ringkasnya:**  
        Jika angka yang dimasukkan masih kurang lebih di dalam kisaran ini, model bekerja lebih stabil.
        """
    )

    st.markdown("### 2. Batas Nilai Fitur Kategorikal")

    st.markdown(
        """
        Untuk kolom kategori, model bekerja paling baik jika admin memakai nilai yang sudah dikenal model dari data sebelumnya.  
        Jika muncul kota, provinsi, atau jenis pembayaran yang baru, model tetap bisa memprediksi tetapi hasilnya bisa kurang tepat.
        """
    )

    with st.expander("Lihat ringkasan kategori yang digunakan model"):
        st.markdown(
            """
            | Fitur Kategorikal                | Contoh Nilai yang Digunakan Model                                                                                             | Catatan untuk Admin                             |
            | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
            | seller_city_mode                 | Nama kota seller yang sudah ada di data historis                                                                             | Kota baru dianggap kategori baru                 |
            | seller_state_mode                | SC, RS, SP, MG, RJ, PR, GO, PE, ES, DF, BA, MT, AM, CE, MS, RN, RO, PB, PI, SE, MA                                           | Gunakan kode provinsi yang konsisten             |
            | order_status_mode                | delivered, canceled, shipped                                                                                                  | Status lain tidak digunakan model                |
            | payment_type_mode                | credit_card, boleto, voucher, debit_card                                                                                      | Metode baru mungkin kurang akurat                |
            | product_category_name_english_mode | Nama kategori produk yang pernah ada di data historis                                                                        | Kategori baru → akurasi bisa turun               |
            | customer_city_mode               | Kota customer dari data historis                                                                                              | Kota baru dianggap kategori baru                 |
            | customer_state_mode              | SP, CE, RS, RJ, MG, PR, GO, BA, DF, MS, SC, PB, MT, TO, ES, PA, AL, PE, MA, RO, AC, PI, SE, AM, AP, RN                      | Pastikan kode provinsi sesuai                    |
            """,
            unsafe_allow_html=False,
        )

    st.markdown(
        """
        **Ringkasnya:**  
        Semakin mirip data yang dimasukkan dengan data historis, semakin bisa dipercaya hasil prediksinya.
        """
    )

    st.markdown("### 3. Catatan Praktis untuk Admin")

    st.markdown(
        """
        - Model melihat pola dari data historis, bukan masa depan yang pasti.  
        - Seller yang sangat baru bisa menghasilkan prediksi kurang stabil.  
        - Perubahan besar seperti promo besar atau kebijakan baru belum tentu tercermin di model.  
        - Gunakan hasil model sebagai **indikasi risiko**, bukan satu-satunya dasar keputusan.
        """
    )
