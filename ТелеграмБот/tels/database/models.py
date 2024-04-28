from django.db import models

# Create your models here.
class RobotsInfoManager(models.Manager):
    def add_info(self, data):
        return self.create(
            bot_id = data['id'],
            latitude = data['location']['lat'], longitude = data['location']['long'],
            yaw = data['direction']['yaw'], pitch = data['direction']['pitch'],
            movement_direction = data['movement_direction'],
            task = data['task'],
            battery_capacity = data['battery']['capacity'], battery_durability = data['battery']['durability'],
            light_state = data['light_active'],
            status = data['status']
        )
    
    def update_info(self, obj, data):
        return 

class RobotsInfo(models.Model):
    bot_id = models.IntegerField()

    latitude = models.FloatField()
    longitude = models.FloatField()

    yaw = models.FloatField()
    pitch = models.FloatField()

    #movement_direction_states
    mv_dir_states = {
        "forward": "forward",
        "backward": "backward",
        "stay": "stay",
    }
    movement_direction = models.CharField(max_length=50, choices=mv_dir_states)

    task_list = {
        "None": "None",
        "moving": "moving",
        "recharge": "recharge",
        "cleaning": "cleaning",
    }
    task = models.CharField(max_length=50, choices=task_list)

    battery_capacity = models.FloatField()
    battery_durability = models.FloatField()

    light_state = models.BooleanField(default=False)

    status_list = {
        "disabled": "disabled",
        "auto": "auto",
        "handled": "handled",
    }
    status = models.CharField(max_length=50, choices=status_list)

    objects = models.Manager()
    info_manager = RobotsInfoManager()

    def __str__(self):
        return str(self.bot_id)

class RobotsData(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=500)

    def __str__(self):
        return str(self.name)