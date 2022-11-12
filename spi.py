import binascii

def wr(spi,cs,m,n):
    cs.value(0)
    spi.write(m)
    r = spi.read(n)
    cs.value(1)
    return r
    

cs = machine.Pin(17, machine.Pin.OUT)
spi = machine.SPI(0,
                  baudrate=80000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(18),
                  mosi=machine.Pin(19),
                  miso=machine.Pin(16))
##W25Q64CV 80Mhz
#print(binascii.hexlify(wr(spi, cs, bytearray([0x9F]), 3)))            # RDID
#print(binascii.hexlify(wr(spi, cs, bytearray([0xAB,0,0,0]), 1)))
#print(binascii.hexlify(wr(spi, cs, bytearray([0x90,0,0,0]), 2)))
#print(binascii.hexlify(wr(spi, cs, bytearray([0x5A,0,0,0x0,0]), 8)))
#print(binascii.hexlify(wr(spi, cs, bytearray([0x4B,0,0,0,0]), 8)))
#print(binascii.hexlify(wr(spi, cs, bytearray([0x03,0,0,0]), 32*256)))    # 

##MX25L3233F 50Mhz
#print(binascii.hexlify(wr(spi, cs, bytearray([0x9F]), 3)))            # RDID
#print(binascii.hexlify(wr(spi, cs, bytearray([0x90,0,0,0]), 2)))      # REMS
#print(binascii.hexlify(wr(spi, cs, bytearray([0x5A,0,0,0x60,0]), 8))) # SFDP

#f = open("fw1.bin", "w")
#for i in range(0, 16):
#    print(i)
#    d = wr(spi, cs, bytearray([0x03,i,0,0]), 256*256)    # READ
#    f.write(d)
#    f.flush()
#
#f.close()
#print("done")
