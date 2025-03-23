set hdlin_unsigned_integers "false"
set verilogout_no_tri "true"


set library_path "xxxx/design/re65_lib_2022/liberty/"
lappend search_path $library_path 
set MYLIBRARY {REL65_KU01_SVT_0p7}
set target_library {REL65_KU01_SVT_0p7.db}
set synthetic_library "dw_foundation.sldb"
set link_library [list $target_library $synthetic_library]


set DESIGN_PATH "../rtl_design/"
set CURRENT_DESIGN $::CURRENT_DESIGN
read_file -format verilog $DESIGN_PATH${CURRENT_DESIGN}.v
current_design $CURRENT_DESIGN


#set_max_delay 5000 -from [all_inputs] -to [all_outputs]
set SDC_FILE_PATH "sdc/main.sdc"
source $SDC_FILE_PATH
check_design 


# synthesis
#compile -ungroup_all
compile
compile_ultra 

define_name_rules verilog -allowed "A-Z0-9_"
change_names -rules verilog -hierarchy 
if {![file exist $CURRENT_DESIGN]} {
    file mkdir $CURRENT_DESIGN
}
write -f verilog -hier -o $CURRENT_DESIGN/${CURRENT_DESIGN}.v
write -f ddc -hier -o $CURRENT_DESIGN/${CURRENT_DESIGN}.ddc
write_sdf -version 1.0 $CURRENT_DESIGN/${CURRENT_DESIGN}.sdf 


# generte reports 
redirect $CURRENT_DESIGN/${CURRENT_DESIGN}.area.log { report_area }
redirect $CURRENT_DESIGN/${CURRENT_DESIGN}.min.timing.log { report_timing -delay min -max_path 20 }
redirect $CURRENT_DESIGN/${CURRENT_DESIGN}.max.timing.log { report_timing -delay max -max_path 20 }
redirect $CURRENT_DESIGN/${CURRENT_DESIGN}.power.log { report_power }
quit
