@echo off
echo Cleaning node_modules...
if exist node_modules rmdir /s /q node_modules
if exist .next rmdir /s /q .next
if exist package-lock.json del package-lock.json

echo Installing dependencies...
npm install

echo Setup complete!