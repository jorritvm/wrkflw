# define if we are in interactive mode or not
if (commandArgs()[1] == "RStudio") {
  interactive = TRUE
} else {
  interactive = FALSE
}

# command line argument parsing
option_list = list(
  make_option("--param", type="character", default="success", 
              help="pass either 'success' or 'failure'", metavar="character")
)

opt_parser = OptionParser(option_list=option_list)
cargs = parse_args(opt_parser)