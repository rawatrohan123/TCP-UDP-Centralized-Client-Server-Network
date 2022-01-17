import random


class DistanceProtocols:

    @staticmethod
    def map_network(user_names):
        num_users = len(user_names)
        distance_arr = [[0, 15, 10, 999], [15, 0, 30, 11], [10, 30, 0, 25], [999, 11, 25, 0]]
        #distance_arr = [[random.randint(1, 9) for i in range(num_users)] for j in range(num_users)]
        return distance_arr

    @staticmethod
    def distance_vector(distance_arr):
        distance = distance_arr
        while True:
            check = 0
            for i in range(len(distance)):
                for j in range(len(distance)):
                    for k in range(len(distance)):
                        if distance[i][j] > distance[i][k] + distance[k][j]:
                            distance[i][j] = distance[i][k] + distance[k][j]
                            check = 1
            if check == 0:
                break
        return distance

    @staticmethod
    def link_state(distance, user_index):
        cost = []
        num_users = len(distance)
        for i in range(0, num_users):
            if user_index == i:
                continue
            cost.append([user_index, distance[i]])
            solution = [user_index]
        for j in range(2, num_users):
            return distance



#print (message)
#print(distance)

