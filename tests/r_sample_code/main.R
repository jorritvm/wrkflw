#####################################################################
# this R sample app showcases an interactive and 
# non interactive mode. 
# 
# in interactive mode the user sets up the param value in the script 
# and executes the script from within RStudio
#
# in non-interactive mode the user passes the param as a CLI argument
# 
# if the parameter equals "failure" then an error is thrown, 
# in any other case "success is print"
# 
# the project is set up with RENV
####################################################################

source("./proc_libraries.R") # load R libraries
source("./proc_commandline_args.R") # define 'interactive' and 'cargs'

if (interactive) {
  # these steps will require user interaction with modal dialogs
  param = "some_value" # any value or "failure"
} else {
  rscript = 
  param = cargs$param
}

print(param)

if (param != "failure") {
  print("success") 
} else {
  stop("random error message")
}