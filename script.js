
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.submit-btn').addEventListener('click', processInput);
  });
  document.querySelector('.submit-btn').addEventListener('click', function() {
    var userInput = document.getElementById('user-input').value;
    
    getShipperName(userInput);
  });
  function getShipperName(userInput) {
    const sparql = `
      PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
      PREFIX code: <https://onerecord.iata.org/ns/code-lists/>
      SELECT ?name WHERE {
        ?party a cargo:Party ;
               cargo:partyRole <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#SHP> ;
               cargo:partyDetails [ cargo:name ?name ] .
      }`;
    callApi(userInput).then(data => {

      // 显示到前端（假设有一个 id 为 "result" 的 HTML 元素）
      document.getElementById("shipperName").textContent = data.shipper_info[0].name;
      document.getElementById("consigneeName").textContent = data.consignee_info[0].name;

    }).catch(error => {
      console.error("Error fetching data:", error);
    });
  }
function processInput() {
    var userInput = document.getElementById('user-input').value;
    console.log("User hello input:", userInput);
}

function callApi(userInput) {

  var data = {
    jsonld: JSON.parse(userInput)
  };


  return fetch('http://localhost:5000/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
    // You can handle the response data here
    return data;
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

