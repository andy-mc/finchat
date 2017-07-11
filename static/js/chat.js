$(function() {
    var ws_path = "/chat/stream/";

    var webSocketBridge = new channels.WebSocketBridge();
    webSocketBridge.connect(ws_path);

    webSocketBridge.listen(function(message) {
        var tbody = $("tbody");
        
        userMessage = $("<tr></tr>");

        userMessage.append(
            $("<td class='username'></td>").text(message['username'])
        )
        userMessage.append(
            $("<td></td>").text(message['message'])
        )
        userMessage.append(
            $("<td></td>").text(message['timestamp'])
        )

        tbody.append(userMessage);
    });

    $("#chatform").on("submit", function(event) {
        event.preventDefault();
        var message = {
            message: $('#message').val(),
        }
        webSocketBridge.send(message);
        $("#message").val('').focus();
    });
});
