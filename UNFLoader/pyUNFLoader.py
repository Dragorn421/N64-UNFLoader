from pathlib import Path
import ctypes
import types
import enum
import logging

# To change the logging level:
# pyUNFLoader.LOGGER.setLevel(logging.INFO)
LOGGER = logging.Logger("pyUNFLoader")
_LOG_CONSOLE_HANDLER = logging.StreamHandler()
_LOG_FORMATTER = logging.Formatter(
    "{name}:{funcName}:{levelname}: {message}",
    style="{",
)
_LOG_CONSOLE_HANDLER.setFormatter(_LOG_FORMATTER)
LOGGER.addHandler(_LOG_CONSOLE_HANDLER)

UNFLoader = ctypes.CDLL(Path(__file__).parent / "UNFLoader.so")

# Used to prevent garbage collection, by the Python GC,
# of data the C/C++ side holds on after getting it from Python
_NOGC = types.SimpleNamespace()


#
# enums
#


class CartType(enum.IntEnum):
    CART_NONE = 0
    CART_64DRIVE1 = 1
    CART_64DRIVE2 = 2
    CART_EVERDRIVE = 3
    CART_SC64 = 4


class CICType(enum.IntEnum):
    CIC_NONE = -1
    CIC_6101 = 0
    CIC_6102 = 1
    CIC_7101 = 2
    CIC_7102 = 3
    CIC_X103 = 4
    CIC_X105 = 5
    CIC_X106 = 6
    CIC_5101 = 7
    CIC_8303 = 8


class SaveType(enum.IntEnum):
    SAVE_NONE = 0
    SAVE_EEPROM4K = 1
    SAVE_EEPROM16K = 2
    SAVE_SRAM256 = 3
    SAVE_FLASHRAM = 4
    SAVE_SRAM768 = 5
    SAVE_FLASHRAMPKMN = 6


class USBDataType(enum.IntEnum):
    DATATYPE_TEXT = 0x01
    DATATYPE_RAWBINARY = 0x02
    DATATYPE_HEADER = 0x03
    DATATYPE_SCREENSHOT = 0x04
    DATATYPE_HEARTBEAT = 0x05


class ProtocolVer(enum.IntEnum):
    PROTOCOL_VERSION1 = 0x00
    PROTOCOL_VERSION2 = 0x02


class DeviceError(enum.IntEnum):
    DEVICEERR_OK = 0
    DEVICEERR_NOTCART = enum.auto()
    DEVICEERR_USBBUSY = enum.auto()
    DEVICEERR_NODEVICES = enum.auto()
    DEVICEERR_CARTFINDFAIL = enum.auto()
    DEVICEERR_CANTOPEN = enum.auto()
    DEVICEERR_FILEREADFAIL = enum.auto()
    DEVICEERR_RESETFAIL = enum.auto()
    DEVICEERR_RESETPORTFAIL = enum.auto()
    DEVICEERR_TIMEOUTSETFAIL = enum.auto()
    DEVICEERR_PURGEFAIL = enum.auto()
    DEVICEERR_READFAIL = enum.auto()
    DEVICEERR_WRITEFAIL = enum.auto()
    DEVICEERR_WRITEZERO = enum.auto()
    DEVICEERR_CLOSEFAIL = enum.auto()
    DEVICEERR_BITMODEFAIL_RESET = enum.auto()
    DEVICEERR_BITMODEFAIL_SYNCFIFO = enum.auto()
    DEVICEERR_SETDTRFAIL = enum.auto()
    DEVICEERR_CLEARDTRFAIL = enum.auto()
    DEVICEERR_GETMODEMSTATUSFAIL = enum.auto()
    DEVICEERR_TXREPLYMISMATCH = enum.auto()
    DEVICEERR_READCOMPSIGFAIL = enum.auto()
    DEVICEERR_NOCOMPSIG = enum.auto()
    DEVICEERR_READPACKSIZEFAIL = enum.auto()
    DEVICEERR_BADPACKSIZE = enum.auto()
    DEVICEERR_MALLOCFAIL = enum.auto()
    DEVICEERR_UPLOADCANCELLED = enum.auto()
    DEVICEERR_TIMEOUT = enum.auto()
    DEVICEERR_POLLFAIL = enum.auto()
    DEVICEERR_64D_BADCMP = enum.auto()
    DEVICEERR_64D_8303USB = enum.auto()
    DEVICEERR_64D_CANTDEBUG = enum.auto()
    DEVICEERR_64D_BADDMA = enum.auto()
    DEVICEERR_64D_DATATOOBIG = enum.auto()
    DEVICEERR_SC64_CMDFAIL = enum.auto()
    DEVICEERR_SC64_COMMFAIL = enum.auto()
    DEVICEERR_SC64_CTRLRELEASEFAIL = enum.auto()
    DEVICEERR_SC64_CTRLRESETFAIL = enum.auto()
    DEVICEERR_SC64_FIRMWARECHECKFAIL = enum.auto()
    DEVICEERR_SC64_FIRMWAREUNSUPPORTED = enum.auto()


