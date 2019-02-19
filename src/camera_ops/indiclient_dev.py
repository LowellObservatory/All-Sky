import PyIndi
from device_dev import Device
from camera_dev import Camera

    
class INDIClient(PyIndi.BaseClient):
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 7624

    # def __init__(self, address=DEFAULT_HOST, port=DEFAULT_PORT, callbacks={}, autoconnect=True):
    def __init__(self, address=DEFAULT_HOST, port=DEFAULT_PORT, autoconnect=True):
        PyIndi.BaseClient.__init__(self)
        self.host = address
        self.port = port
        self.setServer(address, port)
        if autoconnect:
            self.connectServer()

    def devices(self):
        return [Device(x, self) for x in self.device_names]

    def cameras(self):
       return [Camera(x, self, connect_on_create=False) for x in self.__devices_by_interface('ccd')]

    def telescopes(self):
       return self.devices_by_interface('telescope')

    def devices_by_interface(self, interface):
       return [Device(x, self) for x in self.__devices_by_interface(interface)]
    

    @property
    def device_names(self):
        return [d.getDeviceName() for d in self.getDevices()]

    def newDevice(self, d):
        device = Device(d.getDeviceName(), self)
        print('on_new_device', device)

    def removeDevice(self, d):
        print('on_device_removed', dd.getDeviceName())

    def newProperty(self, p):
        device = p.getDeviceName() 
        group = p.getGroupName() 
        property_name = p.getName()
        print('device: ' + str(device))
        print('group: ' + str(group)) 
        print('property_name: ' + str(property_name))

    def removeProperty(self, p):
        print('on_remove_property', p)

    def newBLOB(self, bp):
        print('on_new_blob', bp)

    def newSwitch(self, svp):
        print('on_new_switch', svp)

    def newNumber(self, nvp):
        pass
        # print('on_new_number', nvp)

    def newText(self, tvp):
        print('on_new_text', tvp)

    def newLight(self, lvp):
        print('on_new_light', lvp)

    def newMessage(self, d, m):
        device = Device(d.getDeviceName(), self)
        message = device.get_queued_message(m)
        print('on_new_message', device, message)

    def serverConnected(self):
        print('on_server_connected')

    def serverDisconnected(self, code):
        print('on_server_disconnected', code)

    def __devices_by_interface(self, interface):
        return [x.name for x in self.devices() if interface in x.interfaces]
 
    def __str__(self):
        return 'INDI client connected to {0}:{1}'.format(self.host, self.port)

    def __repr__(self):
        return self.__str__()

