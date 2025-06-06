
document.addEventListener("DOMContentLoaded", function() {

  const TellerConnect = window.TellerConnect;

  var appId = null
  var environment = null

  fetch('/app')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {

      appId = data.app_id
      environment = data.environment

      console.log(appId)
      console.log(environment)

      var tellerConnect = TellerConnect.setup({
        applicationId: appId,
        products: ["transactions", "balance"],
        environment: environment,
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

      var el = document.getElementById("teller-connect");
      el.addEventListener("click", function() {
        tellerConnect.open();
      });
    })
    .catch(error => {
      console.error('Fetch error:', error);
    });
});

