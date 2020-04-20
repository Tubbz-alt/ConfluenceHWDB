
set MAC_POOL_FILE  "/afs/slac/g/reseng/hwdb/macfile"
set MAC_ADDR_POOL_BASES [list "Reserved" "08:00:56:00:40:00"]

set BLANK_NKY_PATH "/afs/slac/g/reseng/hwdb/"

set DTM_SIGNATURE "arm_dap_0 xc7z030_1"
set DPM_SIGNATURE "arm_dap_0 xc7z045_1 arm_dap_2 xc7z045_3"

set KNOWN_DEVICES  "xc7z045* xc7z030*"

proc table_from_efuse {efuse} {
  return [expr ("0x$efuse" & 0xFFFFc000)>>14]
}

proc offset_from_efuse {efuse} {
  return [expr ("0x$efuse" & 0x00003fff)]
}

proc base_from_table {table} {
  global MAC_ADDR_POOL_BASES
  if {$table > [llength $MAC_ADDR_POOL_BASES]-1} {
    return "Invalid Table"
  }
  return [lindex $MAC_ADDR_POOL_BASES $table]
}

proc efuse_from_mac {base addr} {

  global MAC_ADDR_POOL_BASES
  set table [lsearch -exact $MAC_ADDR_POOL_BASES $base]
  if { $table == -1} {
    return -code error "-ERROR- Base MAC $base not known"
  }
  set table [format "0x%x" $table]

  regsub -all ":" $base "" base
  regsub -all ":" $addr "" addr

  set offset [format "0x%x" [expr "0x$addr" - "0x$base"]]
  
  set efuse [format "%08x" [expr ($table<<14) | ($offset & 0x3fff)]]
  
  return $efuse
  
}


proc mac_from_efuse {efuse} {
  
  set table  [table_from_efuse  $efuse]
  set offset [offset_from_efuse $efuse]

  global MAC_ADDR_POOL_BASES
  if {$table > [llength $MAC_ADDR_POOL_BASES]-1} {
    return "Invalid Table"
  }

  if {$table == 0} {
    return "Invalid Table"
  }

  set base [base_from_table $table]
  regsub -all ":" $base "" base
  
  set mac [format "%012X" [expr ("0x$base" + $offset)]]
  
  foreach {a b} [split $mac {}] {
    lappend macaddr "$a$b"
  }
  set mac [join $macaddr ":"]
  
  return $mac
}    

proc selectTarget {esn} {
  
  set targets [get_hw_targets *$esn]
    
  set target ""
  
  if {[llength $targets] == 1} {
    set target [lindex $targets 0]
  } else {
    set index 0
    foreach t $targets {
      puts "$index: $t"
      incr index
    }
    while {$target == ""} {
      puts -nonewline "Choose a cable: "
      flush stdout
      gets stdin choice
      if {[string is integer -strict $choice]} {
	set target [lindex $targets $choice]
      } else {
	set target ""
      }
    }    
  }
  return $target
}

proc identifyCable {devices filter} {
  global DTM_SIGNATURE
  global DPM_SIGNATURE
  
  if { $devices == $DTM_SIGNATURE && $filter != "DPM" } { return "DTM" } 
  if { $devices == $DPM_SIGNATURE && $filter != "DTM" } { return "DPM" }
  
  return ""   
}

proc burnEFUSE {device efuse} {

  current_hw_device $device
  set nky [format "%s%s.nky" $BLANK_NKY_PATH [get_property PART [current_hw_device]]]
  create_hw_bitstream -hw_device [current_hw_device] -nky $nky
  program_hw_devices -key {efuse} -user_efuse $efuse [current_hw_device]
}

proc getEFUSE { device } {
  current_hw_device $device
  return [get_property {REGISTER.EFUSE.FUSE_USER} [current_hw_device]]
}

