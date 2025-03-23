#
set_units -time ps  
#set_units -capacitance pF
#set_units -resistance kohm
#set_units -current mA
# clock definiton in 10MHz

## Clock 250MHz
create_clock  -name CLK -period 6000 -waveform { 0  3000 } [get_ports CLK]
#create_clock -name CLK [get_ports CLK]

## delay from clock edge to data input edge 
#set_input_delay 1 -clock CLK [all_inputs] 
#set_max_delay 6000 -from [all_inputs] -to [all_inputs]
set_input_delay 1 -clock CLK [remove_from_collection [all_inputs] [get_ports CLK]]
set_max_delay 6000 -from [remove_from_collection [all_inputs] [get_ports CLK]] -to [all_outputs]

## margine  
set_output_delay 1 -clock CLK [all_outputs]
#set_min_delay 94.23 -from [all_inputs] -to [all_inputs]
# output load [in library unit, pF]
set_load 0.01 [all_outputs]

## set input transition time
#set_input_transition 0.1 [all_inputs]
