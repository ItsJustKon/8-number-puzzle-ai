import moves
import random
import numpy as np
from math import floor, sqrt
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Normalization
from keras.losses import MeanSquaredError
class Puzzle:
    def __init__(self, state):
        self.state = state
        self.legalmoves, self.moveboard = moves.getLegalMoves(self.state, int(sqrt(self.state.size)))
    
    def makemove(self, action):
        moves.MakeMoves(self.state, int(sqrt(self.state.size)), action, self.moveboard)
        self.legalmoves, self.moveboard = moves.getLegalMoves(self.state, int(sqrt(self.state.size)))
        

def custom_loss(y_true, y_pred):
            
    # calculate loss, using y_pred
    loss = 0
        
    return loss        
board = Puzzle(moves.CreateRandomBoard(random.randint(9,35)))
goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
x = 0
while True:
    print("Current board:\n", board.state, "\nLegal moves:\n", board.legalmoves)
    x = int(input("Make your move: "))
    if x == -1:
        break
    board.makemove(x)
    if np.array_equal(board.state, goal):
        print("Completed", "\n", board.state)
        break
    
#create the input layer
input_layer = Input(shape=(5, ))
normalize_layer = Normalization()(input_layer)
#create the other hidden layers and the output layer
hidden_1 = Dense(5, activation='relu')(normalize_layer)
hidden_2 = Dense(32, activation='relu')(hidden_1)
output = Dense(1, activation='linear')(hidden_2)
model = Model(inputs=input_layer, outputs=output)
filename = 'example.txt'
# inputs = np.loadtxt(filename, delimiter=',', skiprows=1, dtype=str)
# ouputs = np.loadtxt(filename, delimiter=',', skiprows=1, dtype=str)
inputs = np.array([])
outputs = []
for i in range(100):
    inputs = np.append(inputs, np.random.randint(1,9,(5,))) 
    print(inputs)
    try:
        outputs.append(inputs[i][2])
    except IndexError:
        print("Index Error")
        
inputs = tf.convert_to_tensor(inputs.reshape(100,5))
# inputs = np.array([[0,5,5,8,2],[4,2,6,8,9],[0,3,2,4,7]])
# ouputs = np.array([5,6,3])
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),loss="categorical_crossentropy",metrics=['accuracy'])
print(inputs, outputs)
print(model.loss)
model.fit(inputs, outputs)
pred = model.predict(np.array([9,5,9,4,2]))
print(pred)
