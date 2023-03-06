Para esta etapa, escolhi usar a API do CoinGecko para fornecer os valores de determinados cryptoativos para os usuarios do bot.  
O processo foi relativamente simples. Usei RegEx para validar o comando !run, garantindo que são passados dois argumentos formados apenas por letras. Em seguida, uso group() para separar os argumentos na string, e o codigo faz a requisição para a API, passando o primeiro group como argumento.  
Mais uma vez, o chatGPT foi utilizado como fonte para a criação do codigo, assim como algumas respostas do stackoverflow.  
No estado atual, o bot é capaz de receber os argumentos e fazer a requisição usando a API do CoinGecko, disponibilizando o valor do ativo desejado na moeda escolhida. O usuario-alvo do bot, por enquanto, é o investidor de cryptomoedas.
