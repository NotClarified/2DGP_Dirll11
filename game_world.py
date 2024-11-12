world = [[] for _ in range(4)]

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()



# fill here
def collide(a, b):
    if a is None or b is None:
        return False

    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    print(f'Collision detected between: {a} and {b}')

    return True

collision_pairs = {}
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
    for group, objects in collision_pairs.items():
        objects[0] = [a for a in objects[0] if a is not None]
        objects[1] = [b for b in objects[1] if b is not None]


def clean_collision_pairs():
    pass


def handle_collisions():
    clean_collision_pairs()
    for group, pairs in collision_pairs.items():
        pairs[0] = [a for a in pairs[0] if a is not None]
        pairs[1] = [b for b in pairs[1] if b is not None]

        for a in pairs[0][:]:
            for b in pairs[1][:]:
                if a is None or b is None:  # 객체가 None인 경우 충돌 검사 생략
                    continue
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
