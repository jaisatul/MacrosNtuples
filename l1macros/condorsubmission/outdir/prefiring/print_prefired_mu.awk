BEGIN { last_print = ""; print_lines = -1}
/^run/ { print_lines = 4 ;
    this_print = $0}
{
    #if(print_lines > 0){
    #   if(last_print != this_print){ print $0; print_lines -= 1 }}
    #   if(last_print != this_print){ print $0; print_lines -= 1 }}
    if(print_lines > 0){ print $0; print_lines -= 1 }
    if(print_lines == 0){ print ""; print_lines -= 1; last_print = this_print}
}
