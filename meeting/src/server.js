
const app = require('./app');
const { Eureka } = require('eureka-js-client');

const PORT = Number(process.env.PORT || 8083);
const HOST = '127.0.0.1';

// Configuration du client Eureka
const client = new Eureka({
  instance: {
    app: 'MEETING',
    instanceId: `meeting:${PORT}`,
    hostName: HOST,
    ipAddr: HOST,
    statusPageUrl: `http://${HOST}:${PORT}/api/meetings/hello`,
    homePageUrl: `http://${HOST}:${PORT}/`,
    healthCheckUrl: `http://${HOST}:${PORT}/api/meetings/hello`,
    port: {
      '$': PORT,
      '@enabled': 'true'
    },
    vipAddress: 'meeting',
    dataCenterInfo: {
      '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
      name: 'MyOwn'
    }
  },

  eureka: {
    host: 'localhost',
    port: 8761,
    servicePath: '/eureka/apps/',
    registerWithEureka: true,
    fetchRegistry: true
  }
});

// Démarrer le serveur Express
const server = app.listen(PORT, () => {
  console.log(`Meeting running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);

  // Enregistrement auprès du serveur Eureka
  client.start((error) => {
    if (error) {
      console.error('Eureka registration failed:', error);
    } else {
      console.log('MEETING registered successfully in Eureka!');
    }
  });
});

// Arrêt propre du microservice
function shutdown() {
  console.log('Stopping Meeting microservice...');

  client.stop(() => {
    server.close(() => {
      process.exit(0);
    });
  });
}

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
