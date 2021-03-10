
const convict = require('convict');
// const { env } = require('yargs');

//define a schema
var config = convict({
    env: {
        env: 'NODE_ENV',
        format: ['prod', 'dev', 'test'],
        default: 'dev',
    },
    port: {
        env: 'PORT',
        arg: 'port',
        format: 'port',
        default: 3000,
    },
    pythonPath: {
        format: String,
        // default: '/usr/bin/python', // Bu seninki .env dosyasından vericez
        default: "C:/Users/macro/anaconda3/python.exe",
    },

    // env: {
    //     format: String,
    //     default: '/usr/bin/python',
    // },
});

config.load({});

config.validate({
  allowed: 'strict',
});

if (config.get('env') != 'prod') {
  console.log(config.toString());
}

module.exports = config;

