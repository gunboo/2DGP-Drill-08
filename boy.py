from pico2d import *
from state_machine import StateMachine, space_down, time_out, left_up, right_down, left_down, right_up,a_down


class Idle:
    @staticmethod
    def enter(boy,e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e):
            boy.action = 3
            boy.face_dir = 1

        boy.frame = 0
        boy.dir = 0

        boy.start_time = get_time()
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8 #self를 전달하는 매개체 만들어야함 // state_machine에 self.o 객체 추가.
        if get_time() - boy.start_time > 3:
            #이벤트를 발생
            boy.state_machine.add_event(('TIME_OUT', 0))



    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e):
            boy.action = 1   # 오른쪽 이미지 프레임
            boy.dir = 1      # 오른쪽 방향
        elif left_down(e):
            boy.action = 0   # 왼쪽 이미지 프레임
            boy.dir = -1     # 왼쪽 방향
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
       pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5  # dir에 따라 이동

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            boy.x, boy.y
        )


class Sleep:
    @staticmethod
    def enter(boy,e):
        boy.face_dir = 1
        boy.action = 3
        boy.frame = 0
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100,
                                          boy.x, boy.y)

class AutoRun:
    @staticmethod
    def enter(boy,e):
        boy.action = 1 if boy.face_dir == 1 else 0
        boy.frame = 0
        boy.dir = 1 if boy.face_dir == 1 else -1
        boy.speed = 10 #속도 2배 증가
        boy.scale = 2.0 #크기 2배 확대
        boy.start_time = get_time()
    @staticmethod
    def exit(boy,e):
        boy.dir = 0 #나올때 방향 0
        boy.scale = 1.0 #원래크기로

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * boy.speed
        print(f"AutoRun: boy.x = {boy.x}, boy.dir = {boy.dir}, boy.speed = {boy.speed}")
        if boy.x < 0 or boy.x > 800:
            boy.dir *= -1 #화면 끝에 닿으면 방향 전환
            boy.face_dir *= -1
            boy.action = 1 if boy.face_dir ==1 else 0

        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT',0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            boy.x, boy.y+36,
            100 * boy.scale, 100 * boy.scale  # 확대된 크기로 그리기
        )

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.scale = 1.0 #초기 크기
        self.face_dir = 1
        self.state_machine = StateMachine(self) #소년의 객체를 구현하는 클래스 생성//어떤 객체를 위한 상태머신인지 표시
        self.state_machine.start(Run) #객체를 생성하는게 아닌, 직접 Idle 클래스를 사용
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, time_out: Sleep, a_down:AutoRun},
                Run: {right_up: Idle, left_up: Idle, a_down:AutoRun},
                Sleep: {right_down: Run, left_down: Run, right_up: Idle, left_up: Idle, space_down: Idle},
                AutoRun: {a_down:AutoRun,right_down:Run, left_down: Run, time_out: Idle}
            }
        )


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        #evebt : 입력 이벤트 key mouse
        #우리가 state machine 전달해줄건 ( , )

        self.state_machine.add_event(
            ('INPUT',event)
        )
        pass

    def draw(self):
        self.state_machine.draw()