#
# constants
#


# The latest version of the usb protocol handled by the device implementation
USBPROTOCOL_LATEST = ProtocolVer(
    ctypes.c_int.in_dll(UNFLoader, "usbprotocol_latest").value
)


#
# Main device functions
#


# void        device_initialize();
UNFLoader.cw_device_initialize.argtypes = []
UNFLoader.cw_device_initialize.restype = None


def device_initialize():
    UNFLoader.cw_device_initialize()


# DeviceError device_find();
UNFLoader.cw_device_find.argtypes = []
UNFLoader.cw_device_find.restype = ctypes.c_int


def device_find():
    return DeviceError(UNFLoader.cw_device_find())


# DeviceError device_open();
UNFLoader.cw_device_open.argtypes = []
UNFLoader.cw_device_open.restype = ctypes.c_int


def device_open():
    return DeviceError(UNFLoader.cw_device_open())


# uint32_t    device_getmaxromsize();
UNFLoader.cw_device_getmaxromsize.argtypes = []
UNFLoader.cw_device_getmaxromsize.restype = ctypes.c_uint32


def device_getmaxromsize():
    return UNFLoader.cw_device_getmaxromsize()


# uint32_t    device_rompadding(uint32_t romsize);
UNFLoader.cw_device_rompadding.argtypes = [ctypes.c_uint32]
UNFLoader.cw_device_rompadding.restype = ctypes.c_uint32


def device_rompadding():
    return UNFLoader.cw_device_rompadding()


# bool        device_explicitcic();
UNFLoader.cw_device_explicitcic.argtypes = []
UNFLoader.cw_device_explicitcic.restype = ctypes.c_bool


def device_explicitcic() -> bool:
    return UNFLoader.cw_device_explicitcic()


# bool        device_isopen();
UNFLoader.cw_device_isopen.argtypes = []
UNFLoader.cw_device_isopen.restype = ctypes.c_bool


def device_isopen():
    return UNFLoader.cw_device_isopen()


# DeviceError device_testdebug();
UNFLoader.cw_device_testdebug.argtypes = []
UNFLoader.cw_device_testdebug.restype = ctypes.c_int


def device_testdebug():
    return DeviceError(UNFLoader.cw_device_testdebug())


# DeviceError device_sendrom(FILE* rom, uint32_t filesize);
# DeviceError cw_device_sendrom(int fd, uint32_t filesize);
UNFLoader.cw_device_sendrom.argtypes = [ctypes.c_int, ctypes.c_uint32]
UNFLoader.cw_device_sendrom.restype = ctypes.c_int


def device_sendrom(fd: int, filesize: int):
    # Pass a file descriptor to the C wrapper, which makes a FILE* from it
    # The file descriptor is to be closed by the caller
    return DeviceError(UNFLoader.cw_device_sendrom(fd, filesize))


# DeviceError device_senddata(USBDataType datatype, byte* data, uint32_t size);
UNFLoader.cw_device_senddata.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
]
UNFLoader.cw_device_senddata.restype = ctypes.c_int


def device_senddata(datatype: USBDataType, data: bytes):
    size = len(data)
    data_u8array = (ctypes.c_uint8 * size).from_buffer_copy(data)
    return DeviceError(UNFLoader.cw_device_senddata(datatype.value, data_u8array, size))


# DeviceError device_receivedata(uint32_t* dataheader, byte** buff);
UNFLoader.cw_device_receivedata.argtypes = [
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8)),
]
UNFLoader.cw_device_receivedata.restype = ctypes.c_int


def device_receivedata() -> (
    tuple[DeviceError, USBDataType, bytes] | tuple[DeviceError, None, None]
):
    # Call the C wrapper function, passing pointers to local variables
    dataheader_holder = ctypes.c_uint32(0)
    buffp = ctypes.POINTER(ctypes.c_uint8)()
    err = DeviceError(
        UNFLoader.cw_device_receivedata(
            ctypes.pointer(dataheader_holder),
            ctypes.pointer(buffp),
        )
    )

    dataheader = dataheader_holder.value
    # buffp is False-y when NULL
    if dataheader != 0 and buffp:
        # Parse the data header
        size = dataheader & 0x00FF_FFFF
        command = USBDataType((dataheader >> 24) & 0xFF)
        # Copy the data to bytes
        buff_bytes = bytes(buffp[:size])
    else:
        # No data received
        command = None
        buff_bytes = None

    return err, command, buff_bytes


