function openTab(evt, contentName, itemId, receiverId) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(contentName).style.display = "block";
    evt.currentTarget.className += " active";

    if (contentName == "Compose") {
        setMsgItemReceiver(itemId, receiverId);
    }
}

function setMsgItemReceiver(itemId, receiverId) {
    var i, itemField, receiverField;

    itemField = document.querySelector("#id_item");
    for (i = 0; i < itemField.options.length; i++) {
        var option = itemField.options[i];
        option.selected = option.value == itemId ? true : false;
    }

    receiverField = document.querySelector("#id_receiver");
    for (i = 0; i < receiverField.options.length; i++) {
        var option = receiverField.options[i];
        option.selected = option.value == receiverId ? true : false;
    }
}