# ciroai
Criação de um conta que gera tweets como se fosse o Ciro Gomes

# Esse repo consiste dos seguintes arquivos a serem rodados nessa orderm:
* tweetscrapping.py - faz o download dos tweets do candidato
* limpandotweets.py - limpa os tweets e cria um arquivo txt 
* youtubesubtitles.py - adiciona as legendas retiradas dos videos de youtube
* word-rnn-ltsm.py - criar o modelo lstm que prediz a proxima palavra do tweet. Roda melhor com gpus
* gerando_tweets.py - criar uma lista de possíveis tweets com 6 palavras iniciais
