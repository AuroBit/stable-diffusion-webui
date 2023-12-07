@echo off

python aurobit_init.py -cache no -s3 no

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS=--xformers --no-gradio-queue --api --api-log --listen

call webui.bat
