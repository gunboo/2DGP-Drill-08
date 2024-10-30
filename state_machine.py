from pico2d import *
from pymsgbox import password



#event (문자열, 실제 값)
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e): #e가 space down인지 판단 true or false
    return (e[0] == 'INPUT' and
            e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE)
def a_down(e): #a를 누르는것을 감지하기
    return (e[0] == 'INPUT' and
            e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a)
def time_out(e): #e가 time out 인지 판단
    return e[0] == 'TIME_OUT'


#상태 머신을 처리 관리해주는 클래스
class StateMachine:
    def __init__(self, o):
        self.o = o #boy에 self가 전달 // self.o 상태머신과 연결된 캐릭터 객체
        self.event_que = [] # 발생하는 이벤트를 담는 리스트

    def update(self):
        self.cur_state.do(self.o)
        # 이벤트가 발생했는지 확인하고 상태 변환
        if self.event_que:
            e = self.event_que.pop(0)
            # 사전에서 현재 상태에 대한 전이 규칙을 가져옴
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    self.cur_state.exit(self.o,e)
                    print(f'EXIT from {self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o,e)
                    print(f'ENTER into {next_state}')
                    return

    def start(self,start_state):
        # 현재 상태를시작상태로 만듦
        self.cur_state = start_state #Idle
        self.cur_state.enter(self.o, ('START', 0))
        print(f'ENTER into {self.cur_state}')
        pass

    def draw(self):
        self.cur_state. draw(self.o)


    def set_transitions(self,transitions):
        self.transitions = transitions


    def add_event(self,e):
        self.event_que.append(e)
        print(f'    DEBUG: new event {e} is added.')
