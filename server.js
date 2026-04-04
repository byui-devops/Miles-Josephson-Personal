const express = require('express');
const { isValidAge } = require('./pattern');

const app = express();
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.get('/validate-age/:age', (req, res) => {
  const age = parseInt(req.params.age, 10);
  const valid = isValidAge(age);
  res.json({ age, valid });
});

if (require.main === module) {
  app.listen(8080, () => {
    console.log('Age Validator API running on port 8080');
  });
}

module.exports = app;
