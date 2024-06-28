import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import glob
# bring in deps
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
# Create the directory if it doesn't exist
def file_accept():
    output_dir = 'data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
    
        # Save the file to the specified directory
        with open(os.path.join(output_dir, uploaded_file.name), 'wb') as f:
            f.write(bytes_data)
    
        st.write("filename:", uploaded_file.name)
        # st.write(bytes_data)

def file_ask(query1):
    parser = LlamaParse(
        result_type="markdown"  # "markdown" and "text" are available
    )
    input_files = glob.glob('data/*')
# use SimpleDirectoryReader to parse our file
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(input_files=input_files, file_extractor=file_extractor).load_data()

    index = VectorStoreIndex.from_documents(documents)

# create a query engine for the index
    query_engine = index.as_query_engine()

# query the engine
    # query = "Give me a summary of the entire document"
    response = query_engine.query(query1)
    return response

def main():
    st.title("DocDecoder")
    
    # User input
    st.write("Hi, I am a Document Query Bot. Upload any file in pdf format and then, ask me anything!")
    st.write("Enter your files")
    file_accept()
    # Ask me button
    location=st.text_input("Now ask me anything from the document.")
    if st.button("Ask me"):
        # Check if location is provided
        if location:
            # Get current weather
            response = file_ask(location)
            # Display weather details
            # st.json(response)
            st.write(response)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