# DeviceError device_close();
UNFLoader.cw_device_close.argtypes = []
UNFLoader.cw_device_close.restype = ctypes.c_int


def device_close():
    return DeviceError(UNFLoader.cw_device_close())


#
# Device configuration
#

# bool     device_setrom(char* path);
UNFLoader.cw_device_setrom.argtypes = [ctypes.c_char_p]
UNFLoader.cw_device_setrom.restype = ctypes.c_bool


def device_setrom(path: bytes) -> bool:
    path_ctypes = ctypes.create_string_buffer(path)
    ret = UNFLoader.cw_device_setrom(path_ctypes)
    _NOGC.device_setrom_path_ctypes = path_ctypes
    return ret


# void     device_setcart(CartType cart);
UNFLoader.cw_device_setcart.argtypes = [ctypes.c_int]
UNFLoader.cw_device_setcart.restype = None


def device_setcart(cart: CartType):
    UNFLoader.cw_device_setcart(cart.value)


# void     device_setcic(CICType cic);
UNFLoader.cw_device_setcic.argtypes = [ctypes.c_int]
UNFLoader.cw_device_setcic.restype = None


def device_setcic(cic: CICType):
    UNFLoader.cw_device_setcic(cic.value)


# void     device_setsave(SaveType save);
UNFLoader.cw_device_setsave.argtypes = [ctypes.c_int]
UNFLoader.cw_device_setsave.restype = None


def device_setsave(save: SaveType):
    UNFLoader.cw_device_setsave(save.value)


# char*    device_getrom();
UNFLoader.cw_device_getrom.argtypes = []
UNFLoader.cw_device_getrom.restype = ctypes.c_char_p


def device_getrom() -> bytes | None:
    # ctypes seems to automatically return bytes, or None for NULL.
    return UNFLoader.cw_device_getrom()


# CartType device_getcart();
UNFLoader.cw_device_getcart.argtypes = []
UNFLoader.cw_device_getcart.restype = ctypes.c_int


def device_getcart():
    return CartType(UNFLoader.cw_device_getcart())


# CICType  device_getcic();
UNFLoader.cw_device_getcic.argtypes = []
UNFLoader.cw_device_getcic.restype = ctypes.c_int


def device_getcic():
    return CICType(UNFLoader.cw_device_getcic())


# SaveType device_getsave();
UNFLoader.cw_device_getsave.argtypes = []
UNFLoader.cw_device_getsave.restype = ctypes.c_int


def device_getsave():
    return SaveType(UNFLoader.cw_device_getsave())


#
# Upload related
#

# void  device_cancelupload();
UNFLoader.cw_device_cancelupload.argtypes = []
UNFLoader.cw_device_cancelupload.restype = None


def device_cancelupload():
    UNFLoader.cw_device_cancelupload()


# bool  device_uploadcancelled();
UNFLoader.cw_device_uploadcancelled.argtypes = []
UNFLoader.cw_device_uploadcancelled.restype = ctypes.c_bool


def device_uploadcancelled():
    UNFLoader.cw_device_uploadcancelled()


# void  device_setuploadprogress(float progress);
UNFLoader.cw_device_setuploadprogress.argtypes = [ctypes.c_float]
UNFLoader.cw_device_setuploadprogress.restype = None


def device_setuploadprogress():
    UNFLoader.cw_device_setuploadprogress()


# float device_getuploadprogress();
UNFLoader.cw_device_getuploadprogress.argtypes = []
UNFLoader.cw_device_getuploadprogress.restype = ctypes.c_float


def device_getuploadprogress():
    UNFLoader.cw_device_getuploadprogress()


#
# Protocol version handling
#

# void        device_setprotocol(ProtocolVer version);
UNFLoader.cw_device_setprotocol.argtypes = [ctypes.c_int]
UNFLoader.cw_device_setprotocol.restype = None


def device_setprotocol(version: ProtocolVer):
    UNFLoader.cw_device_setprotocol(version.value)


# ProtocolVer device_getprotocol();
UNFLoader.cw_device_getprotocol.argtypes = []
UNFLoader.cw_device_getprotocol.restype = ctypes.c_int


def device_getprotocol():
    return ProtocolVer(UNFLoader.cw_device_getprotocol())


#
# helpers
#


class DeviceErrorNotOK(Exception):
    pass


def helper_check_device_error(err: DeviceError):
    if err != DeviceError.DEVICEERR_OK:
        raise DeviceErrorNotOK(err.name, err.value)


