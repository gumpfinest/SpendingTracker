@REM ----------------------------------------------------------------------------
@REM Maven Wrapper startup batch script for Windows
@REM ----------------------------------------------------------------------------

@echo off
setlocal

set MAVEN_PROJECTBASEDIR=%~dp0
set WRAPPER_JAR="%MAVEN_PROJECTBASEDIR%.mvn\wrapper\maven-wrapper.jar"
set WRAPPER_URL="https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.2.0/maven-wrapper-3.2.0.jar"

@REM Check if wrapper jar exists, if not download it
if not exist %WRAPPER_JAR% (
    echo Maven Wrapper not found. Downloading...
    if not exist "%MAVEN_PROJECTBASEDIR%.mvn\wrapper" mkdir "%MAVEN_PROJECTBASEDIR%.mvn\wrapper"
    powershell -Command "Invoke-WebRequest -Uri %WRAPPER_URL% -OutFile %WRAPPER_JAR%"
)

@REM Check for JAVA_HOME
if not "%JAVA_HOME%"=="" goto OkJHome
for %%i in (java.exe) do set "JAVACMD=%%~$PATH:i"
goto checkJCmd

:OkJHome
set "JAVACMD=%JAVA_HOME%\bin\java.exe"

:checkJCmd
if exist "%JAVACMD%" goto chkMHome

echo Error: JAVA_HOME is not defined correctly. >&2
echo We cannot execute %JAVACMD% >&2
goto error

:chkMHome
set "MAVEN_HOME=%MAVEN_PROJECTBASEDIR%"

@REM Download Maven if wrapper jar doesn't have it
set "MAVEN_CMD=mvn"
where mvn >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Maven not found in PATH. Using wrapper to download...
    "%JAVACMD%" -jar %WRAPPER_JAR% %*
    goto end
)

@REM Execute Maven
%MAVEN_CMD% %*
goto end

:error
set ERROR_CODE=1

:end
endlocal & exit /b %ERROR_CODE%
