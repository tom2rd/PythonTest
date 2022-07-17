#----------------------------------
# ２つのWindowをTkinterで作って、親から子へ行って
# pyserialでコムポートを探して、設定類を書き出し・セット
# １行づつ読み込む
#------------------------------------------

#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText

import sys
import glob
import serial

def serial_ports():
    """ Lists serial port names
 
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
 
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
 
def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None

class ComWindowWidget(tk.Toplevel):
    def baudrate_selected(self,event):  # --- Baudrate ComboBox ---
        print(self.combobox_sp.get())
    def baudrate_enter(self,event):
        print(self.combobox_sp.get())
    def bit_selected(self,event):       # ---- Stop bit ------
        print(self.combobox_bit.get())
    def SetBu_Press(self,event):            
            ser=serial.Serial()
            ser.port=self.combobox_PortNo.get()
            ser.baudrate=self.combobox_sp.get()
            ser.bytesize=int(self.combobox_bit.get())
            ser.parity=get_key_from_value(serial.PARITY_NAMES,self.combobox_pari.get())
            ser.stopbits=float(self.combobox_Stopb.get())
            flow=self.combobox_flo.get()
            if flow=='None':
                ser.xonxoff=False
                ser.rtscts=False
                ser.dsrdtr=False
            elif flow=="Xon/Xoff":
                ser.xonxoff=True
                ser.rtscts=False
                ser.dsrdtr=False
            elif flow=="Rts/Cts":
                ser.xonxoff=False
                ser.rtscts=True
                ser.dsrdtr=False
            elif flow=='Dsr/Dtr':
                ser.xonxoff=False
                ser.rtscts=False
                ser.dsrdtr=True
            else:
                ser.xonxoff=False
                ser.rtscts=False
                ser.dsrdtr=False
            
            serialtimeout=self.combobox_timeout.get()
            if serialtimeout=='None':
                ser.timeout=None
            else:
                ser.timeout=int(serialtimeout)


           # self.tkinterscrolledtext1.insert('end',ser)
           # self.tkinterscrolledtext1.insert('end',"\n")
            
            return ser
    
    def OpenBu_Press(self,event):
        ser=self.SetBu_Press(event)
        #print(ser)
        try:
            ser=serial.Serial(port=ser.port,baudrate=ser.baudrate,bytesize=ser.bytesize,parity=ser.parity,stopbits=ser.stopbits,xonxoff=ser.xonxoff,rtscts=ser.rtscts,dsrdtr=ser.dsrdtr,timeout=ser.timeout)
        except (OSError, serial.SerialException):
            self.tkinterscrolledtext1.insert('end',serial.SerialException)
            self.tkinterscrolledtext1.insert('end',"\n")
            return serial.SerialException
        
        line = ser.readline()
        print(line)
        self.tkinterscrolledtext1.insert('end',"\n")
        self.tkinterscrolledtext1.insert('end',line)
        ser.close()

    def ReadBu_Press(self,event):
        ser=self.SetBu_Press(event)
        line = ser.readline()
        print(line)
        self.tkinterscrolledtext1.insert('end',"\n")
        self.tkinterscrolledtext1.insert('end',line)
        


    def CloseBu_Press(self,event):
        ser=self.SetBu_Press(event)
        ser.close()


    def __init__(self, master=None, **kw):
        super(ComWindowWidget, self).__init__(master, **kw)
        self.label1 = tk.Label(self)
        self.label1.configure(font="TkDefaultFont", text="Port")
        self.label1.grid(column=0, row=0)
        self.label2 = tk.Label(self)
        self.label2.configure(text="Speed")
        self.label2.grid(column=0, row=1)
        self.label3 = tk.Label(self)
        self.label3.configure(text="Bit")
        self.label3.grid(column=0, row=2)
        self.label4 = tk.Label(self)
        self.label4.configure(text="Parity")
        self.label4.grid(column=0, row=3)
        self.label5 = tk.Label(self)
        self.label5.configure(text="StopBit")
        self.label5.grid(column=0, row=4)
        self.label6 = tk.Label(self)
        self.label6.configure(text="Flow")
        self.label6.grid(column=0, row=5)
        self.label7 = tk.Label(self)
        self.label7.configure(text="Timeout")
        self.label7.grid(column=0, row=6)
        #---------------------ComboBoxes---------------------------
        comport_now=serial_ports()
        if len(comport_now) ==0:
            self.combobox_PortNo = ttk.Combobox(self,values=["NONE or Opened"])
            self.combobox_PortNo.current(0)
        else:
            self.combobox_PortNo = ttk.Combobox(self,values=[comport_now])
            self.combobox_PortNo.current(len(self.combobox_PortNo['values'])-1)
        self.combobox_PortNo.grid(column=1, row=0)
        self.combobox_sp = ttk.Combobox(self,values=[2400,9600,57600,115200],textvariable=tk.IntVar())
        self.combobox_sp.current(2)
        self.combobox_sp.bind('<<ComboboxSelected>>',self.baudrate_selected)
        self.combobox_sp.bind('<Enter>',self.baudrate_enter)
        self.combobox_sp.grid(column=1, row=1)
        self.combobox_bit = ttk.Combobox(self,values=[7,8],textvariable=tk.IntVar())
        self.combobox_bit.current(1)
        self.combobox_bit.grid(column=1, row=2)
        parityval=list(serial.PARITY_NAMES.values())
        self.combobox_pari = ttk.Combobox(self,values=parityval,textvariable=tk.StringVar())
        self.combobox_pari.current(0)
        self.combobox_pari.grid(column=1, row=3)
        self.combobox_Stopb = ttk.Combobox(self,values=[1,1.5,2],textvariable=tk.DoubleVar())
        self.combobox_Stopb.current(0)
        self.combobox_Stopb.grid(column=1, row=4)
        self.combobox_flo = ttk.Combobox(self,values=['None','Xon/Xoff','Rts/Cts','Dsr/Dtr'],textvariable=tk.StringVar())
        self.combobox_flo.current(0)
        self.combobox_flo.grid(column=1, row=5)
        self.combobox_timeout=ttk.Combobox(self,values=[None,1,10,0],textvariable=tk.IntVar())
        self.combobox_timeout.current(0)
        self.combobox_timeout.grid(column=1,row=6)
        #-------------- Buttons -----------------
        self.button_set = ttk.Button(self)
        self.button_set.bind('<ButtonPress>',self.SetBu_Press)
        self.button_set.configure(text="Set")
        self.button_set.grid(column=2, padx=2, pady=2, row=1)
        self.button_open = ttk.Button(self)
        self.button_open.configure(text="Open")
        self.button_open.bind('<ButtonPress>',self.OpenBu_Press)
        self.button_open.grid(column=2, padx=2, pady=2, row=2)
        self.button_readline = ttk.Button(self)
        self.button_readline.configure(text="readline")
        self.button_readline.bind('<ButtonPress>',self.ReadBu_Press)
        self.button_readline.grid(column=2, padx=2, pady=2, row=4)
        self.button_close = ttk.Button(self)
        self.button_close.bind('<ButtonPress>',self.CloseBu_Press)
        self.button_close.configure(text="Close")
        self.button_close.grid(column=2, padx=2, pady=2, row=3)
        #------------------------------------------
        self.tkinterscrolledtext1 = ScrolledText(self)
        self.tkinterscrolledtext1.configure(autoseparators="false", setgrid="false")
        self.tkinterscrolledtext1.grid(
            column=0, columnspan=3, padx=5, pady=5, row=8, rowspan=10
        )
        self.configure(height=200, takefocus=False, width=200)
        self.title("Com-Port Setting")



class MainWindowApp(tk.Tk):               #tk.TK のクラス　親アプリウィンドウ
    def __init__(self):
        super().__init__()

        self.geometry('300x200')
        self.title('Main Window')

        # place a button on the root window
        ttk.Button(self,
                text='Open a window',
                command=self.open_window).pack(expand=True)

    def open_window(self):
        window = ComWindowWidget(self)
        window.grab_set()


if __name__ == "__main__":
    app = MainWindowApp()
    app.mainloop()

    
