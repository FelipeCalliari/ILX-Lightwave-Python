import sys
import visa

class ILX_Lightwave:
    def __init__(self, inst_str):
        self.rm = visa.ResourceManager()
        if inst_str in rm.list_resources():
            try:
                self.inst = self.rm.open_resource(inst_str)
                self._programmed = True
            except:
                print("ERROR. There is no {}.".format(inst_str))
                self._programmed = False
            finally:
                if not ("ILX Lightwave,7900 System" in self.inst.query("*IDN?")):
                    print("ERROR. Wrong instrument. Not an ILX Lightwave.")
                    self._programmed = False
        else:
            print("ERROR. There is no {}.".format(inst_str))
            self._programmed = False

    def programmed(self):
        return self._programmed

    def set_local(self):
        self.inst.control_ren(6)
    
    def get_channel(self):
        return self.inst.query("CH?").strip('\r\n')

    def set_channel(self, num):
        if num > 0 and num < 9:
            self.inst.write("CH {}".format(num))
        else:
            print("ERROR: Channel range [1..8]..")

    def get_power(self, ch = -1):
        if ch != -1:
            self.set_channel(ch)

        return self.inst.query("LEVEL?").strip('\r\n')

    def set_power(self, num, ch = -1):
        if ch != -1:
            self.set_channel(ch)

        if num >= -20.00 and num <= +10.50:
            self.inst.write("LEVEL {:4.2f}".format(num))
        else:
            print("ERROR: Power range [-20.00..+10.50] dBm..")
            
    def get_status(self, ch = -1):
        if ch != -1:
            self.set_channel(ch)

        return 'ON' if self.inst.query("OUT?").strip('\r\n') == '1' else 'OFF'

    def set_status(self, num, ch = -1):
        if ch == -1:
            status = 'ON' if num == 1 else 'OFF' 
            self.inst.write("OUT {}".format(status))
        else:
            self.set_channel(ch)
            status = 'ON' if num == 1 else 'OFF' 
            self.inst.write("OUT {}".format(status))

    def get_wavelength(self, ch = -1):
        if ch == -1:
            return self.inst.query("WAVE?").strip('\r\n')
        else:
            self.set_channel(ch)
            return self.inst.query("WAVE?").strip('\r\n')            

    def set_wavelength(self, num, ch = -1):
        if ch != -1:
            self.set_channel(ch)

        self.inst.write("WAVE {:8.3f}".format(float(num)))

    def get_output(self, ch = -1):
        if ch != -1:
            CH = channel
            self.set_channel(CH)
        else:
            CH = self.inst.query("CH?").strip('\r\n')

        OUT = 'ON' if self.inst.query("OUT?").strip('\r\n') == '1' else 'OFF'
        PW  = float(self.inst.query("LEVEL?").strip('\r\n'))
        WL  = float(self.inst.query("WAVE?").strip('\r\n'))
        return "CH{} {:3} - power {:6.2f}dBm - wavelength {:8.3f}nm".format(CH, OUT, PW, WL)

    def set_output(self, ch, out, pw, wl):
        self.set_channel(ch)
        self.set_status(out)
        self.set_power(pw)
        self.set_wavelength(wl)

    
