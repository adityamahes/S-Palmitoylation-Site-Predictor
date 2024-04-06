import streamlit as st
import numpy as np
import keras
from data_processing import encode, sequenced, truncate

def load_model():
    data = keras.layers.TFSMLayer(filepath='S_Palmitoylation_Modelexport', call_endpoint='serving_default')
    return data

def show_predict_page():
    st.title("S Palmitoylation Site Prediction")

    st.write("""### Select the type of input  ###""")

    type_input = st.selectbox("Type", ("Accession", "Raw Sequence"))

    if type_input == "Accession":
        st.write("""#### Enter the following ####""")
        accession = st.text_input("Accession", "P21279")
        position = int(st.text_input("Position of Cystiene Residue", "10"))
        truncated_sequence = truncate(sequenced(accession), position, 100)

        try:
            input = np.array([encode(truncated_sequence)])
        except:
            st.write("""###### Invalid Sequence ######""")
    else:
        st.write("""#### Enter a raw sequence ####""")
        raw_sequence = st.text_area(
            "Raw Sequence", 
            "MTLESIMACCLSEEAKEARRINDEIERHVRRDKRDARRELKLLLLGTGESGKSTFIKQMRIIHGSGYSDEDKRGFTKLVYQNIFTAMQAMIRAMDTLKIPYKYEHNKAHAQLVREVDVEKVSAFENPYVDAIKSLWNDPGIQECYDRRREYQLSDSTKYYLNDLDRVADPSYLPTQQDVLRVRVPTTGIIEYPFDLQSVIFRMVDVGGQRSERRKWIHCFENVTSIMFLVALSEYDQVLVESDNENRMEESKALFRTIITYPWFQNSSVILFLNKKDLLEEKIMYSHLVDYFPEYDGPQRDAQAAREFILKMFVDLNPDSDKIIYSHFTCATDTENIRFVFAAVKDTILQLNLKEYNLV").strip(" ")
        position = int(st.text_input("Position of Cystiene Residue", "10"))
        truncated_sequence = truncate(raw_sequence, position, 100)

        try:
            input = np.array([encode(truncated_sequence)])
        except:
            st.write("""###### Invalid Sequence ######""")
    
    ok = st.button("Calculate Likeliness of Being an S Palmitoylation Site")

    data = load_model()
    print(data(input))
    output = data(input)["output_0"].numpy()[0][0] * 100
    if ok:
        st.subheader(f"The likeliness of it being an S Palmitoylation Site is {output:.2f}%")