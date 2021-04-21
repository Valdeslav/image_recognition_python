import pickle
import matplotlib.pyplot as plt
import numpy as np

class ExpertVector(object):
    def add_expert_vector(self, vector, filename):
        vector = self.simplify_vector(vector)
        with open(filename, 'rb') as f:
            vectors = pickle.load(f)
        vectors.append(vector)
        with open(filename, 'wb') as f:
            pickle.dump(vectors, f)

    def simplify_vector(self, vector):
        simple_vector = []
        for i in range(0, 100, 10):
            for j in range(0, 100, 10):
                area = (j, i, j+10, i+10)
                #part = np.array(vector.crop(area))
                #plt.imshow(part)
                #plt.show()
                part = np.array(vector.crop(area).resize((1, 1)))
                if part[0][0][0] <= 200 and part[0][0][1] <= 200 and part[0][0][2] <= 200:
                    simple_vector.append(1)
                else:
                    simple_vector.append(-1)

        vector = simple_vector
        return vector

    def get_expert_vecotrs(self, filename):
        with open(filename, 'rb') as f:
            vector = pickle.load(f)

        return vector