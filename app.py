import streamlit as st
import pdf2image
from PIL import Image
import pytesseract
from pytesseract import Output, TesseractError
from functions import convert_pdf_to_txt_pages, convert_pdf_to_txt_file, save_pages, displayPDF, images_to_txt

st.set_page_config(page_title="PDF to Text")


html_temp = """
            <div style="background-color:{};padding:1px">
            
            </div>
            """

# st.markdown("""
#     ## :outbox_tray: Text data extractor: PDF to Text
    
# """)
# st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
st.markdown("""
    ## Text data extractor: PDF to Text
    
""")
languages = {
    'Afrikaans': 'afr',
    'Amharic': 'amh',
    'Arabic': 'ara',
    'Assamese': 'asm',
    'Azerbaijani': 'aze',
    'Azerbaijani - Cyrillic': 'aze_cyrl',
    'Belarusian': 'bel',
    'Bengali': 'ben',
    'Tibetan': 'bod',
    'Bosnian': 'bos',
    'Breton': 'bre',
    'Bulgarian': 'bul',
    'Catalan; Valencian': 'cat',
    'Cebuano': 'ceb',
    'Czech': 'ces',
    'Chinese - Simplified': 'chi_sim',
    'Chinese - Traditional': 'chi_tra',
    'Cherokee': 'chr',
    'Corsican': 'cos',
    'Welsh': 'cym',
    'Danish': 'dan',
    'Danish - Fraktur (contrib)': 'dan_frak',
    'German': 'deu',
    'German - Fraktur (contrib)': 'deu_frak',
    'German (Fraktur Latin)': 'deu_latf',
    'Dzongkha': 'dzo',
    'Greek, Modern (1453-)': 'ell',
    'English': 'eng',
    'English, Middle (1100-1500)': 'enm',
    'Esperanto': 'epo',
    'Math / equation detection module': 'equ',
    'Estonian': 'est',
    'Basque': 'eus',
    'Faroese': 'fao',
    'Persian': 'fas',
    'Filipino (old - Tagalog)': 'fil',
    'Finnish': 'fin',
    'French': 'fra',
    'German - Fraktur (now deu_latf)': 'frk',
    'French, Middle (ca.1400-1600)': 'frm',
    'Western Frisian': 'fry',
    'Scottish Gaelic': 'gla',
    'Irish': 'gle',
    'Galician': 'glg',
    'Greek, Ancient (to 1453) (contrib)': 'grc',
    'Gujarati': 'guj',
    'Haitian; Haitian Creole': 'hat',
    'Hebrew': 'heb',
    'Hindi': 'hin',
    'Croatian': 'hrv',
    'Hungarian': 'hun',
    'Armenian': 'hye',
    'Inuktitut': 'iku',
    'Indonesian': 'ind',
    'Icelandic': 'isl',
    'Italian': 'ita',
    'Italian - Old': 'ita_old',
    'Javanese': 'jav',
    'Japanese': 'jpn',
    'Kannada': 'kan',
    'Georgian': 'kat',
    'Georgian - Old': 'kat_old',
    'Kazakh': 'kaz',
    'Central Khmer': 'khm',
    'Kirghiz; Kyrgyz': 'kir',
    'Kurmanji (Kurdish - Latin Script)': 'kmr',
    'Korean': 'kor',
    'Korean (vertical)': 'kor_vert',
    'Kurdish (Arabic Script)': 'kur',
    'Lao': 'lao',
    'Latin': 'lat',
    'Latvian': 'lav',
    'Lithuanian': 'lit',
    'Luxembourgish': 'ltz',
    'Malayalam': 'mal',
    'Marathi': 'mar',
    'Macedonian': 'mkd',
    'Maltese': 'mlt',
    'Mongolian': 'mon',
    'Maori': 'mri',
    'Malay': 'msa',
    'Burmese': 'mya',
    'Nepali': 'nep',
    'Dutch; Flemish': 'nld',
    'Norwegian': 'nor',
    'Occitan (post 1500)': 'oci',
    'Oriya': 'ori',
    'Orientation and script detection module': 'osd',
    'Panjabi; Punjabi': 'pan',
    'Polish': 'pol',
    'Portuguese': 'por',
    'Pushto; Pashto': 'pus',
    'Quechua': 'que',
    'Romanian; Moldavian; Moldovan': 'ron',
    'Russian': 'rus',
    'Sanskrit': 'san',
    'Sinhala; Sinhalese': 'sin',
    'Slovak': 'slk',
    'Slovak - Fraktur (contrib)': 'slk_frak',
    'Slovenian': 'slv',
    'Sindhi': 'snd',
    'Spanish; Castilian': 'spa',
    'Spanish; Castilian - Old': 'spa_old',
    'Albanian': 'sqi',
    'Serbian': 'srp',
    'Serbian - Latin': 'srp_latn',
    'Sundanese': 'sun',
    'Swahili': 'swa',
    'Swedish': 'swe',
    'Syriac': 'syr',
    'Tamil': 'tam',
    'Tatar': 'tat',
    'Telugu': 'tel',
    'Tajik': 'tgk',
    'Tagalog (new - Filipino)': 'tgl',
    'Thai': 'tha',
    'Tigrinya': 'tir',
    'Tonga': 'ton',
    'Turkish': 'tur',
    'Uighur; Uyghur': 'uig',
    'Ukrainian': 'ukr',
    'Urdu': 'urd',
    'Uzbek': 'uzb',
    'Uzbek - Cyrillic': 'uzb_cyrl',
    'Vietnamese': 'vie',
    'Yiddish': 'yid',
    'Yoruba': 'yor'
}

