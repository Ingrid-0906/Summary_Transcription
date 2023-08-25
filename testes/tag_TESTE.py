import unittest
import string
import re
import nltk
from nltk.probability import FreqDist
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

class Tagged:
    def __init__(self):
        self.conteudo = ""
        self.subs = []
    
    def process_text(self, directory_path):
        try:
            with open(directory_path, 'r', encoding="utf-8") as arquivo:
                self.conteudo = arquivo.read()
        except FileNotFoundError:
            print('Não foi possível abrir o arquivo.')
    
    def cleaning_text(self):
        tokens = self.conteudo.split()
        textos = [token.lower() for token in tokens]
        
        punck = re.compile('[%s]' % re.escape(string.punctuation))
        punk = [punck.sub('', token) for token in textos]
        
        stops = [word for word in punk if word not in stopwords.words('portuguese')]
        
        for word in stops:
            tagged_words = pos_tag(word_tokenize(word))
            for tagged_word in tagged_words:
                if tagged_word[1] == 'NN':
                    self.subs.append(tagged_word[0])
      
    def procurar(self, palavras):
        counters = {}
        for word in self.subs:
            if word in palavras:
                counters[word] = counters.get(word, 0) + 1
        counters = dict(sorted(counters.items(), key=lambda item: item[1], reverse=True))
        return counters

class TestTaggedMethods(unittest.TestCase):
    def setUp(self):
        self.tag = Tagged()
        self.tag.process_text("c:/Users/Wande/Documents/GitHub/Summary_Transcription/texto/20230313-161052-081999711631-outgoing-6071.txt")
        self.tag.cleaning_text()

    def test_procurar_favoritas(self):
        result = self.tag.procurar(['viagem', 'investimento', 'dólar'])
        self.assertGreater(len(result), 0)
    
    def test_procurar_proibidas(self):
        result = self.tag.procurar(['lucas', 'americano'])
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
