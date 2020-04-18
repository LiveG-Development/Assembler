:: LiveG Assembler
:: 
:: Copyright (C) LiveG. All Rights Reserved.
:: Copying is not a victimless crime. Anyone caught copying LiveG software may
:: face sanctions.
:: 
:: https://liveg.tech
:: Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

@echo off

set DIR=%~dp0

py -3 "%DIR%\gas.py" %*