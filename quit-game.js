#!/usr/bin/env node

const socket = new WebSocket('ws://localhost:1312');

socket.onclose = () => {
    process.exit(0);
}

socket.onopen = () => {
    socket.send('quit').then(() => {
        socket.close();
    });
};
