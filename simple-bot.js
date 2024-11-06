const mineflayer = require('mineflayer');
const { Server } = require('socket.io');
const mcData = require('minecraft-data')('1.20.6');
const { pathfinder, Movements, goals } = require('mineflayer-pathfinder');

//Setting up bot arguments necessary for proper connection
const botArgs = {
    host: 'localhost', //will connect to local computer
    port: '56769', //port of minecraft LAN multiplayer world
    username: "DawgZilla_AI", 
    version: '1.20.6' //minecraft version
};

let bot = mineflayer.createBot(botArgs); //creates instance "bot", passes arguments previously declared
/*
Separating the arguments from the createBot function will allow us to easily scale up our scripts, IF we wish to 
host multiple bots at once
*/

// Set up Socket.IO server
const io = new Server(3000);

// Set up block IDs for events
const oakLogId = mcData.blocksByName.oak_log.id; // Access the oak_log block ID
console.log(`Oak log block ID: ${oakLogId}`); // Confirms

// Enable pathfinding
bot.loadPlugin(pathfinder);

// BOT EVENTS
// Mineflayers built in event "login". When "bot" listens that "login" was succesful, callback is provided
bot.on('login',() => { // when "login" is succesful, call function "botSocket"
    let botSocket = bot._client.socket; // Creates block-scoped variable that will hold connection info 
    console.log(`Logged in to ${botSocket.server ? botSocket.server : botSocket._host}`); // Outputs a message indicating wether the bot has logged into an external server or local server
}); // (Is there a server inside the socket?)

// Mineflayer built in event "end". When "bot" listens that "end" was succesfull, print Disconnected
bot.on('end', () => {
    console.log('Disconnected');
});

// Mineflayer built in event "spawn". When "bot" listens that "spawn" was succesfull, print lines
bot.on('spawn', async () => {
    const x = 5; // target coordinates
    const y = 88;
    const z = -5;
    console.log("Spawned in"); // On terminal
    bot.chat("Hello! :3"); // On game

    findWoodBlock();
});


//FUNCTIONS
function checkInventory(){
    const oakLogs = bot.inventory.items().find(item => item.type === mcData.blocksByName.oak_log.id);
    if (oakLogs && oakLogs.count >= 64) {
        bot.toss(oakLogs.type, null, 64)  // Drop 64 logs
            .then(() => bot.chat('Dropped a stack of oak logs!'))
            .catch(err => console.error('Error dropping logs:', err));
    }
}

function lookUpAfterChop() {
    // Makes the bot look up at a slight angle
    const lookUpPitch = -Math.PI / 4; // Upward angle; adjust this value as needed
    bot.look(bot.entity.yaw, lookUpPitch, true, () => {
        console.log("Looking up after chopping.");
    });
}

function lookAtBlock(woodBlockFound){
    const targetPosition = woodBlockFound.position.offset(0.5, 0.5, 0.5); // Center of the block
    bot.lookAt(targetPosition, true, () => {
        console.log('Looking at oak log.');
    });
}

function chopWoodBlock(woodBlockFound){
    console.log('woodBlockFound not null');
    const { x, y, z } = woodBlockFound.position; // Get the block's position
    lookAtBlock(woodBlockFound);
    // Use pathfinder to move to the block
    const movements = new Movements(bot);
    bot.pathfinder.setMovements(movements);
    bot.pathfinder.goto(new goals.GoalBlock(x, y, z)).then(() => {
        // After reaching the block, chop it
        bot.dig(woodBlockFound, () => {
            console.log('Chopping...');
            checkInventory();  // Check inventory after each chop
            lookUpAfterChop();
            setTimeout(findWoodBlock, 500); // Short delay before finding the next block

        });
    }).catch(err => console.error('Failed to go to the block:', err));
}

function findWoodBlock(){
    // Find and chop a specific type of wood within a 64-block radius
    const woodBlockFound = bot.findBlock({ // findBlock is a Mineflayer built in function. woodBlockFound It will store the block info if the block is found 
        matching: mcData.blocksByName.oak_log.id, // Block ID that the bot will look for
        maxDistance: 64 
    });
    if (woodBlockFound) {
        bot.chat('Oak log found within range!');
        chopWoodBlock(woodBlockFound);
    } else {
        bot.chat('No oak log found within range :(');
    }
}


// IO EVENTS
// Listen for chop command from Python
io.on('connection', (socket) => {
    console.log('Python connected'); // Confirm connection to python
// After connection is succesful, respond to chop command:
    socket.on('chop', () => { // Reply/callback to chop event/command (sent from python)
        console.log('Chop command heard');
        findWoodBlock();

    }); console.log('Chop ended');
});