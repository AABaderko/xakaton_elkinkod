import json
import requests
import math

SendURL = "http://127.0.0.1:8000/update_data"

isSaveData = False

robot_movement_directions = [
    "forward", "backward", "stay"
]
robot_tasks = [
    "None", "cleaning", "moving", "recharge"
]
robot_stats = [
    "disabled", "auto", "handled"
]

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class RobotCleaner():
    def __init__(self,
            id = 0,
            position = Vector(0, 0),
            direction = Vector(0, 0),
            battery = {
                "capacity": 100,
                "durability": 100,
            },
            mov_dir = robot_movement_directions[0],
            switch_time = 0,
            task = robot_tasks[0],
            status = robot_stats[0],
        ):
        self.id = id
        self.position = position
        self.direction = direction

        self.speed = 1 / 100000

        self.movementDirection = mov_dir
        self.movementDirectionLast = self.movementDirection

        self.movementDirectionSwitchTime = switch_time

        self.battery = battery

        self.task = task
        self.status = status


    def getGPSData(self):
        return {"lat": self.position.x, "long": self.position.y} or {}

    def getAccelerometerData(self):
        return {"yaw": self.direction.x, "pitch": self.direction.y} or {}

    def getBatteryStatus(self):
        return self.battery or {}

    def getMotorsStatus(self):
        return 2

    def getLightsStatus(self):
        isActive = True
        return isActive
    
    def Update(self):
        if self.status == "auto":
            self.position.x += math.sin(self.direction.x) * self.speed
            self.position.y += math.cos(self.direction.x) * self.speed

        if self.movementDirection != self.movementDirectionLast:
            self.movementDirectionSwitchTime = 0.0
            self.movementDirectionLast = self.movementDirection

def sendData(robot=None):
    if not robot: return
    sended_data = {}

    sended_data['id'] = robot.id

    sended_data['location'] = robot.getGPSData()
    sended_data['direction'] = robot.getAccelerometerData()

    sended_data['movement_direction'] = robot.movementDirection
    sended_data['movement_last_switch_time'] = robot.movementDirectionSwitchTime

    sended_data['task'] = robot.task

    sended_data['battery'] = robot.getBatteryStatus()
    sended_data['motor_access'] = robot.getMotorsStatus()
    sended_data['light_active'] = robot.getLightsStatus()

    sended_data['status'] = robot.status
    
    if not isSaveData:
        sended_json_data = {"json": json.dumps(sended_data)}
        # print(sended_json_data)

        status_req = requests.post(SendURL, data = sended_json_data)
        print(f"Статус отправки {status_req.status_code}")
    else:
        with open("robot_data.json", "w") as file:
            json.dump(sended_data, file)