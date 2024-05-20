import streamlit as st
import numpy as np
import keras
import pandas as pd
from data_processing import encode, sequenced, truncate, c_position_list

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
        # position = int(st.text_input("Position of Cystiene Residue", "10"))
        amino_acid_sequence = sequenced(accession)
        position_list = c_position_list(amino_acid_sequence)
        truncated_sequence_list = []
        encoded_sequence_list = []
        for pos in position_list:
            truncated = truncate(amino_acid_sequence, pos, 100)
            truncated_sequence_list.append(truncated[80:120])
            encoded_sequence_list.append(encode(truncated))


    else:
        st.write("""#### Enter a raw sequence ####""")
        raw_sequence = st.text_area(
            "Raw Sequence", 
            "MTLESIMACCLSEEAKEARRINDEIERHVRRDKRDARRELKLLLLGTGESGKSTFIKQMRIIHGSGYSDEDKRGFTKLVYQNIFTAMQAMIRAMDTLKIPYKYEHNKAHAQLVREVDVEKVSAFENPYVDAIKSLWNDPGIQECYDRRREYQLSDSTKYYLNDLDRVADPSYLPTQQDVLRVRVPTTGIIEYPFDLQSVIFRMVDVGGQRSERRKWIHCFENVTSIMFLVALSEYDQVLVESDNENRMEESKALFRTIITYPWFQNSSVILFLNKKDLLEEKIMYSHLVDYFPEYDGPQRDAQAAREFILKMFVDLNPDSDKIIYSHFTCATDTENIRFVFAAVKDTILQLNLKEYNLV").strip(" ")
        # position = int(st.text_input("Position of Cystiene Residue", "10"))
        position_list = c_position_list(raw_sequence)
        truncated_sequence_list = []
        encoded_sequence_list = []
        for pos in position_list:
            truncated = truncate(raw_sequence, pos, 100)
            truncated_sequence_list.append(truncated[80:120])
            encoded_sequence_list.append(encode(truncated))
    
    input = np.array(encoded_sequence_list)
    
    ok = st.button("S Palmitoylation Site Predictions for all Cystiene Residues")


    data = load_model()


    output = data(input)["output_0"].numpy()
    

    table = {
        "Position": position_list,
        "Likeliness of being an S Palmitoylation Site": [str(round(i[0] * 100, 2)) + "%" for i in output.tolist()],
        "Truncated Sequence": truncated_sequence_list
    }
    df = pd.DataFrame(table)

    if ok:
        st.subheader(f"S Palmitoylation Site Prediction for all Cystiene Residues")
        st.table(df)
