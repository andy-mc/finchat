$(function() {
    var ws_path = "/chat" + window.location.pathname;

    var webSocketBridge = new channels.WebSocketBridge();
    webSocketBridge.connect(ws_path);
    updateScroll()

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
        updateScroll()
    });

    $("#chatform").on("submit", function(event) {
        event.preventDefault();
        var message = {
            message: $('#message').val(),
        }
        webSocketBridge.send(message);
        updateScroll()
        $("#message").val('').focus();
    });
});

function updateScroll() {
    var messages = $(".messages");
    messages.stop().animate({ scrollTop: messages[0].scrollHeight}, 1000);
}
