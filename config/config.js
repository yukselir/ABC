
const convict = require('convict');
const { env } = require('yargs');

//define a schema
var config = convict({
    env: {
        format: String,
        default: '/usr/bin/python',
    },
});

// Load environment dependent configuration
const env = config.get('env');
config.loadFile('./config/' + env + '.json'); 

// Perform validation
config.validate({allowed: 'strict'});
module.exports = config();
 
