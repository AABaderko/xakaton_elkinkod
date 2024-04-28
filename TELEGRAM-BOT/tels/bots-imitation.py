import modules.bot_datasender as botds
from modules.bot_datasender import Vector

robots_list = []
robots_list.append(botds.RobotCleaner(
    id=1,
    position=Vector(55.722218, 84.925292), direction=Vector(0, 0),
    mov_dir="forward", switch_time=0,
    battery = {
        "capacity": 90,
        "durability": 98,
    },
    task = botds.robot_tasks[2],
    status = botds.robot_stats[1],
))
robots_list.append(botds.RobotCleaner(
    id=2,
    position=Vector(55.713515, 84.933793), direction=Vector(0, 0),
    mov_dir="forward", switch_time=0,
    battery = {
        "capacity": 98,
        "durability": 99.9,
    },
    task = botds.robot_tasks[2],
    status = botds.robot_stats[1],
))
robots_list.append(botds.RobotCleaner(
    id=3,
    position=Vector(55.713660, 84.934328), direction=Vector(0, 0),
    mov_dir="forward", switch_time=0,
    battery = {
        "capacity": 60,
        "durability": 99.5,
    },
    task = botds.robot_tasks[1],
    status = botds.robot_stats[1],
))
robots_list.append(botds.RobotCleaner(
    id=4,
    position=Vector(55.713936, 84.926814), direction=Vector(0, 0),
    mov_dir="forward", switch_time=0,
    battery = {
        "capacity": 20,
        "durability": 98,
    },
    task = botds.robot_tasks[2],
    status = botds.robot_stats[0],
))
robots_list.append(botds.RobotCleaner(
    id=5,
    position=Vector(55.709729, 84.916441), direction=Vector(0, 0),
    mov_dir="forward", switch_time=0,
    battery = {
        "capacity": 60,
        "durability": 100,
    },
    task = botds.robot_tasks[2],
    status = botds.robot_stats[2],
))
robots_list.append(botds.RobotCleaner(
    id=6,
    position=Vector(55.724363, 84.934257), direction=Vector(0, 0),
    mov_dir="forward", switch_time=0,
    battery = {
        "capacity": 72.1,
        "durability": 98.6,
    },
    task = botds.robot_tasks[2],
    status = botds.robot_stats[1],
))
robots_list.append(botds.RobotCleaner(
    id=7,
    position=Vector(55.710515, 84.872049), direction=Vector(0, 0),
    mov_dir="forward", switch_time=0,
    battery = {
        "capacity": 84.2,
        "durability": 86.2,
    },
    task = botds.robot_tasks[2],
    status = botds.robot_stats[1],
))
robots_list.append(botds.RobotCleaner(
    id=8,
    position=Vector(55.701816, 84.914364), direction=Vector(0, 0),
    mov_dir="forward", switch_time=0,
    battery = {
        "capacity": 65.3,
        "durability": 70.3,
    },
    task = botds.robot_tasks[2],
    status = botds.robot_stats[2],
))
robots_list.append(botds.RobotCleaner(
    id=9,
    position=Vector(55.713453, 84.902084), direction=Vector(0, 0),
    mov_dir="forward", switch_time=0,
    battery = {
        "capacity": 87,
        "durability": 99.5,
    },
    task = botds.robot_tasks[2],
    status = botds.robot_stats[1],
))
robots_list.append(botds.RobotCleaner(
    id=10,
    position=Vector(55.711165, 84.842355), direction=Vector(0, 0),
    mov_dir="forward", switch_time=0,
    battery = {
        "capacity": 90,
        "durability": 96.4,
    },
    task = botds.robot_tasks[2],
    status = botds.robot_stats[2],
))



def updateRobots():
    for robot in robots_list:
        robot.Update()
        botds.sendData(robot)

updateRobots()