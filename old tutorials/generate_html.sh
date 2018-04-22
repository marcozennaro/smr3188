#!/bin/bash

#cd ./labs

#grip --user marcozennaro --pass Eatmenow71! 1-lab-day-1.md --export 1-lab-day-1.html
#grip --user marcozennaro --pass Eatmenow71! 2-lab-day-2.md --export 2-lab-day-2.html
#grip --user marcozennaro --pass Eatmenow71! 3-lab-day-3.md --export 3-lab-day-3.html
#grip --user marcozennaro --pass Eatmenow71! 4-lab-day-4.md --export 4-lab-day-4.html

#grip --user marcozennaro --pass Eatmenow71! LED.md --export LED.html
#grip --user marcozennaro --pass Eatmenow71! lora-mac.md --export lora-mac.html
grip --user marcozennaro --pass Eatmenow71! button.md --export button.html
#grip --user marcozennaro --pass Eatmenow71! resources.md --export resources.html
#grip --user marcozennaro --pass Eatmenow71! lora-sensing-final-project.md --export lora-sensing-final-project.html
#grip --user marcozennaro --pass Eatmenow71! setting-up-a-raspberry.md --export setting-up-a-raspberry.html
#grip --user marcozennaro --pass Eatmenow71! data-analysis-for-iot.md --export data-analysis-for-iot.html
#grip --user marcozennaro --pass Eatmenow71! mqtt.md --export mqtt.html
#grip --user marcozennaro --pass Eatmenow71! setup.md --export setup.html
#grip --user marcozennaro --pass Eatmenow71! github-introduction.md --export github-introduction.html
grip --user marcozennaro --pass Eatmenow71! persisting-data.md --export persisting-data.html
#grip --user marcozennaro --pass Eatmenow71! workflow.md --export workflow.html
#grip --user marcozennaro --pass Eatmenow71! lora-coverage.md --export lora-coverage.html
grip --user marcozennaro --pass Eatmenow71! pysense.md --export pysense.html
#grip --user marcozennaro --pass Eatmenow71! WiFi.md --export WiFi.html


cd ..

mkdir html
mv ./labs/*.html html
cd html
sed -i -- 's/.md/.html/g' *
rm *.html--

cd ..

# grip --user marcozennaro --pass Eatmenow71! agenda.md --export index.html
