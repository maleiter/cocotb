import cocotb
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
import debugpy

def initialize_debugger():
    debugpy.listen(("127.0.0.1", 4001))
    print("Debugger is ready to be attached, press F5", flush=True)
    debugpy.wait_for_client()
    print("Visual Studio Code debugger is now attached", flush=True)


@cocotb.test()
async def mixed_language_test(dut):
    """Try accessing handles and setting values in a mixed language environment."""
    await Timer(100, units="ns")

    verilog = dut.i_swapper_sv
    dut._log.info("Got: %s" % repr(verilog._name))

    vhdl = dut.i_swapper_vhdl
    dut._log.info("Got: %s" % repr(vhdl._name))

    initialize_debugger()

    # setup default valies
    dut.reset_n.value = 0
    dut.stream_out_ready.value = 1

    dut.stream_in_startofpacket.value = 0     
    dut.stream_in_endofpacket.value = 0    
    dut.stream_in_data.value = 0
    dut.stream_in_valid.value = 1
    dut.stream_in_empty.value = 0

    dut.csr_address.value = 0
    dut.csr_read.value = 0
    dut.csr_write.value = 0
    dut.csr_writedata.value = 0

    # reset cycle
    await Timer(100, units="ns")
    dut.reset_n.value = 1
    await Timer(100, units="ns")

    # start clock
    cocotb.start_soon(Clock(dut.clk, 10, units='ns').start())
    await Timer(500, units="ns")

    # transmit some packages
    for pkg in range(1,5):
        print("pkg#" + str(pkg))
        for i in range(1,10):  
            dut.stream_in_startofpacket.value = 1 == 1;      
            dut.stream_in_endofpacket.value = 1 == 20;      
            dut.stream_in_data.value = i + 0x81FFFFFF2B00
            dut.stream_in_valid.value = 1
            await RisingEdge(dut.clk)
            dut.stream_in_valid.value = 0
            await RisingEdge(dut.clk)



    #assert int(verilog.reset_n) == int(vhdl.reset_n), "reset_n signals were different"

    # Try accessing an object other than a port...
    #verilog.flush_pipe.value
    #vhdl.flush_pipe.value
