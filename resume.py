from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from langchain.llms.openai import OpenAI
import os




def get_response(query, directory_path, apk):
    # Load one specific doc
    # Configure prompt parameters and initialise helper
    max_input_size = 4096
    num_output = 256
    max_chunk_overlap = 0.5
    
    llm_predictor = LLMPredictor(llm=OpenAI(openai_api_key=apk, temperature=0, model_name="text-davinci-003"))

    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    if os.path.isdir(directory_path): 
        # Load documents from the 'data' directory
        documents = SimpleDirectoryReader(directory_path).load_data()
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        
        query_engine = index.as_query_engine(response_mode="compact")
        response = query_engine.query(query)
        
        
        if response is None:
            print("Oops! No result found")
        else:
            print(response)
    else:
        print(f"Not a valid directory: {directory_path}")


if __name__ == "__main__":
    openai_api_key='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'
    directory_path='c:/Users/Wande/Documents/GitHub/Summary_Transcription/texto'
    
    print('escreva a query ao lado: ')
    query = input()
    
    if not query.strip():
        print(f"Please provide the search query.")
    else:
        try:
            if len(openai_api_key) > 0:
                get_response(query,directory_path,openai_api_key)
            else:
                print(f"Enter a valid openai key")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    get_response(query,directory_path,openai_api_key)