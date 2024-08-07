const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const fs = require('fs');

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(express.static('.'));

app.post('/generate_diet_plan', (req, res) => {
    const userData = req.body;

    fs.writeFileSync('user_data.json', JSON.stringify(userData, null, 2));

    exec('python generate_diet_plan.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error.message}`);
            return res.status(500).send('Error generating diet plan');
        }
        if (stderr) {
            console.error(`Script error: ${stderr}`);
            return res.status(500).send('Error generating diet plan');
        }

        const dietPlan = JSON.parse(fs.readFileSync('diet_plan.json', 'utf8'));
        res.json(dietPlan);
    });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
