import pyUNFLoader

pyUNFLoader.helper_init()

print("Cart:", repr(pyUNFLoader.device_getcart()))

with pyUNFLoader.helper_with_open():
    rompath = "/home/dragorn421/Documents/n64homebrew/gltest/gltest.z64"

    pyUNFLoader.helper_sendrom(rompath)

    pyUNFLoader.helper_sendtext("Hello from python")

    pyUNFLoader.helper_check_device_error(
        pyUNFLoader.device_senddata(
            pyUNFLoader.USBDataType.DATATYPE_RAWBINARY,
            bytes([1, 2, 3]),
        )
    )

    while True:
        datatype, data = pyUNFLoader.helper_receivedata()
        if datatype is not None:
            print(datatype.name, data)
            if datatype == pyUNFLoader.USBDataType.DATATYPE_TEXT:
                print(data.decode("utf-8", errors="replace"), end="")
        else:
            import time

            time.sleep(0.01)
