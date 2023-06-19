### [BD2] PROYECTO 2:  Recuperación de Documentos de Texto

**INTEGRANTE:**
Arleth Lapa Carhuamaca

---

## Introducción

Este proyecto tiene como objetivo aplicar algoritmos de búsqueda y recuperación de información basada en el contenido. Para lograrlo, se ha construido un índice invertido optimizado para tareas de búsqueda y recuperación en documentos de texto almacenados en memoria secundaria. Los datos utilizados como contenido consisten en un conjunto de tweets en formato JSON, considerando solo los tweets originales y excluyendo los retweets.

El presente informe se centra en presentar las comparaciones obtenidas al utilizar consultas con los mejores resultados. Se mostrará el desempeño del sistema de búsqueda y recuperación implementado, evaluando la precisión y eficiencia de los algoritmos utilizados. Además, se analizarán y discutirán los resultados obtenidos con el fin de destacar las fortalezas y posibles áreas de mejora en el enfoque de búsqueda y recuperación de información utilizado en este proyecto.

## Descripción del dominio de datos

La fuente de datos de este proyecto es un repositorio de tweets en formato JSON. Los tweets son publicaciones cortas realizadas en la plataforma de redes sociales. Cada tweet se compone de varios atributos que proporcionan información relevante sobre el contenido del tweet. Los campos presentes en cada registro de datos son los siguientes:

- ID: Identificador único del tweet.
- DATE: Fecha y hora de creación del tweet.
- TEXT: Texto completo del tweet.
- USER_ID: Identificador único del usuario que envió el tweet.
- USER_NAME: Nombre de usuario del autor del tweet.
- LOCATION: Información de ubicación asociada al usuario.
- RETWEETED: Indica si el tweet es un retweet (true/false).
- RT_TEXT: Texto completo del tweet original en caso de ser un retweet.
- RT_USER_ID: Identificador único del usuario que publicó el tweet - original en caso de ser un retweet.
- RT_USER_NAME: Nombre de usuario del autor del tweet original en caso de ser un retweet.

Cabe destacar que los retweets son mensajes que han sido compartidos por otros usuarios, mientras que los tweets originales son las publicaciones iniciales realizadas por los propios usuarios.

El objetivo principal de este proyecto es realizar consultas de búsqueda y recuperación de información en los tweets. Se buscará extraer los k elementos cuyo contenido sea más similar al de una consulta proporcionada en lenguaje natural. Esto implica encontrar tweets relevantes que coincidan con los términos o temas específicos de la consulta.

A continuación, se muestra un ejemplo de un tweet presente en la base de datos en formato JSON:

```
{
  "id": 1026814183042686976,
  "date": "Tue Aug 07 12:55:53 +0000 2018",
  "text": "RT @de_patty: Asuuuuuuu.. @Renzo_Reggiardo me da mala espina...su pasado fujimorísta qué miedo!!!y @luchocastanedap hijo de corrupto que s…",
  "user_id": 544008122,
  "user_name": "@CARLOSPUEMAPE1",
  "location": {},
  "retweeted": true,
  "RT_text": "Asuuuuuuu.. @Renzo_Reggiardo me da mala espina...su pasado fujimorísta qué miedo!!!y @luchocastanedap hijo de corrupto que secunda lo del padre NI HABLAR! Más comunicore Plop!lideran las preferencias para la alcaldía de Lima, según Ipsos | RPP Noticias https://t.co/w5TnU0Dmwq",
  "RT_user_id": 302995560,
  "RT_user_name": "@de_patty"
}

```

## Backend
Se ha construido un índice invertido óptimo para la busqueda y recuperación de _tweets_  por ranking (top k) para consultas de texto libre.

### Construcción del índice invertido
#### Preprocesamiento
*Filtrado de stopwords*
La librería _nltk_ crea los _stopwords_ en inglés, debido a la data se encuentra en ese idioma.
```
nltk.download('stopwords')
nltk.download('punkt')
stoplist = stopwords.words("english")
stoplist += ['?','.',',','»','«','â','ã','>','<','(',')','º','u']
```
*Reducción de palabras (Stemming)*
La librería _SnowballStemmer_ obtiene las raíces de las palabras de nuestra _data_, las cuales se usan para el proceso de tokenización.
```
stemmer = SnowballStemmer('english')
stem_token = stemmer.stem(word)
```
*Toquenizacion*
Se implementó una función que realiza la limpieza del texto, la cual removerá caracteres principales y urls.

```
def clean_text(self, text):
    text = self.remove_special_character(text)
    text = self.remove_punctuation(text)
    text = self.remove_emoji(text)
    text = self.remove_url(text)
    text = nltk.word_tokenize(text)
    return text
```

La función clean_text es un método que forma parte de una clase y se encarga de realizar una serie de tareas de limpieza y tokenización en un texto dado. A continuación, se describen brevemente las acciones que realiza cada paso dentro de la función:

- remove_punctuation: Remueve los signos de puntuación del texto.
- remove_url: Elimina las URLs presentes en el texto.
- remove_url: Elimina los emojis en el texto.
- remove_special_character: Elimina los caracteres especiales del texto.
- nltk.word_tokenize: Tokeniza el texto en una lista de palabras individuales.
En resumen, la función clean_text realiza una serie de transformaciones en un texto para limpiarlo y dividirlo en palabras individuales, lo cual puede ser útil para posteriores análisis o procesamientos de texto.
#### Ejecución óptima de consultas
Para obtener los resultados de tu consulta siguiendo los pasos mencionados, se realizaría lo siguiente:

1. Limpieza de la consulta en lenguaje natural: Aplicarías las mismas funciones de limpieza que se mencionaron anteriormente, como remover puntuación, URLs, caracteres especiales y emojis. El resultado sería una consulta limpia como: "El señor Daniel Urresti me bloqueo por cuestionar continuamente su candidatura".

2. Cálculo de TF e IDF: Para cada palabra en la consulta, se calcularía su frecuencia (TF) y su factor de inverso de documento (IDF). El TF mide la frecuencia de una palabra en la consulta, y el IDF mide la importancia de una palabra en el corpus de documentos.

3. Cálculo del índice invertido: Si una palabra de la consulta está presente en el índice invertido de los documentos, se obtendría el índice invertido correspondiente a esa palabra.

4. Cálculo de TF-IDF del query: Se multiplicaría el TF de cada palabra en la consulta por su correspondiente IDF para obtener el valor TF-IDF del query. Esto daría una representación numérica de la importancia de cada palabra en la consulta.

5. Ordenamiento de resultados: Finalmente, se ordenarían los documentos en una lista de cosenos, utilizando el valor de similitud del coseno entre el query y cada documento. La lista estaría ordenada de mayor a menor similitud, y contendría el ID del documento, la similitud del coseno y la lista de tweets correspondientes a ese documento.

## Frontend
Se realizó la implementación de una interfaz gráfica para que el usuario pueda interactuar con las funciones de búsqueda y recuperación de _tweets_. Es intiutiva y amigable para el usuario, recoge la consulta y solicita que ingrese el _top k_, que es la cantidad de documentos a recuperar según la mayor similitud de su consulta.

<img src="images/gui_p2.jpeg" alt="GUI VIEW" width="400"/>


#### Video

La presentación final en video se encuentra en el siguiente [link](https://drive.google.com/file/d/1ClbNamqOJMUT2LDFOIJJKhZUBPujqTeB/view?usp=sharing)
