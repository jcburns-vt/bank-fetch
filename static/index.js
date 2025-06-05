const TellerConnect = window.TellerConnect;

document.addEventListener("DOMContentLoaded", function() {
    var tellerConnect = TellerConnect.setup({
        applicationId: "app_peevqq8j16t30s9eig000",
        products: ["verify", "transactions", "balance"],
        environment: "development", // sandbox, production, development
        onInit: function() {
            console.log("Teller Connect has initialized");
        },
        onSuccess: function(enrollment) {
            console.log("User enrolled successfully", enrollment.accessToken);
            fetch('/complete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    access_token: enrollment.accessToken
                })
            });
            document.body.innerHTML = "Connection successful, you may close this window now.";
        },
        onExit: function() {
            console.log("User closed Teller Connect");
        }
    });

    // Part 4. Hook user actions to start Teller Connect
    var el = document.getElementById("teller-connect");
    el.addEventListener("click", function() {
        tellerConnect.open();
    });
});

