def initrc():
    cap = cv2.VideoCapture("/dev/video0")
    dummy_mode=DUMMY_CAMERA|DUMMY_PRINTER
    base_url="http://test111.frp-calvinlin.sealosgzg.site/"
    #mcu_serial=aioserial.AioSerial(port='/dev/ttyACM1',baudrate=9600)#
#    printer_serial=aioserial.AioSerial(port='/dev/null',baudrate=9600)#
#    printer=AioPrinter(printer_serial)
#    printer.magic.encoding="GBK"
#    printer.magic.encoder=type("a",(),{"encode":lambda  text,encoding:text.encode(encoding)})# This make Chinese work
#    printer.magic.disabled=True
#    printer.profile.profile_data["fonts"]['0']['columns']=30
    return locals()
