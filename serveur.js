// installer nodemon pour eviter de relancer le seveur lors de modif du fichier
const http = require('http');

const server = http.createServer((req, res) => {
    res.end('Voilà la réponse du serveur !');
});

server.listen(process.env.PORT || 3000); //serveur ecoute sur le port 3000