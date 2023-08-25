import string
import re
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

class Tagged:
    def __init__(self):
        # Inicializa a classe com uma string vazia para conteúdo e uma lista vazia para subs
        self.conteudo = ""
        self.subs = []
    
    def process_text(self, directory_path):
        """
        Lê o conteúdo do arquivo no diretório especificado e armazena na variável de instância 'conteudo'.
        
        :param directory_path: Caminho do arquivo a ser lido.
        """
        try:
            with open(directory_path, 'r', encoding="utf-8") as arquivo:
                self.conteudo = arquivo.read()
        except FileNotFoundError:
            print('Não foi possível abrir o arquivo.')
    
    def cleaning_text(self):
        """
        Realiza a limpeza e pré-processamento do texto, incluindo tokenização, remoção de stopwords e pontuações.
        """
        tokens = self.conteudo.split()
        textos = [token.lower() for token in tokens]
        
        punck = re.compile('[%s]' % re.escape(string.punctuation))
        punk = [punck.sub('', token) for token in textos]
        
        stops = [word for word in punk if word not in stopwords.words('portuguese')]
        
        # Cria a lista de palavras 'subs' contendo apenas os substantivos
        self.subs = [tagged_word[0] for word in stops for tagged_word in pos_tag(word_tokenize(word)) if tagged_word[1] == 'NN']
      
    def procurar(self, palavras):
        """
        Procura as palavras fornecidas na lista 'subs' e retorna um dicionário de contagem de ocorrências.
        
        :param palavras: Lista de palavras a serem procuradas.
        :return: Dicionário com a contagem de ocorrências de cada palavra.
        """
        # Cria um dicionário de contagem para as palavras especificadas
        counters = {word: self.subs.count(word) for word in self.subs if word in palavras}
        # Ordena o dicionário por contagem, do maior para o menor
        return dict(sorted(counters.items(), key=lambda item: item[1], reverse=True))
    
if __name__ == "__main__":
    # Cria uma instância da classe Tagged
    tag = Tagged()
    # Processa o texto a partir do arquivo especificado
    tag.process_text("c:/Users/Wande/Documents/GitHub/Summary_Transcription/texto/20230313-161052-081999711631-outgoing-6071.txt")
    # Realiza a limpeza do texto
    tag.cleaning_text()
    # Procura palavras específicas e imprime os resultados
    print(tag.procurar(['viagem', 'investimento', 'dólar']))  # Favoritas
    print(tag.procurar(['lucas', 'americano']))  # Proibidas

