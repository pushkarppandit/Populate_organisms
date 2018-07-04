import numpy as np
import matplotlib.pyplot as plt
import copy

class organism:
    def __init__(self,level,pop,vi,ap,defence,agg,m,death):
        self.level=level
        self.vi=vi
        self.ap = ap
        self.defence=defence
        self.agg=agg
        self.m=m
        self.pop = pop
        self.death=death
        self.pop_list = []


    def pop_update(self,org_list,m_prev):
        if self.level>=1:
            food = org_list[self.level-1]
            food_pop = np.array([org.pop for org in food])
            food_m = np.array([org.m for org in food])
            food_mass = np.dot(food_m,food_pop)+ 0.0000001
        else:
            food_mass=m_prev
        if self.level<len(org_list)-1:
            pred = org_list[self.level+1]
            pred_pop = np.array([org.pop for org in pred])
            pred_ap = np.array([org.ap for org in pred])
            pred_eat = np.dot(pred_pop,pred_ap)+ 0.0000001
        else:
            pred_eat=0
        level = org_list[self.level]
        level_pop = np.array([org.pop for org in level])
        level_def = np.array([org.defence for org in level])
        level_agg = np.array([org.agg for org in level])
        level_def_t = np.dot(level_pop,level_def) + 0.0000001
        level_agg_t = np.dot(level_pop, level_agg) + 0.0000001
        # level_pop_t = level_pop.sum()

        self.pop_list.append(self.pop)

        dp = ((self.vi*self.pop - (self.defence*self.pop/level_def_t)*pred_eat) + ((self.agg*self.pop/level_agg_t)*food_mass - self.ap*self.pop)) - 1*self.death
        print(dp/self.pop)
        pop_new = self.pop + 0.005*dp
        pop_new = np.max([pop_new,0])
        return pop_new


    def disaster(self,maxi=0.5):
        # self.pop_list.append(self.pop)
        pop_new = (10 ** (np.random.rand() * (-1*maxi))) * self.pop
        return pop_new


class ecosystem:
    def __init__(self,config_dict):
        org_dict = {}
        for key in config_dict:
            org_list=[]
            for conf in config_dict[key]:
                org_list.append(organism(key,*tuple(conf)))
            org_dict[key] = org_list
        self.org_dict = org_dict

    def simulate(self,iter,dis_prob):
        for i in range(iter):
            pop_dict = {}
            if i>0:
                m_prev=m_now
            m_now = 0
            for key in self.org_dict:
                food_pop = np.array([org.pop for org in self.org_dict[key]])
                food_m = np.array([org.m for org in self.org_dict[key]])
                m_now += 0.18 * np.dot(food_m, food_pop) + 0.0000001
            if i==0:
                m_prev=m_now
            for key in self.org_dict:
                pop_dict[key] = [org_l.pop_update(self.org_dict,m_prev) for org_l in self.org_dict[key]]
            for key in self.org_dict:
                for i,org_l in enumerate(self.org_dict[key]):
                    if (key==0) and (np.random.rand() < dis_prob):
                        org_l.pop = org_l.disaster(0.1)
                    else:
                        org_l.pop = pop_dict[key][i]

    def plot_pop(self):
        pop_list = []
        name_list = []
        for key in self.org_dict:
            for i, org_l in enumerate(self.org_dict[key]):
                name_list.append(str(org_l.level)+'_'+str(i))
                pop_list.append(org_l.pop_list)
        pop_array = np.array(pop_list)
        plt.plot(pop_array.T)
        plt.legend(name_list)
        plt.show()
        # return  pop_array

# organism: [pop,vi,ap,defence,agg,m,death]
config_dict1 = {
    0: np.array([[10,1.3,1  ,1 ,1,2,0.1]]),
    1: np.array([[2 ,0.9,0.3,8 ,5,2,0.2],
                 [2 ,0.7,0.2,10,7,1,0.2]]),
    2: np.array([[1 ,0.1,1.5,1 ,1,4,0.3]])
}# organism: [pop,vi,ap,defence,agg,m,death]
config_dict2 = {
    0: np.array([[6 ,1.8 ,1  ,1  ,1.1,8  ,0.09],
                 [5 ,2.4 ,1.2,0.8,2  ,7  ,0.12],
                 [5 ,2.3 ,1  ,0.9,1.1,12,0.08]]),
    1: np.array([[3 ,0.8 ,1.8,8  ,5  ,1  ,0.15],
                 [3 ,0.7 ,1.6,10 ,5  ,1.1,0.15]]),
    2: np.array([[1 ,0.1 ,2.5,1  ,1  ,1.5  ,0.3 ],
                 [1, 0.1 ,2.5,1  ,1.3,1.8  ,0.3 ]])
}

eco1 = ecosystem(config_dict2)
eco1.simulate(2000,0)
eco1.plot_pop()
# print([len(l) for l in temp_pop])