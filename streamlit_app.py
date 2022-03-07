import streamlit as st
import time
import requests

from training_text import training

def main():
    credits = "Credit to [vicgalle](https://github.com/vicgalle) for the [GPT-J AI API](https://github.com/vicgalle/gpt-j-api), and [@loewhaley](https://www.tiktok.com/@loewhaley) for the idea and training translations."
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title="Professional Speak AI",
        page_icon="💼",
        menu_items={
         'About': "# Just for fun.\n"+credits
        }
    )
    st.title("👩🏾‍💼 Professional Speak AI")
    
    st.write("""Enter a sentence and the AI will attempt to make it more professional.
    \nYou can regenerate multiple times for different professional sentences.
    """)

    ex_names = [
        "I have no idea what I'm doing.",
        "I do not remember what you said.",
        "You've done this all wrong.",
    ]
    example = st.selectbox("Choose an example prompt here:", ex_names)
    
    inp = st.text_area(
        "Or write your own prompt here:", example, max_chars=2000, height=150
    )

    try:
        rec = ex_names.index(inp)
    except ValueError:
        rec = 0

    with st.expander("Generation options..."):
        temp = st.slider(
            "Choose the temperature (Higher is more random, will give you different results on regeneration; lower is more repetitive).",
            0.0,
            1.5,
            0.7,
            0.05,
        )

    response = None
    with st.form(key="inputs"):
        submit_button = st.form_submit_button(label="Generate!")

        if submit_button:
            with st.spinner('Thinking professionally...'):
                payload = {
                    "context": training+inp+"\nTranslation:",
                    "token_max_length": 100,
                    "temperature": temp,
                    "top_p": 0.9,
                    "stop_sequence": "\n###",
                }
                
                query = requests.post("http://api.vicgalle.net:5000/generate", params=payload)
                response = query.json()

                st.markdown(response["text"])
                if "compute_time" in response:
                    st.text(f"Generation done in {response['compute_time']:.3} s.")
                else:
                    st.text("Please try again later.")
                    st.markdown("This website is run for free. You can access the code on github to deploy it yourself, with less restricted limits.")
    st.markdown("""---
    \nMade by [clukes](https://github.com/clukes). View the [source code](https://github.com/clukes/professional_ai).
    \n"""+credits)

if __name__ == "__main__":
    main()
