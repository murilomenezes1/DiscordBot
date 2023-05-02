Para esta etapa, o processo foi mais lento.  
Primeiramente, tive que rever as aulas de tfidf e wordnet, a fim de entender melhor os conceitos e integrá-los ao bot.  
Para a execução, varias estratégias foram contempladas. Pensei em modos de criar um banco de dados para a aplicação, e considerei usar SQL mas, por praticidade, optei por um banco local na estrutura de json.  
Para o indice invertido, tentei seguir a aula de tfidf, usando o countvectorizer, mas o processo não estava andando bem e optei por calcular manualmente a frequência de cada palavra nos documentos presentes no banco de dados.  
A busca por termos semelhantes foi mais simples de implementar, e o processo foi bem parecido com o visto em aula. 