# the default protocol is PROTOCOL_VERSION1 for backwards compatibility
# the protocol is to be upgraded to the adequate version when receiving a heartbeat
def helper_init(protocol: ProtocolVer = ProtocolVer.PROTOCOL_VERSION1):
    device_initialize()
    # Note: protocol is set in device_initialize(),
    # so any call to device_setprotocol must come after
    device_setprotocol(protocol)
    helper_check_device_error(device_find())


def helper_with_open():
    class HelperDeviceOpenContextManager:
        def __enter__(self):
            helper_check_device_error(device_open())

        def __exit__(self, exc_type, exc_val, exc_tb):
            helper_check_device_error(device_close())

    return HelperDeviceOpenContextManager()


# sentinel object indicating a function argument was left default
# and the corresponding thing should be automatically detected
_AUTO_DETECT = object()


def helper_sendrom(
    rom_path,
    cic: CICType | None = _AUTO_DETECT,
    save: SaveType | None = SaveType.SAVE_NONE,
):
    """
    Upload a rom and set relevant settings

    The `cic` and `save` arguments can be set to `None` to not be changed by this function, or to specific values.
    The default for `cic` is to auto-detect the cic type from the rom if needed.
    The default for `save` is `SaveType.SAVE_NONE`.
    """
    rom_path = Path(rom_path)
    # encode path, stat and open the rom file before calling device_ functions,
    # to try avoid setting a partial state in case something fails
    rom_path_bytes = bytes(rom_path)
    rom_stat = rom_path.stat()
    filesize = rom_stat.st_size
    with rom_path.open("rb") as rom_f:
        fd = rom_f.fileno()
        setrom_result = device_setrom(rom_path_bytes)
        if not setrom_result:
            # Currently the only way device_setrom can fail is if rom_path isn't a regular file,
            # which is unlikely at this point given Python has successfully opened it for reading.
            # TODO But maybe this would raise in the case of symlinks or similar?
            raise Exception("device_setrom() didn't succeed")
        if cic is not None:
            if cic is _AUTO_DETECT:
                # Mostly ignore the "cic changed" return value, it's not interesting to us
                if device_explicitcic():
                    LOGGER.debug(f"Autodetected CIC: {device_getcic()!r}")
            else:
                device_setcic(cic)
        if save is not None:
            # auto "detecting" save type involves parsing the advanced rom header
            # TODO ?
            assert save is not _AUTO_DETECT
            device_setsave(save)
        helper_check_device_error(device_sendrom(fd, filesize))


class HeartbeatHandlingError(Exception):
    pass


def helper_handle_heartbeat(buffer: bytes):
    # this function mimics debug_handle_heartbeat

    if len(buffer) < 4:
        raise HeartbeatHandlingError("Error: Malformed heartbeat received")

    # unpacking the version and protocol references usb_sendheartbeat (n64 side)
    # since endianness makes the pc side weird
    protocol_version_int = (buffer[0] << 8) | buffer[1]
    heartbeat_version = (buffer[2] << 8) | buffer[3]

    LOGGER.debug(
        "Handling heartbeat:"
        f" protocol_version_int={protocol_version_int}"
        f" heartbeat_version={heartbeat_version}"
    )

    if protocol_version_int > USBPROTOCOL_LATEST:
        raise HeartbeatHandlingError(
            f"USB protocol {protocol_version_int} unsupported."
            " Your UNFLoader is probably out of date."
        )

    protocol_version = ProtocolVer(protocol_version_int)
    device_setprotocol(protocol_version)
    LOGGER.info(f"Protocol version set to {protocol_version!r} from heartbeat")

    if heartbeat_version == 0x01:
        pass
    else:
        raise HeartbeatHandlingError(
            f"Heartbeat version {heartbeat_version} unsupported."
            " Your UNFLoader is probably out of date."
        )


def helper_receivedata(
    handle_heartbeat=True,
) -> tuple[USBDataType, bytes] | tuple[None, None]:
    err, datatype, data = device_receivedata()
    helper_check_device_error(err)
    if datatype == USBDataType.DATATYPE_HEARTBEAT:
        if handle_heartbeat:
            LOGGER.info("Handling heartbeat from helper_receivedata")
            helper_handle_heartbeat(data)
            return None, None
    return datatype, data


def helper_sendtext(text: str, encoding="utf-8"):
    helper_check_device_error(
        device_senddata(
            USBDataType.DATATYPE_TEXT,
            # A trailing \0 is not strictly necessary, but add it to be safe
            # (the current behavior around '\0's doesn't look final)
            text.encode(encoding=encoding) + b"\0",
        )
    )