proc burnMACs {target devices cmb} {
  
  set ret [list]
  
  foreach dev $devices {
    if { [getEFUSE $dev] != 0 } {
      puts [string repeat "*" 80]
      puts "eFUSE readback NON-ZERO on device $dev, not proceeding with burn"
      puts [string repeat "*" 80]
      return $ret
    }
  }
  
  puts "About to allocate and burn [llength $devices] MAC addresses into $cmb registers"

  puts -nonewline "DO YOU WANT TO PROCEED? (y/N) "
  flush stdout
  gets stdin choice
  if {"Y" != [string toupper $choice]} {
    puts "OK - you are off the hook. Not proceeding."
    return $ret
  }
  
  global MAC_POOL_FILE
  set alloc [exec allocate_mac.py --macfile $MAC_POOL_FILE --number [llength $devices]]
  set alloc  [split $alloc " "]
  
  set base [lshift alloc]
  set addrs $alloc
  
  if {[llength $addrs] != [llength $devices]} {
    puts [string repeat "*" 80]
    puts "Number of allocated MACs not equal to number of devices"
    puts [string repeat "*" 80]
    return $ret
  }
  
  foreach addr $addrs {
    lappend efuses [efuse_from_mac $base $addr]
  }
  
  for {set i 0} {$i<[llength $devices]} {incr i} {
    set dev   [lindex $devices $i]
    set efuse [lindex $efuses $i]
    set addr  [lindex $addrs $i]
    
    puts "Burning eFUSE $efuse (MAC $addr) to $dev"
    burnEFUSE $dev $efuse

    set target [current_hw_target]
    close_hw_target -quiet
    open_hw_target -quiet $target 
    
    set compare [getEFUSE $dev]
    
    if {"0x$compare" != "0x$efuse"} {
      puts [string repeat "*" 80]
      puts "-ERROR- eFUSE readback mismatch on device $dev: wrote $efuse, read $compare"
      puts [string repeat "*" 80]
      lappend ret "Failed"
    } else {
      puts "eFUSE readback matched for device $dev. Congratulations"
      lappend ret $addr
    }
    
  }
  
  return $ret
}

proc dumpMACs {target devices cmb} {
  
  set format_string "| %10s | %8s | %12s | %17s | %17s |"
  
  puts [string repeat "=" 80]
  puts [format "| %-7s %68s |" $cmb $target]
  puts [string repeat "=" 80]
  puts [format $format_string "Device" "eFUSE" "Table/Offset" "Base MAC" "Device MAC"]
  puts [string repeat "-" 80]
  
  foreach dev $devices {
    set efuse [getEFUSE $dev]
    puts [format $format_string $dev $efuse "[table_from_efuse $efuse]/[offset_from_efuse $efuse]" [base_from_table [table_from_efuse $efuse]] [mac_from_efuse $efuse]]
  }
  
  puts [string repeat "=" 80]
}

proc usage {} {
  puts ""
  puts "usage:"
  puts { efuse_mac.sh [--help] (--burn | --dump) [--url URL] [--esn ESN] [--dpm | --dtm]}
  puts "\n"
  puts {arguments:}
  puts { --help      show this help message and exit}
  puts { --burn      Allocate MAC addresses and burn eFUSEs}
  puts { --dump      Dump the eFUSE contents}
  puts { --url URL   host:port of a Vivado hardware server}
  puts { --esn ESN   Xilinx dongle ESN}
  puts { --dpm       Program a DPM}
  puts { --dtm       Program a DTM}
  puts ""
}

proc lshift {listvar} {
  upvar 1 $listvar L
  set r [lindex $L 0]
  set L [lreplace $L [set L 0] 0]
  return $r
}

## Here's the "main"

set error 0

set url  "" 
set esn  *
set cmb ""
set force 0
set burn 0
set dump 0

while {[llength $argv]} {
  set flag [lshift argv]
  switch -exact -- $flag {
    --dump  { set dump 1 }
    --burn  { set burn 1 }
    --dtm   { set cmb  "DTM" }
    --dpm   { set cmb  "DPM" }
    --force { set force 1 }
    --url   {
      set url [lshift argv]
      if {$url == {}} {
	puts " -ERROR- no url specified"
	incr error
	
      }
    }
    --esn   {
      set esn_arg [lshift argv]
      if {$esn_arg == {}} {
	puts " -ERROR- no esn specified"
	incr error
      } else {
	set esn $esn_arg
      }
    }
    --help {
      usage
      return 
    }
    default {
      puts "-ERROR- Invalid argument $flag"
      incr error
    }
  }
}

if {$error} {
  return -code error " -ERROR- argument problems"
}

if { !$burn && !$dump } {
  usage
  return -code error " -ERROR- must specify either --burn or --dump"
}


open_hw -quiet
connect_hw_server -url $url -quiet

# This will throw an error if no target is found
set target [selectTarget $esn]

puts "Opening cable $target"
current_hw_target $target
open_hw_target -quiet

set cmb [identifyCable [get_hw_devices] $cmb]
if { $cmb == "" } {
  if {$force} {
    set cmb "Unknown"
    set device_filter "*"
  } else {
    return -code error "-ERROR- Found no CMB $cmb on cable"
  }
} else {
  set device_filter $KNOWN_DEVICES
}

set devices [get_hw_devices $device_filter]

if {[llength $devices] > 0} {
  
  if {$dump} {
    dumpMACs $target $devices $cmb
  }

  if {$burn} {
    set macs [burnMACs $target $devices $cmb]
    close_hw_target -quiet
    current_hw_target $target
    dumpMACs $target $devices $cmb
  }
}

disconnect_hw_server -quiet
close_hw -quiet
