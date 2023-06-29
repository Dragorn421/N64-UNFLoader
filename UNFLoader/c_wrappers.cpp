#include <stdio.h>
#include "device.h"

/**
 * C wrappers of device_ functions, for using UNFLoader as a shared object / DLL.
 */
extern "C"
{
    int usbprotocol_latest = USBPROTOCOL_LATEST;

    // Main device functions
    void cw_device_initialize() { device_initialize(); }
    DeviceError cw_device_find() { return device_find(); }
    DeviceError cw_device_open() { return device_open(); }
    uint32_t cw_device_getmaxromsize() { return device_getmaxromsize(); }
    uint32_t cw_device_rompadding(uint32_t romsize) { return device_rompadding(romsize); }
    bool cw_device_explicitcic() { return device_explicitcic(); }
    bool cw_device_isopen() { return device_isopen(); }
    DeviceError cw_device_testdebug() { return device_testdebug(); }
    DeviceError cw_device_sendrom(int fd, uint32_t filesize)
    {
        FILE *rom = fdopen(fd, "rb");
        // Closing the file descriptor is left to the caller
        return device_sendrom(rom, filesize);
    }
    DeviceError cw_device_senddata(USBDataType datatype, byte *data, uint32_t size) { return device_senddata(datatype, data, size); }
    DeviceError cw_device_receivedata(uint32_t *dataheader, byte **buff) { return device_receivedata(dataheader, buff); }
    DeviceError cw_device_close() { return device_close(); }

    // Device configuration
    bool cw_device_setrom(char *path) { return device_setrom(path); }
    void cw_device_setcart(CartType cart) { device_setcart(cart); }
    void cw_device_setcic(CICType cic) { device_setcic(cic); }
    void cw_device_setsave(SaveType save) { device_setsave(save); }
    char *cw_device_getrom() { return device_getrom(); }
    CartType cw_device_getcart() { return device_getcart(); }
    CICType cw_device_getcic() { return device_getcic(); }
    SaveType cw_device_getsave() { return device_getsave(); }

    // Upload related
    void cw_device_cancelupload() { device_cancelupload(); }
    bool cw_device_uploadcancelled() { return device_uploadcancelled(); }
    void cw_device_setuploadprogress(float progress) { device_setuploadprogress(progress); }
    float cw_device_getuploadprogress() { return device_getuploadprogress(); }

    // Protocol version handling
    void cw_device_setprotocol(ProtocolVer version) { device_setprotocol(version); }
    ProtocolVer cw_device_getprotocol() { return device_getprotocol(); }
}
