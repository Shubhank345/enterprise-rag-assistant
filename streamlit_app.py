import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# PAGE SETTINGS
st.set_page_config(
    page_title="Enterprise RAG Assistant",
    layout="wide"
)

# TITLE
st.title("Enterprise RAG Assistant")

st.markdown(
    "Upload PDF or TXT documents and chat with AI"
)

# CHAT HISTORY
if "messages" not in st.session_state:

    st.session_state.messages = []

# FILE UPLOAD
uploaded_files = st.file_uploader(
    "Upload PDF or TXT Files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

# PROCESS DOCUMENTS
if uploaded_files:

    if st.button("Process Documents"):

        files = []

        for file in uploaded_files:

            files.append(
                (
                    "files",
                    (
                        file.name,
                        file,
                        file.type
                    )
                )
            )

        with st.spinner(
            "Processing documents..."
        ):

            response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

        st.success(
            "Documents Processed Successfully"
        )

# DISPLAY CHAT HISTORY
for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

# CHAT INPUT
question = st.chat_input(
    "Ask a question"
)

# USER QUESTION
if question:

    # SAVE USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # SHOW USER MESSAGE
    with st.chat_message("user"):

        st.write(question)

    # SEND TO FASTAPI
    with st.spinner("Thinking..."):

        response = requests.post(
            f"{API_URL}/ask",
            json={
                "question": question
            }
        )

    data = response.json()

    answer = data.get(
        "answer",
        "No response generated"
    )

    # SHOW AI RESPONSE
    with st.chat_message("assistant"):

        st.write(answer)

        # SOURCES
        with st.expander("View Sources"):

            for idx, source in enumerate(
                data.get("sources", [])
            ):

                st.markdown(
                    f"### Source {idx+1}"
                )

                # SOURCE TEXT
                st.write(
                    source["content"]
                )

                # METADATA
                metadata = source.get(
                    "metadata",
                    {}
                )

                if metadata:

                    st.write(
                        f"Source File: {metadata.get('source', 'Unknown')}"
                    )

                    if "page" in metadata:

                        st.write(
                            f"Page: {metadata['page']}"
                        )

                else:

                    st.write(
                        "No metadata available"
                    )

                st.divider()

    # SAVE ASSISTANT RESPONSE
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })