set CURRENT_DATE_TIME=%date:~0,4%-%date:~5,2%-%date:~8,2%-%time:~0,2%:%time:~3,2%:%time:~6,2% 

git add .
git commit -m "%CURRENT_DATE_TIME%"
git push origin main
   
echo %CURRENT_DATE_TIME%  
pause