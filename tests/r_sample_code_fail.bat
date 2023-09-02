set rscript="C:/Program Files/R/R-4.2.2/bin/Rscript.exe"

set "original_dir=%cd%"

cd /d C:\dev\python\wrkflw\tests\r_sample_code
%rscript% main.R --param "failure"

cd /d "%original_dir%"