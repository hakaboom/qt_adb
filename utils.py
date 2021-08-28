# -*- coding: utf-8 -*-
from adbutils import ADBDevice
from collections import OrderedDict


class DeviceList(object):
    def __init__(self):
        self.devices = OrderedDict()

    def __iter__(self):
        return self.devices.__iter__()

    def add_device(self, device: ADBDevice):
        """ 添加设备 """
        self.devices[device.device_id] = device

    def get_device_by_id(self, device_id: str):
        """ 通过设备ID找到对应ADBDevice """
        return self.devices.get(device_id)

    def get_device_status_by_id(self, device_id: str):
        """ 通过设备ID, 返回对应设备的状态"""
        device = self.get_device_by_id(device_id)  # type: ADBDevice
        if device:
            return device.status

    def remove_device(self, device_id):
        """ 移除设备"""
        self.devices.pop(device_id)