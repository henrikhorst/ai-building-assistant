from openai import OpenAI
import streamlit as st
import helper_app

st.set_page_config(page_title="🏗️ AI Building Assistant🤖")

st.title("🏗️ AI Building Assistant🤖")



client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


if "openai_model" not in st.session_state:
    st.session_state["model"] = "gpt-4-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": helper_app.system_prompt_2},
      ]

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Wie kann ich helfen?"):
    
    with st.chat_message("user"):
        st.markdown(question)
    
    


    with st.chat_message("assistant"):
        responses = helper_app.execute_processing(helper_app.pdf_files_content, question, helper_app.system_prompt_1, client)
        info_str = ""
        for k, completion in responses:
            info_str+= "\n\n---------\n\n" + completion.choices[0].message.content
        content ="Information:\n" + info_str + "\n\n-----------\n\n" + "Nutze die bereitgestellten Informationen, um mit den relevanten Informationen die Anfrage nutzerfreundlich zu beantworten. Die Anfrage ist: \n" +question
        
        stream = client.chat.completions.create(
            model=st.session_state["model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]+[{"role": "user", "content": content}],
            temperature=0.0,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": response})