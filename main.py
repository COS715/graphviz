import vk_api
import time
from graphviz import Digraph

# Функция для получения списка друзей пользователя
def get_friends(user_id, access_token):
    try:
        response = vk_api.vk_api.VkApi(token=access_token).method('friends.get', {'user_id': user_id})
        return response['items']
    except vk_api.exceptions.ApiError as e:
        if e.code == 6:  # Превышено кол-во запросов в секунду
            time.sleep(1)  # Пауза на 1 секунду
            return get_friends(user_id, access_token)
        else:
            raise e

# Функция для построения графа связей
def build_graph(user_id, depth, access_token):
    graph = []
    queue = [{'user_id': user_id, 'level': 0}]
    visited = set()

    while queue:
        current = queue.pop(0)
        user_id = current['user_id']
        level = current['level']

        if level > depth:
            break

        if user_id in visited:
            continue

        visited.add(user_id)
        friends = get_friends(user_id, access_token)
        graph.append({user_id: friends})

        if level < depth:
            for friend in friends:
                queue.append({'user_id': friend, 'level': level + 1})

    return graph

# Заменить token
access_token = '12345'

# Получение списка друзей и построение графа связей
user_id = 1234  # Заменитm id
depth = 1
graph = build_graph(user_id, depth, access_token)

# Визуализация графа
dot = Digraph(comment='VK Friends Graph')
for level, data in enumerate(graph):
    for user_id, friends in data.items():
        dot.node(str(user_id), str(user_id))
        for friend in friends:
            dot.node(str(friend), str(friend))
            dot.edge(str(user_id), str(friend))

dot.render('friends_graph.gv', view=True)