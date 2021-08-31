from dobot_api import dobot_api_dashboard, dobot_api_feedback, MyType
from multiprocessing import Process
import numpy as np
import time

def main(client_dashboard, client_feedback):
    client_dashboard.ClearError()
    time.sleep(0.5)
    client_dashboard.EnableRobot()
    time.sleep(0.5)
    client_dashboard.User(0)
    client_dashboard.Tool(0)
    client_feedback.JointMovJ(0,50,0,0,0,0)
    time.sleep(5)
    client_feedback.JointMovJ(0,30,0,0,0,0)
    time.sleep(5)
    print('!!!!!!END!!!!!!')

def data_feedback(client_feedback):
    while True:
        time.sleep(0.05)
        all = client_feedback.socket_feedback.recv(10240)
        data = all[0:1440]
        a = np.frombuffer(data, dtype=MyType)
        if hex((a['test_value'][0])) == '0x123456789abcdef':
            print('robot_mode', a['robot_mode'])
            print('tool_vector_actual', np.around(a['tool_vector_actual'], decimals=4))
            print('q_actual', np.around(a['q_actual'], decimals=4))

if __name__ == '__main__':
    client_dashboard = dobot_api_dashboard('192.168.5.1', 29999)
    client_feedback = dobot_api_feedback('192.168.5.1', 30003)
    p1 = Process(target=main, args=(client_dashboard, client_feedback))
    p1.start()
    p2 = Process(target=data_feedback, args=(client_feedback, ))
    p2.daemon =True
    p2.start()
    p1.join()
    client_dashboard.close()
    client_feedback.close()