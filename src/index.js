const express = require('express')
const app = express()
const port = 3000

app.use(express.static('public'));
app.use(express.json());

app.post("/topla", async (req, res) => {
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