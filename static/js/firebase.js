// Initialize Firebase
    // TODO: Replace with your project's customized code snippet
    var config = {
        'messagingSenderId': '1095787248901',
        'apiKey': 'AIzaSyBf2FrQiAE5VnbdkiPVNZ9t8FKdKYeF8S4',
        'projectId': 'dazzling-byway-291808',
        'appId': '1:1095787248901:web:bf3b07d826ce1e6540cb6c',

    };
    firebase.initializeApp(config);

const messaging = firebase.messaging();

messaging.requestPermission().then(function(){
    console.log('notification permission granted');
    getRegisterToken();
    if(isTokenSentToServer()){
        console.log("token already sent");
    }
    else{
        getRegisterToken();
    }
    })
    .catch(function(err){
        console.log('unable to get permission',err);

 });


function getRegisterToken(){

// Get registration token. Initially this makes a network call, once retrieved
// subsequent calls to getToken will return from cache.


    messaging.getToken().then(function(currentToken){
    if (currentToken) {
    globalThis.fcm_token = currentToken;
    console.log(currentToken);
    sendTokenToServer(currentToken);
    //updateUIForPushEnabled(currentToken);
  } else {
    // Show permission request.
    console.log('No registration token available. Request permission to generate one.');
    // Show permission UI.
    //updateUIForPushPermissionRequired();
    setTokenSentToServer(false);
  }
}).catch(function(err) {
  console.log('An error occurred while retrieving token. ', err);
  //showToken('Error retrieving registration token. ', err);
  setTokenSentToServer(false);
});
}

function setTokenSentToServer(sent) {
    window.localStorage.setItem('sentToServer', sent ? '1' : '0');
}

function sendTokenToServer(currentToken) {
if (!isTokenSentToServer()) {
  console.log('Sending token to server...');
  // TODO(developer): Send the current token to your server.
  setTokenSentToServer(true);
} else {
  console.log('Token already sent to server so won\'t send it again ' +
      'unless it changes');
}

}

function isTokenSentToServer() {
    return window.localStorage.getItem('sentToServer') === '1';
}
