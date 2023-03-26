# IceCubeLogging
A quick resource monitoring script for linux and windows devices I made for fun while trying to learn useful informational commands.

All that needs to be done for the script to run is to type "python3 IceCubeXXX" with XXX being Win or Lin in the command prompt. It then takes a second to run through the code in the script and it will create an HTML file titled with the date and time for tracking purposes in the directory you have the script file in. you can open up said file in your web browser and scroll through the information it grabbed, or just look through the HTML you psycho.

Its rather easy to read and understand where which bits of code come from so if you would rather it not grab certain data you can quite simply remove that section from the code.

I imagine its best use could be when paired with chron scheduling or something of a simular sort in order for it to be ran on a daily basis or during certain times throughout the day. This is to ensure you have enough data to track resource usage like storage space consumption and ram and cpu during peak operation times. You can also write another script to grab the info you want from said logging files from a certain date range and paste it into an excel spreadsheet. I've managed that too and if i refine it more I might also add that to this repo.


