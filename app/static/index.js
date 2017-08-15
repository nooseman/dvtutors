$(document).ready(function() {
    var connection = new RTCMultiConnection();

    //connection.socketURL = 'https://rtcmulticonnection.herokuapp.com:443/';
    connection.socketURL = "http://localhost:9001/";
    //connection.socketURL = 'https://dvsignal.herokuapp.com:443/'

    connection.iceServers = [];
    connection.iceServers.push({
        urls: 'stun.l.google.com:19302'
    });

    connection.session = {
        audio:true,
        video: true,
        data: true
    };

    connection.sdpConstraints.mandatory = {
        OfferToReceiveAudio: true,
        OfferToReceiveVideo: true
    };

    connection.enableFileSharing = true;

    connection.onstream = function(event) {
        var video = event.mediaElement;

        if (event.type === 'local') {
            document.getElementById('localVideos').appendChild(video);
        } else if (event.type === 'remote') {
            document.getElementById('remoteVideos').appendChild(video);
        }
    };

    connection.onmessage = function(event) {
        console.log('Message received: ' + event.data);
        document.getElementById('incoming-messages').appendChild(event.data);
    };

    var room_id = window.location.href.match(/[^\/]*$/);
    //var room_id = prompt('Room?');
    connection.openOrJoin(room_id);
    
});