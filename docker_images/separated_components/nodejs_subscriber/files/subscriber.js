const { Kafka, logLevel } = require('kafkajs')
var fs = require('fs');

const kafka = new Kafka({
  logLevel: logLevel.INFO,
  brokers: [process.argv[2]]
})

const consumer = kafka.consumer({ 
  groupId: 'test',
  rackId: process.argv[3] 
})

const topic = process.argv[4]
const filename = '/var/log/' + topic + '.csv'
var newLine= "\r\n";

const run = async () => {
  await consumer.connect()
  await consumer.subscribe({ topic, fromBeginning: false })
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
        var msg_json = JSON.parse(`${message.value}`)
        console.log("Message received:")
        console.log(`- ${message.value}`)
        var records = msg_json.records
        if ( typeof records !== 'undefined' && records ) {
            var value = records[0].value.timestamp
            var timestamp = new Date().getTime()/1000;
            var latency = timestamp - value;

            fs.stat(filename, function (err, stat) {
                var csv = latency + newLine;
                console.log('Latency value appended to file: ' + latency)
                fs.appendFile(filename, csv, function (err) {
                    if (err) throw err;
                });
            });
        }
        else {
            console.log("Latency value not appended to file")
        }
    },
  })
}

run().catch(e => console.error(`[example/consumer] ${e.message}`, e))

const errorTypes = ['unhandledRejection', 'uncaughtException']
const signalTraps = ['SIGTERM', 'SIGINT', 'SIGUSR2']

errorTypes.map(type => {
  process.on(type, async e => {
    try {
      console.log(`process.on ${type}`)
      console.error(e)
      await consumer.disconnect()
      process.exit(0)
    } catch (_) {
      process.exit(1)
    }
  })
})

signalTraps.map(type => {
  process.once(type, async () => {
    try {
      await consumer.disconnect()
    } finally {
      process.kill(process.pid, type)
    }
  })
})
