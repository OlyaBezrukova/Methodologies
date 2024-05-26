from .models import Criterias, Options, Scores, Methodologies, CriteriasPriority
import pandas as pd
import numpy as np 


class Ahp(object):
    def __init__(self, user=None):
        self.criterias = [crit for crit in list(Criterias.objects.filter(access=user))]
        names = [crit.name for crit in self.criterias]
        self.matrix = pd.DataFrame(data=np.zeros((len(self.criterias), len(self.criterias))), columns=names, index=names)

    def __normalized(self):
        columns_sum = self.matrix.apply(lambda value: sum(value), axis=0)
        self.matrix = self.matrix.div(columns_sum.values, axis=1)

    def __get_responses(self):
        for crit1 in self.criterias:
            for crit2 in self.criterias:
                try:
                    priority = CriteriasPriority.objects.filter(criteria = crit1).filter(_criteria = crit2)[0].priority
                    self.matrix.loc[crit1.name, crit2.name] = priority * 1.0
                    self.matrix.loc[crit2.name, crit1.name] = 1.0/priority
                except:
                    try:
                        priority = CriteriasPriority.objects.filter(criteria = crit2).filter(_criteria = crit1)[0].priority
                        self.matrix.loc[crit2.name, crit1.name] = priority * 1.0
                        self.matrix.loc[crit1.name, crit2.name] = 1.0/priority
                    except:
                        pass
                
    
    def get_weights(self):
        self.__get_responses()
        self.__normalized()
        row_sum = self.matrix.apply(lambda value: sum(value), axis=1)
        gen_sum = row_sum.sum()
        weights = row_sum.div(gen_sum, axis=0)
        return weights.to_dict()
        

                





