// Import net module.
var net = require('net');
var cs_status=0


// Create and return a net Server object, the function will be invoked when client connect to this server.
var server = net.createServer(function(client) {

    console.log('Client connect. Client local address : ' + client.localAddress + ':' + client.localPort + '. client remote address : ' + client.remoteAddress + ':' + client.remotePort);
    //encoding
    client.setEncoding('utf-8');
    //set timeout
    client.setTimeout(1000);

    // When receive client data.
    client.on('data', function (data) {

        // Print received client data and length.
        console.log('Receive client send data : ' + data + ', data size : ' + client.bytesRead);

        // Server send data back to client use client net.Socket object.
        console.log("Received Ready message");
        if (data === "request" && cs_status === 1) {
            console.log("I have received a request for my status");
            console.log("I am in my critical Section", cs_status);
            //wait until you are out critical section
        }
        else if(data === "request" && cs_status === 0 ) {
            console.log("request");
            console.log("I am not in my critical section");
            client.end('OK');
        }
        else if( data === "OK"){
            console.log("Ok message received");
            console.log(data);
        }
        else
            {
                console.log("message received was", data)
                console.log("server returned, ", data)

            }
    });

    // When client send data complete.
    client.on('end', function () {
        console.log('Client disconnect.');

        // Get current connections count.
        server.getConnections(function (err, count) {
            if(!err)
            {
                // Print current connection count in server console.
                console.log("There are %d connections now. ", count);
            }else
            {
                console.error(JSON.stringify(err));
            }

        });
    });

    // When client timeout.
    client.on('timeout', function () {
        console.log('Client request time out. ');
    })
});

// Make the server a TCP server listening on port 12348.
server.listen(12348, function () {

    // Get server address info.
    var serverInfo = server.address();

    var serverInfoJson = JSON.stringify(serverInfo);

    console.log('TCP server listen on address : ' + serverInfoJson);

    server.on('close', function () {
        console.log('TCP server socket is closed.');
    });

    server.on('error', function (error) {
        console.error(JSON.stringify(error));
    });

});



