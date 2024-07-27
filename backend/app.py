import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense


data = pd.read_csv('Disease,Symptoms,Ayurvedic Treatment.csv')


training_sentences = data['Symptoms'].tolist()
training_labels = data['Disease'].tolist()


tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_sentences)
max_sequence_len = max([len(x) for x in training_sequences])
padded = pad_sequences(training_sequences, maxlen=max_sequence_len, padding='post')


label_tokenizer = Tokenizer()
label_tokenizer.fit_on_texts(training_labels)
label_word_index = label_tokenizer.word_index
training_label_seq = label_tokenizer.texts_to_sequences(training_labels)
training_label_seq = np.array([item[0] for item in training_label_seq])  


model = Sequential([
    Embedding(10000, 16, input_length=max_sequence_len),
    LSTM(32),
    Dense(24, activation='relu'),
    Dense(len(label_word_index) + 1, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


model.fit(padded, training_label_seq, epochs=30)


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    req_data = request.get_json()
    Symptoms = req_data['Symptoms']

    
    input_seq = tokenizer.texts_to_sequences([Symptoms])
    padded_input_seq = pad_sequences(input_seq, maxlen=max_sequence_len, padding='post')

    
    predictions = model.predict(padded_input_seq)
    predicted_label = np.argmax(predictions)
    Disease = label_tokenizer.index_word[predicted_label]  

    
    Treatment = data[data['Disease'] == Disease]['Treatment'].values[0]
    Procedure = data[data['Disease'] == Disease]['Procedure'].values[0]
    Precautions = data[data['Disease'] == Disease]['Precautions'].values[0]

    return jsonify({
        'Disease': Disease,
        'Treatment': Treatment,
        'Procedure': Procedure,
        'Precautions': Precautions
    })

if __name__ == '__main__':
    app.run(debug=True)
