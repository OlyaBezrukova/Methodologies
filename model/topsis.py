from .models import Criterias, Options, Scores, Methodologies
import pandas as pd
import numpy as np 
from .ahp import Ahp
from django.contrib.auth.models import User


class Topsis(object):
    def __init__(self, user):
        ahp = Ahp(user)
        self.weights = ahp.get_weights()
        self.methodologies_names = [meth.name for meth in list(Methodologies.objects.filter(access=user))] 
        self.methodologies= list(Methodologies.objects.filter(access=user)) 
        self.relation_matrix = pd.DataFrame(data=np.zeros((len(self.methodologies), len(self.weights))), columns=self.weights.keys(), index=self.methodologies)

    def __normalize_and_weighted(self):
        squared_matrix = pd.DataFrame(data=np.power(self.relation_matrix.values, 2), 
                                      columns=self.relation_matrix.columns, index=self.relation_matrix.index)
        columns_sum = squared_matrix.apply(lambda value: np.sqrt(sum(value)), axis=0)
        self.relation_matrix = self.relation_matrix.div(columns_sum.values, axis=1)
        self.relation_matrix = self.relation_matrix.mul(self.weights)
    
    def get_results(self, response: dict = None):
        self.__get_responses(response=response)
        self.__normalize_and_weighted()

        columns_max_values = self.relation_matrix.max(axis=0)
        columns_min_values = self.relation_matrix.min(axis=0)

        ideal_relation_matrix = self.relation_matrix.copy(deep=True)
        ideal_relation_matrix = ideal_relation_matrix.sub(columns_max_values, axis=1)
        ideal_relation_matrix = ideal_relation_matrix.apply(lambda value: np.power(value, 2))

        negative_relation_matrix = self.relation_matrix.copy(deep=True)
        negative_relation_matrix = negative_relation_matrix.sub(columns_min_values, axis=1)
        negative_relation_matrix = negative_relation_matrix.apply(lambda value: np.power(value, 2))

        ideal_sum = ideal_relation_matrix.sum(axis=1)
        negative_sum = negative_relation_matrix.sum(axis=1)

        result = (negative_sum / (ideal_sum + negative_sum)).to_frame()
        result.columns = ['Distance to negative']
        result['Distance to negative'] = result['Distance to negative'].apply(lambda x: np.round(x, 3))
        result['Distance to ideal'] = np.round((1 - result['Distance to negative']), 3)
        result = result.sort_values(by=['Distance to negative'], ascending=False)
        result['Ранг'] = np.arange(result.shape[0]) + 1
        result = result[['Ранг', 'Distance to ideal', 'Distance to negative']]

        return result

    def __get_responses(self, response: dict = None):
        for key, value in response.items():
            value_id = Options.objects.get(description=value).id
            scores = []
            for i in range(0,  len(self.methodologies)):
                score = Scores.objects.get(option=value_id, methodology=self.methodologies[i].pk).score
                scores.append(score)
            self.relation_matrix.loc[:, key] = scores


        
