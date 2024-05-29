from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter



def main():
    load_dotenv()
    # upload file
    pdf = st.file_uploader("Upload your PDF", type="pdf")
    # extract the text
    if pdf is not None:
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
        text += page.extract_text()
        
        
      # split into chunks
      text_splitter = CharacterTextSplitter(
        separator="",
        chunk_size=100,
        chunk_overlap=20,
        length_function=len
      )
      chunks = text_splitter.split_text(text)
      st.write(chunks)
      # joined_text = ''.join(chunks)
      # st.write(joined_text)
      
      # # create embeddings
      # embeddings = OpenAIEmbeddings()
      # knowledge_base = FAISS.from_texts(chunks, embeddings)
      
      # # show user input
      # user_question = st.text_input("Ask a question about your PDF:")
      # if user_question:
      #   docs = knowledge_base.similarity_search(user_question)
        
      #   llm = OpenAI()
      #   chain = load_qa_chain(llm, chain_type="stuff")
      #   with get_openai_callback() as cb:
      #     response = chain.run(input_documents=docs, question=user_question)
      #     print(cb)
           
      #   st.write(response)
    

if __name__ == '__main__':
    main()
