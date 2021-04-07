const express = require('express')
const app = express()
const port = 3001

const { PythonShell } = require('python-shell');
const config = require("../config/config");

let options = {
    mode: 'text',
    pythonPath: config.get("pythonPath"),
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: './fem',
    args: ['value1', 'value2', 'value3', 'value4']
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
    PythonShell.run('/topla.py', { ...options, args: [a, b] }, function (err, results) {
        if (err) {
            return res.send(err);
        }
        console.log('results: j%', results);
        return res.send({ ok: true, payload: results });
    });
})

app.post("/truss2D/solve", (req, res) => {
    const { h, dLx, N } = req.body;

    PythonShell.run('/truss2D.py', { ...options, args: [h, dLx, N] }, function (err, results) {
        if (err) {
            console.log(err);
            return res.send(err);
        }
        const rjson = JSON.parse(results);
        return res.send({ ok: true, payload: rjson });
    });
})

app.post("/truss2D", (req, res) => {
    const {
        node1x, node1y, node1rx, node1ry,
        node2x, node2y, node2rx, node2ry,
        node3x, node3y, node3rx, node3ry,
        node4x, node4y, node4rx, node4ry,
        node5x, node5y, node5rx, node5ry,
        Elm1ni, Elm1nj, Elm1EA,
        Elm2ni, Elm2nj, Elm2EA,
        Elm3ni, Elm3nj, Elm3EA,
        Elm4ni, Elm4nj, Elm4EA,
        Elm5ni, Elm5nj, Elm5EA,
        Elm6ni, Elm6nj, Elm6EA,
        Elm7ni, Elm7nj, Elm7EA } = req.body;
    PythonShell.run('/main.py', {
        ...options, args: [
            node1x, node1y, node1rx, node1ry,
            node2x, node2y, node2rx, node2ry,
            node3x, node3y, node3rx, node3ry,
            node4x, node4y, node4rx, node4ry,
            node5x, node5y, node5rx, node5ry,
            Elm1ni, Elm1nj, Elm1EA,
            Elm2ni, Elm2nj, Elm2EA,
            Elm3ni, Elm3nj, Elm3EA,
            Elm4ni, Elm4nj, Elm4EA,
            Elm5ni, Elm5nj, Elm5EA,
            Elm6ni, Elm6nj, Elm6EA,
            Elm7ni, Elm7nj, Elm7EA]
    }, function (err, results) {
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
