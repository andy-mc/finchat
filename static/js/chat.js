$(function() {
    var ws_path = "/chat/stream/";

    var webSocketBridge = new channels.WebSocketBridge();
    webSocketBridge.connect(ws_path);

    webSocketBridge.listen(function(message) {
        var messagesDiv = $("#room .messages");
        
        userMessage = $("<div class='message'></div>");

        userMessage.append(
            $("<span class='username'></span>").text(message['username'])
        )
        userMessage.append(
            $("<span class='msg-text'></span>").text(message['message'])
        )
        userMessage.append(
            $("<span class='timestamp'></span>").text(message['timestamp'])
        )

        messagesDiv.append(userMessage);
    });

    $("#chatform").on("submit", function(event) {
        event.preventDefault();
        var message = {
            username: $('#username').val(),
            message: $('#message').val(),
        }
        webSocketBridge.send(message);
        $("#message").val('').focus();
    });
});
