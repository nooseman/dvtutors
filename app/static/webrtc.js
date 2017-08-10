var stun = {
	'url' : 'stun:stun.l.google.com:19302'
};

var webrtc = new SimpleWebRTC({
	localVideoEl: 'localVideo',
	remoteVideosEl: 'remotesVideos',
	autoRequestMedia: true,
	enableDataChannels: true,
	peerConnectionConfig: { 'iceServers': [stun, null] }
});