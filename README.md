# Roblox-Items-Sniper
Buys any item you want at any price automatically (don't work on limited).



## Instructions
(windows only)

### Step 1: Download Python
You can download Python from www.python.org/downloads/release/python-3115/. If you're on Windows, I recommend downloading the x64 version. Make sure to check the box at the bottom that will say "Add Python to PATH."

### Step 2: Download the sniper
(You're already here.) Download the main.py and settings.json files.

### Step 3: Edit the settings.json file
This is easy. Get your .ROBLOSECURITY cookie (look up a tutorial for that if you need it) and put that in the quotes after "cookie". Then, put the item IDs and the max price you'd pay in the items section. Keep "watch_speed" the same. Your file should then look something like this:
```
{
    "cookie": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_....",
    "items": {
        
        //"id": price,
        "15056545609": 80,
        "15035204715": 250,
        "15056767344": 120,
        "15056630331": 30

    },
    "watch_speed": 1
}
```

### Step 4: Download the dependencies
Open a command prompt file and type python ```-m pip install requests```.

After the request has been installed also in the cmd run ```pip install colorama```.





### Credits
This sniper uses code from https://github.com/workframes/personals-sniper, so all the credits belong to the frames.
Additionally, the instructions are written by a7x (__a7x), they were just so well written so i kinda took em 😁🙏.
