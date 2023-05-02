import discord
from dotenv import load_dotenv
import os
from pycoingecko import CoinGeckoAPI
import re 
from bs4 import BeautifulSoup
import requests
import pprint
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet

import tensorflow as tf






headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }








load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

cg = CoinGeckoAPI()

words = {}





index = {}

@client.event
async def on_message(message):

	if not isinstance(message.channel, discord.DMChannel):
		return # ignore messages that are not sent via private message
	if message.author == client.user:
		return

	if message.content.lower() == "!help":
		await message.channel.send('Olá!\n!run <crypto> <currency> retorna o valor atual do ativo na moeda escolhida - dados fornecidos pela API da CoinGecko\n!crawl <url> adiciona o conteudo da url ao banco de dados, e começa um processo de crawling.\n!search <palavra> faz uma busca pela palavra no banco de dados. O parametro <th=float> pode ser passado, adicionando um limiar de sentimento para a busca.\n!wn_search <palavra> faz uma busca, no banco de dados, por termos semelhantes à palavra indicada. O parametro <th=float> pode ser passado, adicionando um limiar de sentimento para a busca. ')
	if message.content.lower() == '!source':
		await message.channel.send('Olá! Você pode encontrar meu source code em https://github.com/murilomenezes1/DiscordBot')
	if message.content.lower() == "!author":
		await message.channel.send("Fui desenvolvido por Murilo Menezes para a disciplina de NLP!")

	match = re.match(r'^!run ([A-Za-z]+) ([A-Za-z]+)$', message.content.lower())
	if match:
		coin = match.group(1).lower()
		currency = match.group(2).lower()
		p = cg.get_price(ids=coin, vs_currencies=currency)

		await message.channel.send("{} está sendo negociada à {}${:5,.2f}".format(coin,  currency.upper(), p[coin][currency]))

	crawler = re.match(r'^!crawl ((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)', message.content.lower())

	if crawler:


		url = crawler.group(1).lower()
		req = requests.get(url,headers)
		soup = BeautifulSoup(req.text, 'html.parser')

		model = tf.keras.models.load_model('Model/BLSTM')

		db = {}

		db['URL: {}'.format(url)] = {'title' : soup.title.string}

		# print(soup.prettify())
		links = []
		for link in soup.find_all('a',attrs={'href': re.compile("^https://")}):
		    links.append(link.get('href'))

		db['URL: {}'.format(url)]['Links'] = links



		txt_data = soup.get_text()
		tokens = re.findall(r'\b\w+\b', txt_data)

		db['URL: {}'.format(url)]['Tokens'] = tokens

		sentiment = model.predict([soup.title.string])

		db['URL: {}'.format(url)]['Sentiment'] = str(sentiment[0][1])

		with open(f'db/database.json', 'w+') as f:
			json.dump(db, f)
		

		if sentiment[0][1] > 0.3:

			sentiment_n = 'positive'

		else:

			sentiment_n = 'negative'

		await message.channel.send("Input adicionado ao banco de dados.\nURL: {}\nTitulo: {}\nSentimento: {} ({})".format(url, soup.title.string, sentiment[0][1], sentiment_n))
		vectorizer = TfidfVectorizer()
		tfidf = vectorizer.fit_transform(tokens)

		inverted_index = {}




		with open('db/database.json', 'r') as r:

			data = json.load(r)





		for i in data.keys():

			for term in data[i]['Tokens']:

				if term not in inverted_index.keys():

					inverted_index[term] = {i : data[i]['Tokens'].count(term)/len(data[i]['Tokens'])}


				else:

					inverted_index[term][i] = data[i]['Tokens'].count(term)/len(data[i]['Tokens'])

		with open('index/inverted_index.json', 'w+') as f:

			json.dump(inverted_index, f)

		


	search = re.match(r'^!search ([A-Za-z]+)(?: th=([\d.]+))?', message.content.lower())

	if search:

		th = 0 
		term = search.group(1).lower()

		if search.group(2):
			th = wn_search.group(2)[3:]
			await message.channel.send("Iniciando busca por termo usando threshold = {}".format(th))

		else:

			await message.channel.send("Iniciando busca por termo sem threshold.")

		with open('index/inverted_index.json', 'r') as r:

			inverted_index = json.load(r)

		with open('db/database.json', 'r') as db:

			data = json.load(db)



		if term in inverted_index.keys():

			freq = 0

			for i in inverted_index[term].keys():

				# print(db[i]['Sentiment'])
				print(data[i]['Sentiment'])
				print(th)

				if float(data[i]['Sentiment']) >= float(th):

					freq += inverted_index[term][i]
					await message.channel.send("A palavra '{}' foi encontrada no '{}' e seu TFIDF para este link é {}".format(term,i,inverted_index[term][i]))

				else:

					await message.channel.send("O link {} foi ignorado na busca, por não atender o limite de negatividade indicado pelo parametro th.".format(i))

			await message.channel.send("O TFIDF da palavra '{}' entre os documentos em que ela aparece é {}".format(term,freq))


		else:

			await message.channel.send("A palavra '{}' não foi encontrada em nenhum dos documentos no banco de dados.")





	wn_search = re.match(r'^!wn_search ([A-Za-z]+)(?: th=([\d.]+))?', message.content.lower())
	if wn_search:

		th = 0 
		wn_term = wn_search.group(1).lower()
		synsets = wordnet.synsets(wn_term)


		if wn_search.group(2):
			th = wn_search.group(2)[3:]
			await message.channel.send("Iniciando busca por temo usando threshold = {}".format(th))

		else:

			await message.channel.send("Iniciando busca por termo sem threshold.")



		res = []
		l =[]


		for s in synsets:

			l = [l.name() for l in s.lemmas()]


		with open('index/inverted_index.json', 'r') as f:

			index = json.load(f)


		with open('db/database.json', 'r') as r:

			data = json.load(r)





		for i in l:

			if i in index.keys():

				for k in index[i].keys():

					print(k)

					if float(data[k]['Sentiment']) >= float(th):

						res.append((i, index[i][k], k))

					else:

						await message.channel.send("{} ignored.".format(k))



		await message.channel.send("Sinonimos para a palavra '{}': {}".format(wn_term, l))

		if len(res) > 0:
			await message.channel.send("Encontrei estes sinonimos em meu banco de dados, assim como seu TFIDF e o link que contém a palavra: {}".format(res))

		else:

			await message.channel.send("Nenhum dos sinonimos foi encontrado em meu banco de dados.")



		


		# print(links)




client.run(str(TOKEN))