with st.sidebar:
    st.title(":outbox_tray: PDF to Text")
    textOutput = st.selectbox(
        "How do you want your output text?",
        ('One text file (.txt)', 'Text file per page (ZIP)'))
    ocr_box = st.checkbox('Enable OCR (scanned document)')
    
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    # How does it work?
    Simply load your PDF and convert it to single-page or multi-page text.
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    Made by [@nainia_ayoub](https://twitter.com/nainia_ayoub) 
    """)
    st.markdown(
        """
        <a href="https://www.buymeacoffee.com/nainiayoub" target="_blank">
        <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174">
        </a>
        """,
        unsafe_allow_html=True,
    )
    

pdf_file = st.file_uploader("Load your PDF", type=['pdf', 'png', 'jpg'])
hide="""
<style>
footer{
	visibility: hidden;
    	position: relative;
}
.viewerBadge_container__1QSob{
  	visibility: hidden;
}
#MainMenu{
	visibility: hidden;
}
<style>
"""
st.markdown(hide, unsafe_allow_html=True)
if pdf_file:
    path = pdf_file.read()
    file_extension = pdf_file.name.split(".")[-1]
    
    if file_extension == "pdf":
        # display document
        with st.expander("Display document"):
            displayPDF(path)
        if ocr_box:
            option = st.selectbox('Select the document language', list(languages.keys()))
        # pdf to text
        if textOutput == 'One text file (.txt)':
            if ocr_box:
                texts, nbPages = images_to_txt(path, languages[option])
                totalPages = "Pages: "+str(nbPages)+" in total"
                text_data_f = "\n\n".join(texts)
            else:
                text_data_f, nbPages = convert_pdf_to_txt_file(pdf_file)
                totalPages = "Pages: "+str(nbPages)+" in total"

            st.info(totalPages)
            st.download_button("Download txt file", text_data_f)
        else:
            if ocr_box:
                text_data, nbPages = images_to_txt(path, languages[option])
                totalPages = "Pages: "+str(nbPages)+" in total"
            else:
                text_data, nbPages = convert_pdf_to_txt_pages(pdf_file)
                totalPages = "Pages: "+str(nbPages)+" in total"
            st.info(totalPages)
            zipPath = save_pages(text_data)
            # download text data   
            with open(zipPath, "rb") as fp:
                btn = st.download_button(
                    label="Download ZIP (txt)",
                    data=fp,
                    file_name="pdf_to_txt.zip",
                    mime="application/zip"
                )
    else:
        option = st.selectbox("What's the language of the text in the image?", list(languages.keys()))
        pil_image = Image.open(pdf_file)
        text = pytesseract.image_to_string(pil_image, lang=languages[option])
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Display Image"):
                st.image(pdf_file)
        with col2:
            with st.expander("Display Text"):
                st.info(text)
        st.download_button("Download txt file", text)

    st.markdown('''
    <a target="_blank" style="color: black" href="https://twitter.com/intent/tweet?text=You%20can%20extract%20text%20from%20your%20PDF%20using%20this%20PDF%20to%20Text%20streamlit%20app%20by%20@nainia_ayoub!%0A%0Ahttps://nainiayoub-pdf-text-data-extractor-app-p6hy0z.streamlit.app/">
        <button class="btn">
            Spread the word!
        </button>
    </a>
    <style>
    .btn{
        display: inline-flex;
        -moz-box-align: center;
        align-items: center;
        -moz-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        margin: 0px;
        line-height: 1.6;
        color: rgb(49, 51, 63);
        background-color: #fff;
        width: auto;
        user-select: none;
        border: 1px solid rgba(49, 51, 63, 0.2);
        }
    .btn:hover{
        color: #00acee;
        background-color: #fff;
        border: 1px solid #00acee;
    }
    </style>
    ''',
    unsafe_allow_html=True
    )
    
