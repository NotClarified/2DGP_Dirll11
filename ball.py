from pico2d import *
import game_world
import game_framework
from zombie import Zombie


class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.collided = False
        # 모든 zombie와 충돌 페어를 자동으로 등록
        for obj in game_world.world[1]:  # 레이어 1에 있는 모든 객체 (zombie가 있는 레이어로 가정)
            if isinstance(obj, Zombie):  # 객체가 Zombie인 경우만 등록
                game_world.add_collision_pair('ball:zombie', self, obj)

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        if not self.collided:  # 충돌 후에는 위치 업데이트하지 않음
            self.x += self.velocity * 100 * game_framework.frame_time
            # print(f'Ball position - x: {self.x}, y: {self.y}')  # 현재 좌표를 로그로 출력
            if self.x < 25 or self.x > 1600 - 25:
                game_world.remove_object(self)


    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if self.collided:
            return
        if group == 'boy:ball':
            print('boy ball 접촉!!')
            game_world.remove_object(self)
        elif group == 'ball:zombie' and not self.collided:  # 충돌 플래그로 중복 방지
            print ('ball zombie 접촉!!')
            self.y = 1000 # 뭔짓을해도 공이 삭제되기 전 충돌처리가 여러번 나서 공중으로 공을 이동시킴
            self.collided = True
            try:
                game_world.remove_object(self)
            except ValueError:
                print("이미 제거된 ball 객체입니다.")