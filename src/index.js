const express = require('express')
const app = express()
const port = 3000

const { PythonShell } = require('python-shell');
const convict = require('convict');

let options = {
    mode: 'text',
    pythonPath: '/config/config.js',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: './src',
    args: ['value1', 'value2', 'value3']
};

app.use(express.static('public'));
app.use(express.json());



const deneme = (req, res, next) => {
    const { a, b } = req.body;

    if (!a || !b) {
        return res.status(400).end();
    } else {
        return next();
    }
}


app.post("/run", (req, res) => {
    const { a, b } = req.body;
    PythonShell.run('/topla.py', {...options, args: [a, b]}, function (err, results) {
        if (err) {
            return res.send(err);
        }
        console.log('results: %j', results);
        return res.send({ ok: true, payload: results });
    });
})


app.post("/topla", [deneme], async (req, res) => {
    try {
        const { a, b } = req.body;
        res.json({ payload: { c: a + b } })
    } catch (error) {
        res.status(400).end()
    }
})

// app.get('/', (req, res) => {
//   res.send('Hello World!')
// })

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})

console.log("SOOOOOOOOOOOOOOOOOOOOOOON")