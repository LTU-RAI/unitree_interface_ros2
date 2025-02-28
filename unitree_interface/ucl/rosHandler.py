import time

from .common import byte_print, decode_version, decode_sn, getVoltage, pretty_print_obj
from .highCmd import highCmd
from .highState import highState
from .lowCmd import lowCmd
from .unitreeConnection import unitreeConnection, WIFI_DEFAULTS, LOW_CMD_DEFAULTS, HIGH_CMD_DEFAULTS
from .enums import Mode, GaitType, SpeedLevel
from .complex import motorCmd

class ROSHandler:
    def __init__(self, networkSettings) -> None:
        # You can use one of the 3 Presets WIFI_DEFAULTS, LOW_CMD_DEFAULTS or HIGH_CMD_DEFAULTS.
        # IF NONE OF THEM ARE WORKING YOU CAN DEFINE A CUSTOM ONE LIKE THIS:
        #
        # MY_CONNECTION_SETTINGS = (listenPort, addr_wifi, sendPort_high, local_ip_wifi)
        # conn = unitreeConnection(MY_CONNECTION_SETTINGS)
        #
        print("Trying to connect to the dog...")
        self.conn = unitreeConnection(networkSettings)
        self.conn.startRecv()
        self.hcmd = highCmd()
        self.hstate = highState()

    def firstContact(self):
        conn, hcmd, hstate = self.conn, self.hcmd, self.hstate

        # Send empty command to tell the dog the receive port and initialize the connectin
        cmd_bytes = hcmd.buildCmd(debug=False)
        self.conn.send(cmd_bytes)
        time.sleep(0.5)  # Some time to collect pakets ;)
        data = conn.getData()
        print(len(data))

        for paket in data:
            print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')
            hstate.parseData(paket)
            print(f'SN [{byte_print(hstate.SN)}]:\t{decode_sn(hstate.SN)}')
            print(f'Ver [{byte_print(hstate.version)}]:\t{decode_version(hstate.version)}')
            print(f'SOC:\t\t\t{hstate.bms.SOC} %')
            print(f'Overall Voltage:\t{getVoltage(hstate.bms.cell_vol)} mv')  # something is still wrong here...
            print(f'Current:\t\t{hstate.bms.current} mA')
            print(f'Cycles:\t\t\t{hstate.bms.cycle}')
            print(f'Temps BQ:\t\t{hstate.bms.BQ_NTC[0]} °C, {hstate.bms.BQ_NTC[1]}°C')
            print(f'Temps MCU:\t\t{hstate.bms.MCU_NTC[0]} °C, {hstate.bms.MCU_NTC[1]}°C')
            print(f'FootForce:\t\t{hstate.footForce}')
            print(f'FootForceEst:\t\t{hstate.footForceEst}')
            # print(hstate.bms)
            # print(foo.motorstate[0].__dict__)
            # pretty_print_obj(hstate)
            print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')

    def testCommand(self):
        conn, hcmd = self.conn, self.hcmd

        hcmd.mode = Mode.VEL_WALK
        hcmd.gaitType = GaitType.TROT
        hcmd.velocity = [0.0, 0.0]
        hcmd.yawSpeed = 2
        hcmd.footRaiseHeight = 0.1
        hcmd.encrypt = False
        cmd_bytes = hcmd.buildCmd(debug=True)
        conn.send(cmd_bytes)
        time.sleep(0.1)

    def sendMovement(self, velx, vely, yaw):
        conn, hcmd = self.conn, self.hcmd

        hcmd.mode = Mode.VEL_WALK
        hcmd.gaitType = GaitType.TROT
        hcmd.velocity = [velx, vely]
        hcmd.yawSpeed = yaw
        hcmd.footRaiseHeight = 0.1
        hcmd.encrypt = False
        cmd_bytes = hcmd.buildCmd(debug=True)
        conn.send(cmd_bytes)
        # time.sleep(0.1)


if __name__ == "__main__":
    listenPort = 8090
    sendPort_low = 8007
    sendPort_high = 8082

    # local_ip_wifi = '192.168.12.14'
    local_ip_wifi = '192.168.12.90'
    local_ip_eth = '192.168.123.69'
    addr_wifi = '192.168.12.1'
    # addr_wifi = '192.168.123.61'
    addr_low = '192.168.123.10'
    addr_high = '192.168.123.161'

    WIFI_DEFAULTS = (listenPort, addr_wifi,       # rasp pi side
                     sendPort_high, local_ip_eth)  # marios side

    roshandler = ROSHandler(WIFI_DEFAULTS)
    print('First Contact...')
    roshandler.firstContact()

    print('Test Command...')
    lx, ly = 0.15, 0.0
    yawRate = 0.0
    roshandler.sendMovement(lx, ly, yawRate)
